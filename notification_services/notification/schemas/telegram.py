from typing import Optional

from notification_services.notification.schemas.base_notification_context import BaseNotificationContext, BaseNotification


class TelegramContext(BaseNotificationContext):
    notification_uuid: str


class TelegramNotification(BaseNotification):
    message: str
    context: TelegramContext


class TelegramBidNotification(TelegramContext):
    is_bid_up: bool = False
    lot_id: int
    bid_amount: int
    user_email: str | None = None
    vehicle_title: Optional[str] = None
    auction: Optional[str] = None


class TelegramOrderStatusNotification(TelegramContext):
    new_order_status: str
    previous_order_status: str
    order_id: int
    vin: str
    vehicle_title: str
    auction: str
    lot_id: int
    user_email: Optional[str] = None
