"""
Cấu hình cho Zalo Daily Standup Bot.

Bot sử dụng tài khoản Zalo cá nhân (thông qua zlapi) để gửi
tin nhắn nhắc nhở standup vào nhóm Zalo.

Tất cả thông tin nhạy cảm được đọc từ file .env.
"""

import os
import json
from pathlib import Path

from dotenv import load_dotenv

# Tự động đọc biến môi trường từ file .env
load_dotenv()

# ============================================================
# ĐƯỜNG DẪN
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "bot.log"

# ============================================================
# ZALO CÁ NHÂN - Lấy từ extension "Get Cookie & IMEI Zalo"
# ============================================================
ZALO_PHONE = os.getenv("ZALO_PHONE", "")
ZALO_IMEI = os.getenv("ZALO_IMEI", "")

# Cookies có thể là JSON string hoặc dict
_raw_cookies = os.getenv("ZALO_COOKIES", "{}")
try:
    ZALO_COOKIES = json.loads(_raw_cookies) if isinstance(_raw_cookies, str) else _raw_cookies
except json.JSONDecodeError:
    ZALO_COOKIES = {}

# ============================================================
# NHÓM ZALO
# ============================================================
# Group ID của nhóm Zalo muốn gửi tin nhắn
ZALO_GROUP_ID = os.getenv("ZALO_GROUP_ID", "")

# ============================================================
# LỊCH GỬI TIN NHẮN
# ============================================================
STANDUP_HOUR = int(os.getenv("STANDUP_HOUR", "10"))
STANDUP_MINUTE = int(os.getenv("STANDUP_MINUTE", "24"))
TIMEZONE = os.getenv("TIMEZONE", "Asia/Ho_Chi_Minh")

# ============================================================
# NỘI DUNG TIN NHẮN
# ============================================================
STANDUP_MESSAGE = """@all ⏰ DAILY STANDUP REMINDER ⏰

Chào cả team! Đã đến giờ Daily Standup hằng ngày!
Mọi người vui lòng cập nhật nhanh 3 thông tin sau nhé:

1. 🟢 Hôm qua bạn đã hoàn thành gì?
2. 🟡 Hôm nay bạn dự định làm gì?
3. 🔴 Có blocker / khó khăn gì không?

Chúc cả team một ngày làm việc hiệu quả! 🚀"""
