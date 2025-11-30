"""AI processing module using OpenAI API."""

from typing import Dict, Optional
from openai import AsyncOpenAI
from config import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class AIProcessor:
    """Process messages using OpenAI API."""
    
    def __init__(self):
        """Initialize AI processor."""
        self.client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.OPENAI_MODEL
    
    def _clean_forwarded_text(self, text: str) -> str:
        """Remove forwarded message signatures and metadata."""
        if not text:
            return text
        
        lines = text.split('\n')
        cleaned = []
        
        for line in lines:
            line_stripped = line.strip()
            
            # Пропускаем пустые строки в начале
            if not line_stripped and not cleaned:
                continue
            
            # Пропускаем строки с каналами (содержат |)
            if '|' in line and len(line_stripped) < 60:
                continue
            
            # Пропускаем строки начинающиеся с @
            if line_stripped.startswith('@'):
                continue
            
            # Пропускаем разделители
            if line_stripped in ['—', '——', '———', '____', '---', '___', '–', '–––']:
                continue
            
            # Пропускаем строки только из символов
            if line_stripped and all(c in '—_-=|–' for c in line_stripped):
                continue
            
            cleaned.append(line)
        
        # Убираем пустые строки в конце
        while cleaned and not cleaned[-1].strip():
            cleaned.pop()
        
        return '\n'.join(cleaned).strip()
    
    async def process_message(self, text: str, has_image: bool = False) -> Dict[str, str]:
        """
        Process message text and generate full and short versions.
        
        Args:
            text: Original message text
            has_image: Whether message has an image
            
        Returns:
            Dictionary with 'full_text' and 'short_text' keys
        """
        try:
            # Очищаем от подписей пересылки
            text = self._clean_forwarded_text(text)
            
            if not text and has_image:
                # Generate description for image-only message
                return await self._generate_image_description()
            
            # Detect language and process
            prompt = self._build_prompt(text)
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional social media content editor. Your task is to improve text for social media posts."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content.strip()
            
            # Parse the response
            full_text, short_text = self._parse_response(result)
            
            logger.info("Message processed successfully")
            return {
                'full_text': full_text,
                'short_text': short_text
            }
            
        except Exception as e:
            logger.error(f"AI processing failed: {e}")
            # Fallback: return original text
            return {
                'full_text': text,
                'short_text': self._create_short_version(text)
            }
    
    def _build_prompt(self, text: str) -> str:
        """
        Build prompt for AI processing.
        
        Args:
            text: Original text
            
        Returns:
            Formatted prompt
        """
        return f"""Process this social media post:

Original text:
{text}

Tasks:
1. If the text is in Russian, translate it to English
2. Improve the writing style to be engaging and professional
3. Keep the main message and meaning intact
4. Preserve any links or URLs as-is

Provide TWO versions:

FULL VERSION:
[Write the full improved/translated version here]

SHORT VERSION:
[Write a concise version (max 240 characters) with relevant hashtags. The total length including hashtags must not exceed 280 characters for Twitter]

Format your response EXACTLY as shown above with clear section headers."""
    
    async def _generate_image_description(self) -> Dict[str, str]:
        """
        Generate description for image-only message.
        
        Returns:
            Dictionary with generated descriptions
        """
        try:
            prompt = """Generate a short, engaging social media caption for an image.

Requirements:
1. Create an interesting caption (2-3 sentences)
2. Add relevant hashtags

Provide TWO versions:

FULL VERSION:
[Write a full caption here]

SHORT VERSION:
[Write a concise version (max 240 characters) with hashtags. Total length must not exceed 280 characters]"""

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a creative social media content creator."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=500
            )
            
            result = response.choices[0].message.content.strip()
            full_text, short_text = self._parse_response(result)
            
            return {
                'full_text': full_text,
                'short_text': short_text
            }
            
        except Exception as e:
            logger.error(f"Failed to generate image description: {e}")
            return {
                'full_text': "Check out this image! 📸",
                'short_text': "Check out this image! 📸 #photo #image"
            }
    
    def _parse_response(self, response: str) -> tuple[str, str]:
        """
        Parse AI response into full and short versions.
        
        Args:
            response: AI response text
            
        Returns:
            Tuple of (full_text, short_text)
        """
        try:
            # Split by sections
            parts = response.split('SHORT VERSION:')
            
            if len(parts) == 2:
                full_part = parts[0].replace('FULL VERSION:', '').strip()
                short_part = parts[1].strip()
                
                # Clean up any remaining markers
                full_text = full_part.replace('[', '').replace(']', '').strip()
                short_text = short_part.replace('[', '').replace(']', '').strip()
                
                # Ensure short text is not too long
                if len(short_text) > 280:
                    short_text = short_text[:277] + '...'
                
                return full_text, short_text
            
            # Fallback if parsing fails
            return response, self._create_short_version(response)
            
        except Exception as e:
            logger.error(f"Failed to parse AI response: {e}")
            return response, self._create_short_version(response)
    
    def _create_short_version(self, text: str) -> str:
        """
        Create a short version of text as fallback.
        
        Args:
            text: Original text
            
        Returns:
            Shortened text with hashtags
        """
        # Take first 240 characters
        short = text[:240]
        
        # Add generic hashtags
        short += " #content #social"
        
        # Ensure it's not too long
        if len(short) > 280:
            short = short[:277] + "..."
        
        return short
```

---

## 📋 Что изменилось:

1. ✅ Добавлен метод `_clean_forwarded_text()` - удаляет подписи из пересланных сообщений
2. ✅ В `process_message()` добавлен вызов очистки текста
3. ✅ Улучшена логика очистки - убирает:
   - Строки с `|` (типа "RU | BigLiquid | Pro Channel")
   - Строки начинающиеся с `@` (типа "@meduzalive")
   - Разделители (`—`, `___`, и т.д.)
   - Пустые строки в начале и конце

---

## 🔧 Что делать:

1. **Откройте** `bot/ai_processor.py` на GitHub
2. **Нажмите Edit**
3. **Удалите всё** содержимое
4. **Вставьте** код выше
5. **Commit changes**: 
```
   Add automatic cleaning of forwarded message signatures
