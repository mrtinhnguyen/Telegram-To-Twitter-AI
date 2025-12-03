"""Configuration settings for the bot."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Bot configuration class."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        # Telegram settings
        self.TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        self.TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
        self.AUTHORIZED_USER_ID = os.getenv('AUTHORIZED_USER_ID')
        
        # Twitter settings
        self.TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
        self.TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
        self.TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
        self.TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')
        self.TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
        
        # OpenAI settings
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        
        # Logging
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        
        # Paths
        self.BASE_DIR = Path(__file__).parent.parent
        self.TEMP_DIR = self.BASE_DIR / 'temp'
        self.TEMP_DIR.mkdir(exist_ok=True)
        
        # Validate required settings
        self._validate()
    
    def _validate(self):
        """Validate that all required settings are present."""
        required_settings = {
            'TELEGRAM_BOT_TOKEN': self.TELEGRAM_BOT_TOKEN,
            'TELEGRAM_CHANNEL_ID': self.TELEGRAM_CHANNEL_ID,
            'AUTHORIZED_USER_ID': self.AUTHORIZED_USER_ID,
            'TWITTER_API_KEY': self.TWITTER_API_KEY,
            'TWITTER_API_SECRET': self.TWITTER_API_SECRET,
            'TWITTER_ACCESS_TOKEN': self.TWITTER_ACCESS_TOKEN,
            'TWITTER_ACCESS_SECRET': self.TWITTER_ACCESS_SECRET,
            'TWITTER_BEARER_TOKEN': self.TWITTER_BEARER_TOKEN,
            'OPENAI_API_KEY': self.OPENAI_API_KEY,
        }
        
        missing = [key for key, value in required_settings.items() if not value]
        
        if missing:
            print(f"❌ Lỗi: Thiếu các biến môi trường bắt buộc: {', '.join(missing)}")
            print("Vui lòng kiểm tra file .env của bạn và đảm bảo tất cả các biến bắt buộc đã được thiết lập.")
            sys.exit(1)


# Create global config instance
config = Config()
