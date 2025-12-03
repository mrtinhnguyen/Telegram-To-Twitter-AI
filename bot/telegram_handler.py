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
            "🤖 <b>Bot Cầu Nối Nội Dung Mạng Xã Hội</b>\n\n"
            "Tôi sẽ giúp bạn đăng lại nội dung lên kênh Telegram của bạn!\n\n"
            "📝 <b>Cách sử dụng:</b>\n"
            "1. Chuyển tiếp bất kỳ tin nhắn nào cho tôi (văn bản và/hoặc hình ảnh)\n"
            "2. Tôi sẽ xử lý nó bằng AI\n"
            "3. Tôi sẽ tự động đăng lên kênh của bạn\n\n"
            "🔧 Sử dụng /help để biết thêm thông tin",
            parse_mode='HTML'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        await update.message.reply_text(
            "📖 <b>Trợ giúp</b>\n\n"
            "<b>Tính năng:</b>\n"
            "✅ Dịch tiếng Việt sang tiếng Anh\n"
            "✅ Cải thiện phong cách văn bản\n"
            "✅ Tạo phiên bản ngắn\n"
            "✅ Thêm hashtag phù hợp\n"
            "✅ Hỗ trợ hình ảnh (chỉ hình đầu tiên)\n"
            "✅ Tạo chú thích cho bài chỉ có hình ảnh\n\n"
            "<b>Bạn có thể gửi:</b>\n"
            "• Tin nhắn văn bản\n"
            "• Tin nhắn có hình ảnh\n"
            "• Chỉ hình ảnh (AI sẽ tạo chú thích)\n\n"
            "<b>Không hỗ trợ:</b>\n"
            "• Video\n"
            "• Nhiều hình ảnh (chỉ dùng hình đầu tiên)\n"
            "• File âm thanh\n\n"
            "🔐 Chỉ người dùng được ủy quyền mới có thể sử dụng bot này",
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
            status_msg = await update.message.reply_text("⏳ Đang xử lý tin nhắn của bạn...")
            
            # Extract message content
            text = update.message.text or update.message.caption or ""
            has_photo = bool(update.message.photo)
            
            # Check if message has content
            if not text and not has_photo:
                await status_msg.edit_text("❌ Không có nội dung để đăng. Vui lòng gửi văn bản và/hoặc hình ảnh.")
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
            await status_msg.edit_text("🤖 Đang xử lý bằng AI...")
            processed = await self.ai_processor.process_message(text, has_image=has_photo)
            
            full_text = processed['full_text']
            short_text = processed['short_text']
            
            logger.info(f"Full text ({len(full_text)} chars): {full_text[:100]}...")
            logger.info(f"Short text ({len(short_text)} chars): {short_text}")
            
            # Publish to Telegram channel
            await status_msg.edit_text("📤 Đang đăng lên Telegram...")
            telegram_success = await self.telegram_publisher.publish(full_text, image_path)
            
            # Publish to Twitter
            await status_msg.edit_text("🐦 Đang đăng lên Twitter...")
            twitter_success, twitter_url = await self.twitter_publisher.publish(short_text, image_path)
            
            # Cleanup temporary files
            if image_path:
                self.image_handler.cleanup(image_path)
            
            # Build final status message
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
            
            # Build message with Twitter link if available
            message_lines = [
                "<b>Đăng bài hoàn tất!</b>",
                "",
                final_status,
                "",
                f"📝 Văn bản đầy đủ: {len(full_text)} ký tự",
                f"🐦 Văn bản ngắn: {len(short_text)} ký tự"
            ]
            
            # Add Twitter link if available
            if twitter_success and twitter_url:
                message_lines.append("")
                message_lines.append(f"🔗 <a href=\"{twitter_url}\">Xem tweet trên Twitter</a>")
            
            await status_msg.edit_text(
                "\n".join(message_lines),
                parse_mode='HTML',
                disable_web_page_preview=False
            )
            
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            try:
                await update.message.reply_text(f"❌ Lỗi: {str(e)}")
            except:
                pass
    
    def run(self):
        """Run the bot."""
        logger.info("🚀 Đang khởi động bot...")
        logger.info(f"📢 Kênh: {config.TELEGRAM_CHANNEL_ID}")
        logger.info(f"👤 Người dùng được ủy quyền: {config.AUTHORIZED_USER_ID}")
        
        # Test Twitter connection
        try:
            success, message = self.twitter_publisher.test_connection()
            logger.info(message)
            if not success:
                logger.warning("⚠️ Twitter có thể không hoạt động. Kiểm tra cấu hình OAuth 1.0a trong Twitter Developer Portal.")
        except Exception as e:
            logger.warning(f"⚠️ Không thể kiểm tra kết nối Twitter: {e}")
        
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
