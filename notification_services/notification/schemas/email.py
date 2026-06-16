from datetime import UTC, datetime

from config import settings
from notification_services.notification.schemas.base_notification_context import BaseNotificationContext, BaseNotification
from pydantic import Field


def _current_year() -> int:
    return datetime.now(UTC).year


ORDER_STATUS_DEFAULT_LINK = f"{settings.COMPANY_LINK.rstrip('/')}/pl/profile/bids_won"


class EmailContext(BaseNotificationContext):
    logo_url: str = settings.LOGO_URL
    user_uuid: str
    notification_uuid: str
    year: int = Field(default_factory=_current_year)

class EmailNotification(BaseNotification):
    subject: str
    template_name: str
    context: EmailContext

class EmailBidClass(EmailContext):
    bid_amount: int
    auction_date: datetime
    vehicle_title: str
    vehicle_image: str
    auction: str
    lot_id: int

class EmailNewBidPlacedContext(EmailBidClass):
    current_bid: int

class EmailBidLostWonContext(EmailBidClass):
    final_bid: int

class EmailCodeContext(EmailContext):
    code: str
    expire_minutes: int

class EmailResetCodeContext(EmailContext):
    code: str
    expire_minutes: int
    user_email: str


class EmailOrderStatusContext(EmailContext):
    new_order_status: str
    previous_order_status: str
    order_id: int
    vin: str
    vehicle_title: str
    auction: str
    lot_id: int
    link: str = ORDER_STATUS_DEFAULT_LINK


class EmailPasswordResetContext(EmailContext):
    reset_link: str
    expire_hours: int
