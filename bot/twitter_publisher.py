"""Twitter publisher module."""

from pathlib import Path
from typing import Optional
import tweepy
from config import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TwitterPublisher:
    """Publish content to Twitter."""
    
    def __init__(self):
        """Initialize Twitter publisher."""
        # Twitter API v2 client
        self.client = tweepy.Client(
            bearer_token=config.TWITTER_BEARER_TOKEN,
            consumer_key=config.TWITTER_API_KEY,
            consumer_secret=config.TWITTER_API_SECRET,
            access_token=config.TWITTER_ACCESS_TOKEN,
            access_token_secret=config.TWITTER_ACCESS_SECRET
        )
        
        # API v1.1 for media upload
        auth = tweepy.OAuth1UserHandler(
            config.TWITTER_API_KEY,
            config.TWITTER_API_SECRET,
            config.TWITTER_ACCESS_TOKEN,
            config.TWITTER_ACCESS_SECRET
        )
        self.api = tweepy.API(auth)
    
    def test_connection(self) -> tuple[bool, str]:
        """
        Test Twitter API connection and permissions.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Try to get user info to verify permissions
            me = self.client.get_me()
            if me.data:
                return True, f"✅ Kết nối Twitter thành công: @{me.data.username}"
            return False, "❌ Không thể xác thực với Twitter API"
        except tweepy.TweepyException as e:
            error_msg = str(e)
            if "403" in error_msg or "Forbidden" in error_msg or "oauth1" in error_msg.lower():
                return False, "❌ Lỗi quyền OAuth! Vui lòng kiểm tra cấu hình Twitter API (xem log chi tiết)"
            return False, f"❌ Lỗi kết nối Twitter: {error_msg}"
        except Exception as e:
            return False, f"❌ Lỗi không xác định: {str(e)}"
    
    async def publish(self, text: str, image_path: Optional[Path] = None) -> tuple[bool, Optional[str]]:
        """
        Publish tweet to Twitter.
        
        Args:
            text: Tweet text (must be <= 280 characters)
            image_path: Optional path to image
            
        Returns:
            Tuple of (success: bool, tweet_url: Optional[str])
            tweet_url is None if failed or username not available
        """
        try:
            # Validate text length
            if len(text) > 280:
                logger.warning(f"Tweet text too long ({len(text)} chars), truncating to 280")
                text = text[:277] + "..."
            
            media_ids = []
            
            # Upload image if provided
            if image_path and image_path.exists():
                try:
                    media = self.api.media_upload(filename=str(image_path))
                    media_ids = [media.media_id]
                    logger.debug(f"Image uploaded to Twitter: {media.media_id}")
                except Exception as e:
                    logger.error(f"Failed to upload image to Twitter: {e}")
            
            # Create tweet
            if media_ids:
                response = self.client.create_tweet(
                    text=text,
                    media_ids=media_ids
                )
            else:
                response = self.client.create_tweet(text=text)
            
            tweet_id = response.data['id']
            logger.info(f"✅ Published to Twitter: {tweet_id}")
            
            # Get username to create tweet URL
            try:
                me = self.client.get_me()
                if me.data and me.data.username:
                    username = me.data.username
                    tweet_url = f"https://twitter.com/{username}/status/{tweet_id}"
                    return True, tweet_url
            except Exception as e:
                logger.warning(f"Could not get username for tweet URL: {e}")
                # Return success but without URL
                return True, None
            
            return True, None
            
        except tweepy.TweepyException as e:
            error_msg = str(e)
            logger.error(f"❌ Failed to publish to Twitter: {e}")
            
            # Provide helpful error messages
            if "403" in error_msg or "Forbidden" in error_msg or "oauth1" in error_msg.lower():
                logger.error("⚠️ Lỗi quyền OAuth! Vui lòng kiểm tra:")
                logger.error("1. Vào Twitter Developer Portal: https://developer.twitter.com/en/portal/dashboard")
                logger.error("2. Chọn app của bạn → Settings → User authentication settings")
                logger.error("3. Đảm bảo OAuth 1.0a được bật với quyền 'Read and Write'")
                logger.error("4. Tạo lại Access Token và Access Token Secret sau khi thay đổi quyền")
                logger.error("5. Cập nhật TWITTER_ACCESS_TOKEN và TWITTER_ACCESS_SECRET trong file .env")
            
            return False, None
        except Exception as e:
            logger.error(f"❌ Unexpected error publishing to Twitter: {e}")
            return False, None
