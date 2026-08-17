"""
WhatsApp Automation Package - Bot RPA con Patrones de Diseño y Persistencia de Sesión
"""

from .core.bot_facade import WhatsAppBotFacade
from .core.session_manager import SessionManager
from .pages.base_page import BasePage
from .pages.login_page import LoginPage
from .pages.chat_page import ChatPage
from .services.message_builder import (
    MessageBuilder,
    IMessageStrategy,
    TechnicalReportStrategy,
    CustomMessageStrategy,
    create_technical_report_message
)
from .whatsapp_automation import WhatsAppAutomation, send_whatsapp_message

__version__ = "2.0.0"

__all__ = [
    "WhatsAppBotFacade",
    "SessionManager",
    "BasePage",
    "LoginPage",
    "ChatPage",
    "MessageBuilder",
    "IMessageStrategy",
    "TechnicalReportStrategy",
    "CustomMessageStrategy",
    "create_technical_report_message",
    "WhatsAppAutomation",
    "send_whatsapp_message",
]
