"""
WhatsApp Automation Root Package Re-export
"""

from .whatsapp_automation import (
    WhatsAppBotFacade,
    SessionManager,
    BasePage,
    LoginPage,
    ChatPage,
    MessageBuilder,
    IMessageStrategy,
    MerzaDesignPatternsStrategy,
    CustomMessageStrategy,
    create_merza_pattern_message,
    WhatsAppAutomation,
    send_whatsapp_message,
    __version__,
)

__all__ = [
    "WhatsAppBotFacade",
    "SessionManager",
    "BasePage",
    "LoginPage",
    "ChatPage",
    "MessageBuilder",
    "IMessageStrategy",
    "MerzaDesignPatternsStrategy",
    "CustomMessageStrategy",
    "create_merza_pattern_message",
    "WhatsAppAutomation",
    "send_whatsapp_message",
    "__version__",
]
