# 🚀 Hướng Dẫn Deploy Bot Lên Render

Hướng dẫn chi tiết để deploy Telegram bot lên Render để chạy 24/7.

## 📋 Yêu Cầu

- Tài khoản [Render](https://render.com) (miễn phí)
- GitHub repository chứa code bot
- Tất cả API keys đã được cấu hình

## 🔧 Bước 1: Chuẩn Bị Repository

### 1.1. Đảm Bảo Code Đã Commit Lên GitHub

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 1.2. Kiểm Tra File Cần Thiết

Đảm bảo các file sau có trong repository:
- ✅ `main.py` - Entry point
- ✅ `requirements.txt` - Dependencies
- ✅ `render.yaml` - Render configuration (sẽ tạo ở bước sau)
- ✅ `.env.example` - Template cho environment variables

## 📝 Bước 2: Tạo File Cấu Hình Render

File `render.yaml` đã được tạo sẵn trong project. Bot sử dụng **Web Service** (thay vì Background Worker) để có thể dùng free tier.

**Giải pháp**: Tạo một web server đơn giản (Flask) để giữ service hoạt động, đồng thời chạy bot trong background thread.

File `render.yaml`:
```yaml
services:
  - type: web
    name: telegram-twitter-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python web_server.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
    plan: free
```

**Lưu ý**: 
- Sử dụng `web_server.py` thay vì `main.py`
- File `web_server.py` đã được tạo sẵn, chạy cả Flask server và bot

## 🌐 Bước 3: Tạo Service Trên Render

### 3.1. Đăng Nhập Render

1. Truy cập [Render Dashboard](https://dashboard.render.com)
2. Đăng nhập bằng GitHub account (khuyến nghị)

### 3.2. Tạo New Web Service

1. Click **"New +"** → **"Web Service"**
   - ✅ **Lưu ý**: Chọn "Web Service" để có thể dùng free tier
   - Bot sẽ chạy trong background thread, web server chỉ để giữ service hoạt động

2. **Connect Repository**:
   - Chọn GitHub repository chứa code bot
   - Chọn branch (thường là `main` hoặc `master`)

3. **Configure Service**:
   - **Name**: `telegram-twitter-bot` (hoặc tên bạn muốn)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python web_server.py` ⚠️ **Quan trọng**: Dùng `web_server.py` không phải `main.py`
   - **Plan**: Chọn **Free** (có thể sleep sau 15 phút) hoặc **Starter** ($7/tháng - chạy 24/7)

### 3.3. Cấu Hình Environment Variables

Trong phần **"Environment"**, thêm tất cả các biến từ file `.env`:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHANNEL_ID=@your_channel_username
AUTHORIZED_USER_ID=your_telegram_user_id
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
TWITTER_BEARER_TOKEN=your_bearer_token
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini
LOG_LEVEL=INFO
```

⚠️ **Lưu ý quan trọng**:
- Không có khoảng trắng quanh dấu `=`
- Mỗi biến trên một dòng riêng
- Không commit file `.env` lên Git (đã có trong `.gitignore`)

### 3.4. Advanced Settings (Tùy Chọn)

1. **Auto-Deploy**: Bật để tự động deploy khi push code mới
2. **Health Check**: Không cần (bot không có HTTP endpoint)
3. **Docker**: Không cần (dùng Python trực tiếp)

## 🚀 Bước 4: Deploy

1. Click **"Create Background Worker"**
2. Render sẽ tự động:
   - Clone repository
   - Install dependencies từ `requirements.txt`
   - Chạy `python main.py`
3. Xem logs trong tab **"Logs"** để kiểm tra bot đã khởi động thành công

## ✅ Bước 5: Kiểm Tra Bot Hoạt Động

1. Vào tab **"Logs"** trên Render dashboard
2. Kiểm tra log có hiển thị:
   ```
   ============================================================
   Bot Cầu Nối Nội Dung Mạng Xã Hội
   ============================================================
   🚀 Đang khởi động bot...
   📢 Kênh: @your_channel
   👤 Người dùng được ủy quyền: 123456789
   ✅ Kết nối Twitter thành công: @your_username
   ```

3. Mở Telegram và gửi `/start` cho bot
4. Nếu bot phản hồi → Deploy thành công! 🎉

## 🔧 Troubleshooting

### Bot Không Khởi Động

**Kiểm tra**:
1. Logs trên Render dashboard
2. Environment variables đã được set đúng chưa
3. `requirements.txt` có đầy đủ dependencies không

**Lỗi thường gặp**:
- `ModuleNotFoundError`: Kiểm tra `requirements.txt`
- `Missing required environment variables`: Kiểm tra tất cả env vars đã được set
- `Connection refused`: Bot token hoặc API keys sai

### Bot Tự Động Dừng

**Nguyên nhân**: Render free tier có thể sleep sau 15 phút không hoạt động.

**Giải pháp**:
1. Upgrade lên **Starter plan** ($7/tháng) để chạy 24/7
2. Hoặc dùng service như [UptimeRobot](https://uptimerobot.com) để ping bot định kỳ (nhưng bot này không có HTTP endpoint nên không áp dụng được)

### Lỗi "Port Already in Use"

**Nguyên nhân**: Đã chọn "Web Service" thay vì "Background Worker".

**Giải pháp**: 
- Xóa service hiện tại
- Tạo lại với type "Background Worker"

## 💰 Chi Phí

### Free Tier
- ✅ Miễn phí
- ⚠️ Service có thể sleep sau 15 phút không hoạt động
- ⚠️ Không đảm bảo chạy 24/7

### Starter Plan ($7/tháng)
- ✅ Chạy 24/7 không sleep
- ✅ 512 MB RAM
- ✅ Đủ cho bot nhỏ đến vừa

### Standard Plan ($25/tháng)
- ✅ Chạy 24/7
- ✅ 2 GB RAM
- ✅ Phù hợp cho bot lớn hoặc nhiều bot

## 📊 Monitoring

### Xem Logs
1. Vào Render dashboard
2. Chọn service của bạn
3. Tab **"Logs"** để xem real-time logs

### Health Check
Bot này không có HTTP endpoint nên không thể dùng health check. Thay vào đó:
- Kiểm tra logs thường xuyên
- Test bot bằng cách gửi tin nhắn
- Monitor qua Telegram (bot có phản hồi không)

## 🔄 Update Bot

### Cách 1: Auto-Deploy (Khuyến Nghị)

1. Push code mới lên GitHub:
   ```bash
   git add .
   git commit -m "Update bot"
   git push origin main
   ```

2. Render sẽ tự động deploy nếu đã bật "Auto-Deploy"

### Cách 2: Manual Deploy

1. Vào Render dashboard
2. Chọn service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**

## 🔐 Bảo Mật

### Không Commit Secrets

✅ **Đúng**:
- File `.env` đã có trong `.gitignore`
- Chỉ set environment variables trên Render dashboard

❌ **Sai**:
- Commit file `.env` lên Git
- Hardcode API keys trong code

### Rotate Keys Định Kỳ

- Thay đổi API keys mỗi 3-6 tháng
- Regenerate ngay nếu phát hiện keys bị lộ

## 📚 Tài Liệu Tham Khảo

- [Render Documentation](https://render.com/docs)
- [Render Python Guide](https://render.com/docs/deploy-python)
- [Background Workers on Render](https://render.com/docs/background-workers)

## ⚠️ Lưu Ý Quan Trọng

1. **Free Tier có thể sleep**: Bot có thể không hoạt động liên tục trên free tier
2. **Logs bị giới hạn**: Free tier chỉ giữ logs 7 ngày
3. **Không có persistent storage**: File tạm sẽ bị xóa khi restart
4. **Rate limits**: Tuân thủ rate limits của Telegram và Twitter API

---

**Cần giúp đỡ?** Kiểm tra logs trên Render dashboard hoặc mở issue trên GitHub.

