"""
Client gửi tin nhắn Zalo qua tài khoản cá nhân (zlapi).

Sử dụng thư viện zlapi (unofficial) để gửi tin nhắn vào nhóm Zalo
từ tài khoản Zalo cá nhân thông qua Cookie & IMEI.

⚠️ Đây là thư viện KHÔNG CHÍNH THỨC. Có rủi ro bị khóa tài khoản.
"""

import logging

from zlapi import ZaloAPI
from zlapi.models import Message, ThreadType, Mention

from config import ZALO_PHONE, ZALO_IMEI, ZALO_COOKIES

logger = logging.getLogger(__name__)


class ZaloClient:
    """Client gửi tin nhắn Zalo qua tài khoản cá nhân."""

    def __init__(self):
        self._client = None

    def _get_client(self) -> ZaloAPI:
        """Khởi tạo hoặc trả về ZaloAPI client."""
        if self._client is None:
            if not ZALO_PHONE or not ZALO_IMEI or not ZALO_COOKIES:
                raise RuntimeError(
                    "Thiếu thông tin đăng nhập Zalo! "
                    "Hãy điền ZALO_PHONE, ZALO_IMEI, ZALO_COOKIES vào file .env"
                )

            logger.info("Đang kết nối Zalo với SĐT: %s...", ZALO_PHONE[:4] + "***")
            self._client = ZaloAPI(
                ZALO_PHONE,
                "",  # password không cần khi dùng cookie
                imei=ZALO_IMEI,
                cookies=ZALO_COOKIES,
            )
            logger.info("✅ Kết nối Zalo thành công!")

        return self._client

    def send_group_message(self, group_id: str, text: str) -> bool:
        """
        Gửi tin nhắn text vào nhóm Zalo (hỗ trợ tag @all).

        Args:
            group_id: ID của nhóm Zalo.
            text: Nội dung tin nhắn.

        Returns:
            bool: True nếu gửi thành công, False nếu thất bại.
        """
        try:
            client = self._get_client()
            
            # Nếu tin nhắn có chứa @all ở đầu, tự động tạo Mention tag all
            if text.startswith("@all"):
                mention = Mention(uid="-1", offset=0, length=4)
                msg = Message(text=text, mention=mention)
            else:
                msg = Message(text=text)

            client.send(msg, thread_id=group_id, thread_type=ThreadType.GROUP)
            logger.info("✅ Đã gửi tin nhắn (kèm tag @all) vào nhóm: %s", group_id[:15] + "...")
            return True

        except Exception as e:
            logger.error("❌ Lỗi khi gửi tin nhắn vào nhóm: %s", e)
            return False
