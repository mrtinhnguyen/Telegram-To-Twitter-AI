"""Telegram bot handler for receiving messages."""

from typing import Optional
from pathlib import Path
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)
from config import config
from utils.logger import setup_logger
from utils import ImageHandler
from bot.ai_processor import AIProcessor
from bot.telegram_publisher import TelegramPublisher
from bot.twitter_publisher import TwitterPublisher

logger = setup_logger(__name__)


class TelegramHandler:
    """Handle incoming Telegram messages and orchestrate publishing."""
    
    def __init__(self):
        """Initialize Telegram handler."""
        self.image_handler = ImageHandler()
        self.ai_processor = AIProcessor()
        self.telegram_publisher = TelegramPublisher()
        self.twitter_publisher = TwitterPublisher()
        
        # Build application
        self.application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(
            MessageHandler(
                filters.User(user_id=int(config.AUTHORIZED_USER_ID)) & 
                (filters.TEXT | filters.PHOTO),
                self.handle_message
            )
        )
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        await update.message.reply_text(
            "🤖 <b>Social Content Bridge Bot</b>\n\n"
            "I will help you republish content to your Telegram channel and Twitter!\n\n"
            "📝 <b>How to use:</b>\n"
            "1. Forward any message to me (text and/or image)\n"
            "2. I will process it with AI\n"
            "3. I will automatically publish to your channel and Twitter\n\n"
            "🔧 Use /help for more information",
            parse_mode='HTML'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        await update.message.reply_text(
            "📖 <b>Help</b>\n\n"
            "<b>Features:</b>\n"
            "✅ Translate Russian to English\n"
            "✅ Improve text style\n"
            "✅ Generate short version for Twitter (≤280 chars)\n"
            "✅ Add relevant hashtags\n"
            "✅ Support images (first image only)\n"
            "✅ Generate captions for image-only posts\n\n"
            "<b>What to send:</b>\n"
            "• Text messages\n"
            "• Messages with images\n"
            "• Images only (AI will generate caption)\n\n"
            "<b>Not supported:</b>\n"
            "• Videos\n"
            "• Multiple images (only first is used)\n"
            "• Audio files\n\n"
            "🔐 Only authorized user can use this bot",
            parse_mode='HTML'
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle incoming message and orchestrate the publishing flow.
        
        Args:
            update: Telegram update object
            context: Telegram context object
        """
        try:
            # Send processing notification
            status_msg = await update.message.reply_text("⏳ Processing your message...")
            
            # Extract message content
            text = update.message.text or update.message.caption or ""
            has_photo = bool(update.message.photo)
            
            # Check if message has content
            if not text and not has_photo:
                await status_msg.edit_text("❌ No content to publish. Please send text and/or image.")
                return
            
            # Download image if present
            image_path: Optional[Path] = None
            if has_photo:
                photo = update.message.photo[-1]  # Get largest size
                file = await context.bot.get_file(photo.file_id)
                image_path = await self.image_handler.download_image(file, photo.file_id)
                
                if image_path:
                    # Optimize image for social media
                    image_path = self.image_handler.optimize_image(image_path)
            
            # Process text with AI
            await status_msg.edit_text("🤖 Processing with AI...")
            processed = await self.ai_processor.process_message(text, has_image=has_photo)
            
            full_text = processed['full_text']
            short_text = processed['short_text']
            
            logger.info(f"Full text ({len(full_text)} chars): {full_text[:100]}...")
            logger.info(f"Short text ({len(short_text)} chars): {short_text}")
            
            # Publish to Telegram channel
            await status_msg.edit_text("📤 Publishing to Telegram...")
            telegram_success = await self.telegram_publisher.publish(full_text, image_path)
            
            # Publish to Twitter
            await status_msg.edit_text("🐦 Publishing to Twitter...")
            twitter_success = await self.twitter_publisher.publish(short_text, image_path)
            
            # Cleanup temporary files
            if image_path:
                self.image_handler.cleanup(image_path)
            
            # Send final status
            status_parts = []
            if telegram_success:
                status_parts.append("✅ Telegram")
            else:
                status_parts.append("❌ Telegram")
            
            if twitter_success:
                status_parts.append("✅ Twitter")
            else:
                status_parts.append("❌ Twitter")
            
            final_status = " | ".join(status_parts)
            
            await status_msg.edit_text(
                f"<b>Publishing complete!</b>\n\n"
                f"{final_status}\n\n"
                f"📝 Full text: {len(full_text)} chars\n"
                f"🐦 Short text: {len(short_text)} chars",
                parse_mode='HTML'
            )
            
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            try:
                await update.message.reply_text(f"❌ Error: {str(e)}")
            except:
                pass
    
    def run(self):
        """Run the bot."""
        logger.info("🚀 Starting bot...")
        logger.info(f"📢 Channel: {config.TELEGRAM_CHANNEL_ID}")
        logger.info(f"👤 Authorized user: {config.AUTHORIZED_USER_ID}")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
