"""
🤖 Zalo Daily Standup Bot - Main Entry Point

Bot gửi tin nhắn nhắc nhở Daily Standup vào nhóm Zalo
lúc 9:00 sáng hàng ngày (Thứ 2 → Thứ 6).

Tích hợp Web Server (Flask) để phục vụ Health Check khi deploy lên Render/Fly.io
và giữ bot hoạt động 24/7 với UptimeRobot.

Cách sử dụng:
    # Gửi 1 lần ngay lập tức (test)
    python bot.py --send-now

    # Chạy scheduler + Web Server liên tục (production / Render)
    python bot.py --schedule
"""

import argparse
import logging
import os
import sys
import threading
import time

from flask import Flask
import schedule

from config import (
    STANDUP_MESSAGE,
    STANDUP_HOUR,
    STANDUP_MINUTE,
    TIMEZONE,
    ZALO_GROUP_ID,
    LOG_DIR,
    LOG_FILE,
)
from zalo_client import ZaloClient

# ============================================================
# Logging setup
# ============================================================
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)
logger = logging.getLogger("standup-bot")

# ============================================================
# Web Server (Health Check cho Render / UptimeRobot)
# ============================================================
app = Flask(__name__)


@app.route("/")
def health_check():
    return "Zalo Standup Bot đang chạy 24/7!", 200


def start_web_server():
    port = int(os.getenv("PORT", "5000"))
    logger.info("🌐 Web Server Health Check đang chạy tại port %d", port)
    # Tắt log thừa từ werkzeug trong production
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    app.run(host="0.0.0.0", port=port)


# ============================================================
# Core function
# ============================================================
def send_standup_reminder():
    """Gửi tin nhắn Daily Standup vào nhóm Zalo."""
    logger.info("=" * 50)
    logger.info("🚀 Bắt đầu gửi Daily Standup Reminder")
    logger.info("=" * 50)

    if not ZALO_GROUP_ID:
        logger.error(
            "❌ Chưa cấu hình ZALO_GROUP_ID! "
            "Hãy thêm group_id vào file .env"
        )
        return

    client = ZaloClient()
    success = client.send_group_message(
        group_id=ZALO_GROUP_ID,
        text=STANDUP_MESSAGE,
    )

    if success:
        logger.info("📊 Kết quả: Gửi thành công!")
    else:
        logger.error("📊 Kết quả: Gửi thất bại!")

    logger.info("=" * 50)


# ============================================================
# Scheduler
# ============================================================
def run_scheduler():
    """Chạy scheduler để tự động gửi tin nhắn theo lịch kèm Web Server."""
    # Chạy Web Server ở thread riêng để Render / UptimeRobot check-in được
    web_thread = threading.Thread(target=start_web_server, daemon=True)
    web_thread.start()

    standup_time = f"{STANDUP_HOUR:02d}:{STANDUP_MINUTE:02d}"

    logger.info("⏰ Bot đã khởi động với scheduler!")
    logger.info("📅 Lịch gửi: %s hàng ngày (Thứ 2 → Thứ 6)", standup_time)
    logger.info("💬 Nhóm: %s", ZALO_GROUP_ID[:15] + "..." if ZALO_GROUP_ID else "⚠️ CHƯA CẤU HÌNH")
    logger.info("🌏 Timezone: %s", TIMEZONE)
    logger.info("-" * 50)

    # Đăng ký lịch cho từng ngày làm việc
    schedule.every().monday.at(standup_time).do(send_standup_reminder)
    schedule.every().tuesday.at(standup_time).do(send_standup_reminder)
    schedule.every().wednesday.at(standup_time).do(send_standup_reminder)
    schedule.every().thursday.at(standup_time).do(send_standup_reminder)
    schedule.every().friday.at(standup_time).do(send_standup_reminder)

    logger.info("✅ Scheduler đã sẵn sàng. Đang chờ đến giờ gửi...")
    logger.info("   Nhấn Ctrl+C để dừng bot.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(30)
    except KeyboardInterrupt:
        logger.info("\n🛑 Bot đã dừng bởi người dùng.")


# ============================================================
# CLI Entry Point
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="🤖 Zalo Daily Standup Bot (tài khoản cá nhân)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  python bot.py --send-now     Gửi tin nhắn ngay (test)
  python bot.py --schedule     Chạy scheduler + Web Server 24/7
        """,
    )

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--send-now",
        action="store_true",
        help="Gửi tin nhắn Daily Standup ngay lập tức",
    )
    group.add_argument(
        "--schedule",
        action="store_true",
        help="Chạy scheduler tự động gửi theo lịch (kèm Web Server 24/7)",
    )

    args = parser.parse_args()

    if args.send_now:
        logger.info("🔧 Chế độ: Gửi ngay")
        send_standup_reminder()
    else:
        # Khi chạy `python bot.py` (mặc định trên Render), tự động bật scheduler & web server
        logger.info("🔧 Chế độ: Scheduler & Web Server (Render 24/7)")
        run_scheduler()


if __name__ == "__main__":
    main()
