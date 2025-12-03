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


def run_flask():
    """Run Flask web server in a separate thread."""
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🌐 Web server đang chạy trên port {port}")
    logger.info("💡 Health check: http://localhost:{}/health".format(port))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)


def main():
    """Main entry point - starts both web server and bot."""
    global bot_handler, bot_thread
    
    # Start Flask web server in background thread (to keep service alive)
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("🌐 Flask server đã khởi động trong background thread")
    
    # Run bot in main thread (needed for signal handlers)
    try:
        logger.info("=" * 60)
        logger.info("Bot Cầu Nối Nội Dung Mạng Xã Hội")
        logger.info("=" * 60)
        
        bot_handler = TelegramHandler()
        bot_handler.run()
    except KeyboardInterrupt:
        logger.info("\n👋 Bot đã dừng bởi người dùng")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Lỗi nghiêm trọng khi chạy bot: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

