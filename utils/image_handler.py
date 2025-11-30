"""Image handling utilities."""

import os
from pathlib import Path
from typing import Optional
from PIL import Image
from config import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ImageHandler:
    """Handle image download, processing, and cleanup."""
    
    def __init__(self):
        """Initialize image handler."""
        self.temp_dir = config.TEMP_DIR
        
    async def download_image(self, file, file_id: str) -> Optional[Path]:
        """
        Download image from Telegram.
        
        Args:
            file: Telegram file object
            file_id: Unique file identifier
            
        Returns:
            Path to downloaded file or None if failed
        """
        try:
            # Get file path
            file_path = self.temp_dir / f"{file_id}.jpg"
            
            # Download file
            await file.download_to_drive(file_path)
            
            logger.info(f"Image downloaded: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to download image: {e}")
            return None
    
    def optimize_image(self, image_path: Path, max_size: int = 5 * 1024 * 1024) -> Path:
        """
        Optimize image for social media.
        
        Args:
            image_path: Path to image
            max_size: Maximum file size in bytes (default 5MB for Twitter)
            
        Returns:
            Path to optimized image
        """
        try:
            # Check if optimization is needed
            if os.path.getsize(image_path) <= max_size:
                return image_path
            
            # Open and optimize
            with Image.open(image_path) as img:
                # Convert RGBA to RGB if needed
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                
                # Resize if too large
                max_dimension = 4096  # Twitter limit
                if max(img.size) > max_dimension:
                    ratio = max_dimension / max(img.size)
                    new_size = tuple(int(dim * ratio) for dim in img.size)
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Save with optimization
                optimized_path = image_path.with_stem(f"{image_path.stem}_optimized")
                quality = 85
                
                while quality > 20:
                    img.save(optimized_path, 'JPEG', quality=quality, optimize=True)
                    if os.path.getsize(optimized_path) <= max_size:
                        logger.info(f"Image optimized: {optimized_path}")
                        return optimized_path
                    quality -= 5
                
                # If still too large, use original
                logger.warning("Could not optimize image enough, using original")
                return image_path
                
        except Exception as e:
            logger.error(f"Failed to optimize image: {e}")
            return image_path
    
    def cleanup(self, *file_paths: Path):
        """
        Remove temporary files.
        
        Args:
            *file_paths: Paths to files to remove
        """
        for file_path in file_paths:
            try:
                if file_path and file_path.exists():
                    file_path.unlink()
                    logger.debug(f"Cleaned up: {file_path}")
            except Exception as e:
                logger.error(f"Failed to cleanup {file_path}: {e}")
