"""Telegram channel publisher module."""

from pathlib import Path
from typing import Optional
from telegram import Bot
from telegram.error import TelegramError
from config import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TelegramPublisher:
    """Publish content to Telegram channel."""
    
    def __init__(self):
        """Initialize Telegram publisher."""
        self.bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
        self.channel_id = config.TELEGRAM_CHANNEL_ID
    
    async def publish(self, text: str, image_path: Optional[Path] = None) -> bool:
        """
        Publish message to Telegram channel.
        
        Args:
            text: Message text
            image_path: Optional path to image
            
        Returns:
            True if published successfully, False otherwise
        """
        try:
            if image_path and image_path.exists():
                # Publish with image
                with open(image_path, 'rb') as image_file:
                    await self.bot.send_photo(
                        chat_id=self.channel_id,
                        photo=image_file,
                        caption=text,
                        parse_mode='HTML'
                    )
                logger.info(f"✅ Published to Telegram with image: {self.channel_id}")
            else:
                # Publish text only
                await self.bot.send_message(
                    chat_id=self.channel_id,
                    text=text,
                    parse_mode='HTML'
                )
                logger.info(f"✅ Published to Telegram: {self.channel_id}")
            
            return True
            
        except TelegramError as e:
            logger.error(f"❌ Failed to publish to Telegram: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error publishing to Telegram: {e}")
            return False
