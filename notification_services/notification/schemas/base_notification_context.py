from config import settings
from pydantic import BaseModel


class BaseNotificationContext(BaseModel):
    company_name: str = settings.COMPANY_NAME.upper()
    link: str = f'https://{settings.COMPANY_LINK}'

class BaseNotification(BaseModel):
    recipient: str
    context: BaseNotificationContext
