import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader
import aiosmtplib
from config import settings
from datetime import UTC, datetime

from notification_services.notification.schemas.email import (
    EmailBidLostWonContext,
    EmailCodeContext,
    EmailNewBidPlacedContext,
    EmailNotification,
    EmailOrderStatusContext,
    EmailResetCodeContext,
)
from utils import BASE_DIR


async def send_templated_email(data:EmailNotification):
    env = Environment(loader=FileSystemLoader(BASE_DIR / 'src/templates'))
    template = env.get_template(data.template_name)
    html_content = template.render(data.context.model_dump())

    msg = MIMEMultipart("alternative")
    msg['From'] = settings.SENDER_EMAIL
    msg['To'] = data.recipient
    msg['Subject'] = data.subject
    msg.attach(MIMEText(html_content, "html"))

    try:
        await aiosmtplib.send(
            msg,
            hostname=settings.SMPT_SERVER,
            port=settings.SMPT_PORT,
            start_tls=True,
            username=settings.EMAIL_USER,
            password=settings.EMAIL_PASSWORD,
        )
        print("Email sent successfully")
    except Exception as e:
        print(f"Error while sending email: {e}")


async def send_all_template_previews(recipient: str) -> None:
    auction_date = datetime(2026, 6, 8, 14, 30, tzinfo=UTC)
    common = {"user_uuid": "preview-user", "notification_uuid": "preview-notification"}

    previews: list[tuple[str, str, EmailCodeContext | EmailResetCodeContext | EmailBidLostWonContext | EmailNewBidPlacedContext | EmailOrderStatusContext]] = [
        (
            "code_email.html",
            "[Preview] Your verification code",
            EmailCodeContext(**common, code="123456", expire_minutes=10),
        ),
        (
            "auth_reset_password.html",
            "[Preview] Reset password code",
            EmailResetCodeContext(**common, code="654321", expire_minutes=10, user_email=recipient),
        ),
        (
            "new_bid_placed.html",
            "[Preview] New bid placed",
            EmailNewBidPlacedContext(
                **common,
                bid_amount=5200,
                current_bid=4800,
                auction_date=auction_date,
                vehicle_title="2020 BMW X5 xDrive40i",
                vehicle_image="https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400",
                auction="Copart",
                lot_id=42187,
            ),
        ),
        (
            "bid_won.html",
            "[Preview] Congratulations! You won the auction",
            EmailBidLostWonContext(
                **common,
                bid_amount=5200,
                final_bid=5500,
                auction_date=auction_date,
                vehicle_title="2020 BMW X5 xDrive40i",
                vehicle_image="https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400",
                auction="Copart",
                lot_id=42187,
            ),
        ),
        (
            "bid_lost.html",
            "[Preview] Update on your recent bid",
            EmailBidLostWonContext(
                **common,
                bid_amount=5000,
                final_bid=5500,
                auction_date=auction_date,
                vehicle_title="2020 BMW X5 xDrive40i",
                vehicle_image="https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400",
                auction="Copart",
                lot_id=42187,
            ),
        ),
        (
            "order_status_updated.html",
            "[Preview] Your order status has been updated",
            EmailOrderStatusContext(
                **common,
                new_order_status="Shipped",
                previous_order_status="Processing",
                order_id=9901,
                vin="WBAJB7C50KB123456",
                vehicle_title="2020 BMW X5 xDrive40i",
                auction="Copart",
                lot_id=42187,
            ),
        ),
    ]

    for template_name, subject, context in previews:
        print(f"Sending {template_name}...")
        await send_templated_email(
            EmailNotification(
                recipient=recipient,
                subject=subject,
                template_name=template_name,
                context=context,
            )
        )


if __name__ == "__main__":
    asyncio.run(send_all_template_previews(settings.SENDER_EMAIL))
