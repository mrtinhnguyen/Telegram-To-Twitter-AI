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
    
    async def publish(self, text: str, image_path: Optional[Path] = None) -> bool:
        """
        Publish tweet to Twitter.
        
        Args:
            text: Tweet text (must be <= 280 characters)
            image_path: Optional path to image
            
        Returns:
            True if published successfully, False otherwise
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
            
            logger.info(f"✅ Published to Twitter: {response.data['id']}")
            return True
            
        except tweepy.TweepyException as e:
            logger.error(f"❌ Failed to publish to Twitter: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error publishing to Twitter: {e}")
            return False
