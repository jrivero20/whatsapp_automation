"""
Suite de Pruebas Unitarias para el Bot de WhatsApp RPA
Valida el funcionamiento de los Patrones de Diseño (POM, Facade, Singleton, Builder) y formateo.
"""

import unittest
import os
import sys

# Agregar path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from whatsapp_automation import (
    WhatsAppBotFacade,
    SessionManager,
    BasePage,
    LoginPage,
    ChatPage,
    MessageBuilder,
    TechnicalReportStrategy,
    CustomMessageStrategy,
    create_technical_report_message
)


class TestMessageBuilderAndStrategy(unittest.TestCase):
    """Pruebas para el Patrón Builder y Strategy."""

    def test_technical_report_strategy_output(self):
        msg = create_technical_report_message(recipient="Merza", developer="Jose Rivero")
        self.assertIn("Merza", msg)
        self.assertIn("Jose Rivero", msg)
        self.assertIn("https://github.com/jrivero20/whatsapp_automation", msg)
        self.assertIn("Page Object Model", msg)
        self.assertIn("Facade Pattern", msg)
        self.assertIn("Singleton Pattern", msg)
        self.assertIn("Builder / Strategy", msg)
        self.assertIn("Persistencia de Sesión", msg)

    def test_builder_with_custom_note(self):
        builder = MessageBuilder(TechnicalReportStrategy())
        builder.set_custom_note("Prueba unitaria automatizada")
        msg = builder.build()
        self.assertIn("Prueba unitaria automatizada", msg)

    def test_custom_message_strategy(self):
        builder = MessageBuilder(CustomMessageStrategy())
        builder.set_text("Mensaje simple")
        msg = builder.build()
        self.assertEqual(msg, "Mensaje simple")


class TestSessionManagerSingleton(unittest.TestCase):
    """Pruebas para el Patrón Singleton en SessionManager."""

    def test_singleton_identity(self):
        sm1 = SessionManager(session_dir="test_session")
        sm2 = SessionManager(session_dir="test_session")
        self.assertIs(sm1, sm2, "SessionManager debe mantener una única instancia (Singleton).")


class TestPageObjectSelectors(unittest.TestCase):
    """Pruebas de selectores e integridad de los Page Objects."""

    def test_login_page_selectors(self):
        self.assertTrue(len(LoginPage.QR_SELECTORS) > 0)
        self.assertTrue(len(LoginPage.LOGGED_IN_SELECTORS) > 0)
        self.assertTrue(len(LoginPage.MODAL_SELECTORS) > 0)

    def test_chat_page_selectors(self):
        self.assertTrue(len(ChatPage.SEARCH_INPUT_SELECTORS) > 0)
        self.assertTrue(len(ChatPage.CONTACT_ITEM_SELECTORS) > 0)
        self.assertTrue(len(ChatPage.MESSAGE_INPUT_SELECTORS) > 0)
        self.assertTrue(len(ChatPage.SEND_BUTTON_SELECTORS) > 0)


class TestBotFacade(unittest.TestCase):
    """Pruebas para el Patrón Facade."""

    def test_facade_instantiation(self):
        facade = WhatsAppBotFacade(headless=True, session_dir="temp_session")
        self.assertIsNotNone(facade.session_manager)
        self.assertEqual(facade.headless, True)


if __name__ == "__main__":
    unittest.main()
