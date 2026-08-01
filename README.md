# 🤖 Zalo Daily Standup Bot (24/7 Free Hosting)

Bot tự động gửi tin nhắn nhắc nhở **Daily Standup** vào nhóm Zalo mỗi buổi sáng (Thứ 2 → Thứ 7 lúc 9:00 AM).

Sử dụng **tài khoản Zalo cá nhân** (thông qua `zlapi`), tích hợp **Flask Web Server** để deploy 24/7 miễn phí lên **Render** kết hợp **UptimeRobot**.

---

## ⚠️ Cảnh báo

> **QUAN TRỌNG:** Bot sử dụng thư viện `zlapi` — API **KHÔNG CHÍNH THỨC** cho Zalo cá nhân.
>
> - Nên dùng **tài khoản Zalo phụ** làm bot
> - Không chia sẻ file `.env` chứa Cookie và IMEI

---

## 📁 Cấu trúc Project

```
zalo-standup-bot/
├── bot.py              # 🚀 Entry point chính (Scheduler + Flask Health Check)
├── config.py           # ⚙️ Cấu hình (đọc từ biến môi trường / .env)
├── zalo_client.py      # 📨 Client gửi tin nhắn (zlapi)
├── requirements.txt    # 📦 Dependencies (zlapi, schedule, flask, dotenv)
├── .env.example        # 📋 Template biến môi trường
├── .gitignore          # 🚫 Files không commit
└── README.md           # 📖 Hướng dẫn
```

---

## 🌐 Hướng dẫn chạy 24/7 Miễn phí (Render + UptimeRobot)

### Bước 1: Chuẩn bị Git Repository

1. Đảm bảo file `.gitignore` có các dòng sau:
   ```plaintext
   venv/
   .env
   logs/
   __pycache__/
   ```
2. Đẩy dự án lên GitHub (tài khoản GitHub cá nhân, chọn **Private** hoặc **Public**):
   ```bash
   git init
   git add .
   git commit -m "Zalo standup bot 24/7"
   git branch -M main
   git remote add origin https://github.com/pieupieu16/zalo-standup-bot
   git push -u origin main
   ```

---

### Bước 2: Lấy Cookie & IMEI từ Zalo Web

1. Cài extension **"Get Cookie & IMEI Zalo"** trên Chrome / Cốc Cốc.
2. Đăng nhập [chat.zalo.me](https://chat.zalo.me).
3. Nhấn vào extension để lấy `ZALO_COOKIES` và `ZALO_IMEI`.
4. Lấy `ZALO_GROUP_ID` của nhóm Zalo bạn muốn gửi.

zpw_sek=Q11b.461705189.a0.oPy2xHjM80oO8wLXN2mWUWOEHH5V5W8SI4X9FJ1yL1LF5LOJA6SB4Gj7GoWi4HrO02qMwrJ7dZpnBPow4KOWUW

6e7bfc76-74f3-43a7-b852-c23fa949d459-c33c588009b95570bda142ca18d363d2
---
xp1z2fsgaxl51to2nden
### Bước 3: Triển khai Web Service trên Render (Free $0/tháng)

1. Truy cập [render.com](https://render.com) và đăng nhập bằng GitHub.
2. Chọn **New +** → **Web Service**.
3. Chọn Repository `zalo-standup-bot` vừa đẩy lên GitHub.
4. Cấu hình các thông số:
   - **Name:** `zalo-standup-bot`
   - **Region:** Singapore (khuyến nghị cho tốc độ tối ưu về Việt Nam)
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
   - **Instance Type:** `Free`
5. Trong mục **Environment Variables**, thêm các biến môi trường sau:
   - `ZALO_PHONE`: Số điện thoại Zalo của bạn (VD: `0901234567`)
   - `ZALO_IMEI`: Chuỗi IMEI lấy ở Bước 2
   - `ZALO_COOKIES`: Chuỗi JSON Cookie lấy ở Bước 2 (VD: `{"zpw_sek":"..."}`)
   - `ZALO_GROUP_ID`: Group ID nhóm Zalo
   - `STANDUP_HOUR`: `10`
   - `STANDUP_MINUTE`: `9`
   - `TIMEZONE`: `Asia/Ho_Chi_Minh`
6. Nhấn **Create Web Service**. Render sẽ bắt đầu build và khởi động bot.
7. Sau khi thành công, copy địa chỉ URL công khai do Render cấp (VD: `https://zalo-standup-bot-xxxx.onrender.com`).

---

### Bước 4: Cấu hình UptimeRobot để giữ Bot thức 24/7

Do Render Free Tier sẽ tự động Sleep nếu không có lượt truy cập sau 15 phút, ta dùng **UptimeRobot** để gửi ping giữ cho bot luôn "thức":

1. Đăng ký tài khoản miễn phí tại [uptimerobot.com](https://uptimerobot.com).
2. Bấm **Add New Monitor**:
   - **Monitor Type:** `HTTP(s)`
   - **Friendly Name:** `Zalo Bot Keep Alive`
   - **URL (or IP):** Dán URL Render của bạn (VD: `https://zalo-standup-bot-xxxx.onrender.com`)
   - **Monitoring Interval:** `5 minutes` (mỗi 5 phút 1 lần)
3. Nhấn **Create Monitor**.

👉 **Kết quả:** UptimeRobot sẽ tự động gõ vào Web Server 5 phút/lần. Bot của bạn trên Render sẽ **chạy 24/7 liên tục**, không bao giờ bị tắt máy, và sẽ tự động gửi tin nhắn nhắc nhở Daily Standup đúng **09:00 AM** mỗi ngày từ Thứ 2 đến Thứ 6.

---

## 💻 Chạy thử cục bộ trên máy tính (Local)

```bash
# Cài đặt
pip install -r requirements.txt

# Test gửi ngay 1 lần
python bot.py --send-now

# Chạy Scheduler + Health Check Server cục bộ
python bot.py --schedule
```

---

## 📝 License

MIT License - Tự do sử dụng và tùy chỉnh.
