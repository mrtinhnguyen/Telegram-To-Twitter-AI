# 🌉 Social Content Bridge Bot

A Telegram bot that automatically republishes content to your Telegram channel and Twitter. Features AI-powered text processing, translation, and optimization for social media.

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=flat&logo=telegram&logoColor=white)
![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=flat&logo=twitter&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white)

## ✨ Features

- 🤖 **AI Processing**: Uses GPT-4o mini to improve text quality
- 🌍 **Auto Translation**: Translates Russian to English automatically
- ✂️ **Smart Formatting**: Creates full and short (≤280 chars) versions
- 🏷️ **Hashtags**: Automatically adds relevant hashtags
- 📸 **Image Support**: Handles images with optimization
- 🎨 **Caption Generation**: Creates captions for image-only posts
- 🚀 **Auto Publishing**: One message → Multiple platforms instantly

## 📋 Prerequisites

- Python 3.9 or higher
- Telegram Bot Token
- Twitter API credentials (API v2 with OAuth 1.0a)
- OpenAI API key
- A Telegram channel where you're an admin

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/social-content-bridge.git
cd social-content-bridge
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or using a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHANNEL_ID=@your_channel_username
AUTHORIZED_USER_ID=your_telegram_user_id
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
TWITTER_BEARER_TOKEN=your_bearer_token
OPENAI_API_KEY=your_openai_key
```

## 🔑 Getting API Keys

### Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token provided
5. **Get your User ID**: Send any message to [@userinfobot](https://t.me/userinfobot) to get your user ID

### Telegram Channel Setup

1. Create a channel or use existing one
2. Add your bot as an administrator with "Post messages" permission
3. Get your channel username (e.g., `@my_channel`)
   - Or use channel ID (e.g., `-1001234567890`)

### Twitter API Credentials

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new project and app
3. Set up OAuth 1.0a in "User authentication settings"
4. Set permissions to "Read and Write"
5. Generate API keys and access tokens
6. Copy all credentials:
   - API Key (Consumer Key)
   - API Secret (Consumer Secret)
   - Access Token
   - Access Token Secret
   - Bearer Token

### OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign up or log in
3. Go to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key (shown only once!)
6. Add billing info and credits ($5-10 recommended)

**Cost estimate**: ~$0.0004 per message = ~$0.12/month for 10 posts/day

## 🚀 Usage

### Start the bot

```bash
python main.py
```

You should see:

```
============================================================
Social Content Bridge Bot
============================================================
🚀 Starting bot...
📢 Channel: @your_channel
👤 Authorized user: 123456789
```

### Using the bot

1. Open your bot in Telegram
2. Send `/start` to see welcome message
3. Forward any message to the bot (text and/or image)
4. Bot will automatically:
   - Process text with AI
   - Translate if Russian
   - Improve style
   - Create short version
   - Publish to Telegram channel (full version)
   - Publish to Twitter (short version ≤280 chars)

### Commands

- `/start` - Show welcome message
- `/help` - Show help and features

### Supported Content

✅ **Supported:**
- Text messages (any language, Russian → English)
- Messages with images (uses first image)
- Image-only messages (AI generates caption)

❌ **Not supported:**
- Videos
- Multiple images (only first is used)
- Audio files
- Documents

## 📁 Project Structure

```
social-content-bridge/
├── bot/
│   ├── __init__.py
│   ├── telegram_handler.py     # Main bot handler
│   ├── ai_processor.py         # OpenAI integration
│   ├── telegram_publisher.py   # Telegram channel publisher
│   └── twitter_publisher.py    # Twitter publisher
├── config/
│   ├── __init__.py
│   └── settings.py             # Configuration management
├── utils/
│   ├── __init__.py
│   ├── image_handler.py        # Image processing
│   └── logger.py               # Logging setup
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── main.py                     # Entry point
└── README.md                   # This file
```

## 🔒 Security

- Never commit `.env` file to Git
- Keep your API keys secure
- Only authorized user (your Telegram ID) can use the bot
- Set spending limits on OpenAI account
- Regularly rotate API keys

## 🐛 Troubleshooting

### Bot doesn't respond

- Check if bot is running: `python main.py`
- Verify bot token is correct in `.env`
- Make sure your user ID is correct
- Check bot logs for errors

### "Missing required environment variables"

- Make sure `.env` file exists
- Verify all required variables are filled in
- No spaces around `=` in `.env` file

### Twitter publishing fails

- Verify Twitter API credentials
- Check if app has "Read and Write" permissions
- Ensure access tokens are for OAuth 1.0a (not OAuth 2.0)
- Check Twitter API usage limits

### Telegram channel publishing fails

- Verify bot is admin in the channel
- Check if bot has "Post messages" permission
- Use channel username with @ or channel ID

### OpenAI errors

- Check API key is valid
- Verify you have credits in your account
- Check OpenAI API status page

## 💰 Cost Estimation

**OpenAI GPT-4o mini:**
- ~$0.0004 per message
- 10 posts/day = $0.12/month
- 100 posts/day = $1.20/month

**Twitter API:**
- Free tier available
- Check [Twitter API pricing](https://developer.twitter.com/en/docs/twitter-api)

**Telegram:**
- Completely free!

## 🔄 Updates and Maintenance

### Update dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Check logs

Logs are printed to console with color coding:
- 🟢 INFO - Normal operations
- 🟡 WARNING - Non-critical issues
- 🔴 ERROR - Problems that need attention

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Review bot logs for error messages
3. Open an issue on GitHub with details

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [tweepy](https://github.com/tweepy/tweepy) - Twitter API wrapper
- [OpenAI](https://openai.com) - AI processing

---

Made with ❤️ for seamless cross-platform content sharing
