# 🐦 Hướng Dẫn Cấu Hình Twitter API OAuth 1.0a

Hướng dẫn chi tiết để cấu hình Twitter API với OAuth 1.0a cho bot này, đặc biệt khi **không có website callback URL**.

## 📋 Bước 1: Tạo Twitter Developer Account

1. Truy cập [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Đăng nhập với tài khoản Twitter của bạn
3. Nếu chưa có Developer Account:
   - Click "Sign up" hoặc "Apply"
   - Điền thông tin và mô tả use case (ví dụ: "Personal content automation bot")
   - Xác thực số điện thoại
   - Chờ phê duyệt (thường vài phút đến vài giờ)

## 🔑 Bước 2: Tạo App và Project

1. Vào [Developer Portal Dashboard](https://developer.twitter.com/en/portal/dashboard)
2. Click **"Create Project"** hoặc **"+ Add App"**
3. Điền thông tin:
   - **Project name**: Tên dự án của bạn (ví dụ: "Content Bridge Bot")
   - **Use case**: Chọn "Making a bot" hoặc "Exploring the API"
   - **App name**: Tên app (ví dụ: "content-bridge-bot")
4. Click **"Create"**

## ⚙️ Bước 3: Cấu Hình User Authentication Settings

### 3.1. Vào Settings

1. Trong Developer Portal, chọn **Project** của bạn
2. Chọn **App** bạn vừa tạo
3. Click tab **"Settings"** (hoặc **"User authentication settings"**)

### 3.2. Cấu Hình OAuth 1.0a (KHÔNG CẦN CALLBACK URL)

1. Tìm phần **"User authentication settings"**
2. Click **"Set up"** hoặc **"Edit"**

3. **App permissions**: Chọn **"Read and Write"** (quan trọng!)
   - Đây là quyền cần thiết để đăng tweet

4. **Type of App**: Chọn **"Native App"** hoặc **"Web App"**
   - **Native App**: Không cần callback URL (khuyến nghị cho bot này)
   - **Web App**: Cần callback URL (không phù hợp nếu không có website)

5. **Callback URI / Redirect URL**:
   - Nếu chọn **"Native App"**: Để trống hoặc nhập `http://localhost` hoặc `http://127.0.0.1`
   - Nếu chọn **"Web App"**: Nhập `http://localhost` hoặc `http://127.0.0.1/callback`
   - ⚠️ **Lưu ý**: Bot này không thực sự sử dụng callback URL, nên bạn có thể dùng bất kỳ URL nào

6. **Website URL** (nếu có):
   - Nếu không có website: Nhập `http://localhost` hoặc để trống
   - Nếu có website: Nhập URL của bạn

7. Click **"Save"** hoặc **"Update"**

### 3.3. Lưu ý Quan Trọng

- ✅ **App permissions** PHẢI là **"Read and Write"** (không phải "Read only")
- ✅ Sau khi thay đổi permissions, bạn **PHẢI tạo lại Access Tokens**
- ✅ Callback URL không quan trọng cho bot này vì chúng ta dùng OAuth 1.0a với pre-authorized tokens

## 🔐 Bước 4: Lấy API Keys và Tokens

1. Vẫn trong tab **"Settings"** của app
2. Cuộn xuống phần **"Keys and tokens"**

### 4.1. API Key và API Secret (Consumer Keys)

1. Tìm **"Consumer Keys"**
2. Click **"Regenerate"** nếu cần (hoặc dùng keys hiện có)
3. Copy:
   - **API Key** (Consumer Key) → `TWITTER_API_KEY` trong `.env`
   - **API Secret** (Consumer Secret) → `TWITTER_API_SECRET` trong `.env`
4. ⚠️ **Lưu ý**: API Secret chỉ hiển thị một lần! Copy ngay.

### 4.2. Access Token và Access Token Secret

1. Tìm **"Access Token and Secret"**
2. ⚠️ **QUAN TRỌNG**: Nếu bạn vừa thay đổi App permissions, click **"Regenerate"**
3. Copy:
   - **Access Token** → `TWITTER_ACCESS_TOKEN` trong `.env`
   - **Access Token Secret** → `TWITTER_ACCESS_SECRET` trong `.env`
4. ⚠️ **Lưu ý**: Tokens chỉ hiển thị một lần! Copy ngay.

### 4.3. Bearer Token

1. Tìm **"Bearer Token"**
2. Click **"Regenerate"** nếu cần
3. Copy **Bearer Token** → `TWITTER_BEARER_TOKEN` trong `.env`

## 📝 Bước 5: Cập Nhật File .env

Mở file `.env` và cập nhật các giá trị:

```env
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_SECRET=your_access_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

⚠️ **Lưu ý**:
- Không có khoảng trắng quanh dấu `=`
- Không có dấu ngoặc kép (trừ khi giá trị có khoảng trắng)
- Mỗi giá trị trên một dòng riêng

## ✅ Bước 6: Kiểm Tra Cấu Hình

1. Khởi động lại bot:
   ```bash
   python main.py
   ```

2. Kiểm tra log khi khởi động:
   - Nếu thấy: `✅ Kết nối Twitter thành công: @your_username` → Thành công!
   - Nếu thấy: `❌ Lỗi quyền OAuth!` → Xem phần Troubleshooting bên dưới

3. Test bằng cách gửi một tin nhắn cho bot

## 🔧 Troubleshooting

### Lỗi: "403 Forbidden - oauth1 app permissions"

**Nguyên nhân**: App permissions chưa đúng hoặc Access Tokens chưa được tạo lại.

**Giải pháp**:
1. Vào Twitter Developer Portal
2. Chọn app → Settings → User authentication settings
3. Đảm bảo **App permissions** là **"Read and Write"**
4. Click **"Save"**
5. Vào **"Keys and tokens"** → **"Access Token and Secret"**
6. Click **"Regenerate"** để tạo tokens mới
7. Copy tokens mới vào file `.env`
8. Khởi động lại bot

### Lỗi: "Invalid or expired token"

**Nguyên nhân**: Access Tokens đã hết hạn hoặc không hợp lệ.

**Giải pháp**:
1. Tạo lại Access Token và Access Token Secret
2. Cập nhật file `.env`
3. Khởi động lại bot

### Lỗi: "Callback URL mismatch"

**Nguyên nhân**: Callback URL trong settings không khớp (nhưng bot này không cần callback thực sự).

**Giải pháp**:
1. Vào Settings → User authentication settings
2. Đảm bảo Type of App là **"Native App"**
3. Callback URL: `http://localhost` hoặc để trống
4. Click **"Save"**

### Không thấy "User authentication settings"

**Nguyên nhân**: App chưa được cấu hình đúng.

**Giải pháp**:
1. Đảm bảo bạn đã tạo Project và App
2. Chọn đúng App trong danh sách
3. Nếu vẫn không thấy, thử tạo App mới

## 📚 Tài Liệu Tham Khảo

- [Twitter API v2 Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [OAuth 1.0a Guide](https://developer.twitter.com/en/docs/authentication/oauth-1-0a)
- [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)

## ⚠️ Lưu Ý Quan Trọng

1. **App permissions** PHẢI là **"Read and Write"** để có thể đăng tweet
2. Sau khi thay đổi permissions, **PHẢI tạo lại Access Tokens**
3. Không chia sẻ API keys và tokens với ai
4. Không commit file `.env` lên Git
5. Nếu tokens bị lộ, hãy regenerate ngay lập tức

---

**Cần giúp đỡ?** Kiểm tra log của bot để xem thông báo lỗi chi tiết.

