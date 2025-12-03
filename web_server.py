#!/usr/bin/env python3
"""
Web server for Render deployment.
Keeps the service alive while running the Telegram bot in background.
"""

import threading
import sys
import os
import asyncio
from flask import Flask
from bot.telegram_handler import TelegramHandler
from utils.logger import setup_logger

logger = setup_logger(__name__)

app = Flask(__name__)
bot_handler = None
bot_thread = None


@app.route('/')
def health_check():
    """Health check endpoint for Render."""
    return {
        'status': 'ok',
        'service': 'Telegram Twitter Bot',
        'bot_running': bot_handler is not None and bot_thread.is_alive() if bot_thread else False
    }, 200


@app.route('/health')
def health():
    """Alternative health check endpoint."""
    return {'status': 'healthy'}, 200


def run_bot():
    """Run the Telegram bot in a separate thread."""
    global bot_handler
    try:
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        logger.info("=" * 60)
        logger.info("Bot Cầu Nối Nội Dung Mạng Xã Hội")
        logger.info("=" * 60)
        
        bot_handler = TelegramHandler()
        bot_handler.run()
    except Exception as e:
        logger.error(f"❌ Lỗi nghiêm trọng khi chạy bot: {e}", exc_info=True)
        sys.exit(1)


def main():
    """Main entry point - starts both web server and bot."""
    global bot_thread
    
    # Start bot in background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info("🤖 Bot đã khởi động trong background thread")
    
    # Start Flask web server (this will keep the service alive)
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🌐 Web server đang chạy trên port {port}")
    logger.info("💡 Health check: http://localhost:{}/health".format(port))
    
    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == "__main__":
    main()

