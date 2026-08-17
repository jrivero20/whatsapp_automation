"""
Módulo WhatsAppBotFacade - Patrón Facade (Fachada)
Proporciona una interfaz unificada, simple y robusta para toda la automatización RPA de WhatsApp,
ocultando la complejidad de sincronización de Playwright, Page Objects y Session Management.
"""

import sys
import time
import logging
from typing import Optional

from .session_manager import SessionManager
from ..pages.login_page import LoginPage
from ..pages.chat_page import ChatPage
from ..services.message_builder import MessageBuilder, MerzaDesignPatternsStrategy, CustomMessageStrategy

logger = logging.getLogger("WhatsAppBot.Facade")


class WhatsAppBotFacade:
    """
    Patrón Facade: Orquestador principal del Bot RPA de WhatsApp.
    Interactúa 100% a través de la interfaz gráfica (búsqueda lateral, selección de chat y redacción).
    """

    def __init__(
        self,
        session_dir: Optional[str] = None,
        headless: bool = False,
        wait_time: float = 2.0,
        auto_close: bool = True
    ):
        self.session_dir = session_dir
        self.headless = headless
        self.wait_time = wait_time
        self.auto_close = auto_close

        # Singleton Session Manager
        self.session_manager = SessionManager(
            session_dir=self.session_dir,
            headless=self.headless,
            wait_time=self.wait_time
        )
        self.page = None
        self.login_page: Optional[LoginPage] = None
        self.chat_page: Optional[ChatPage] = None

    def initialize(self) -> None:
        """Inicia el navegador y los Page Objects."""
        self.page = self.session_manager.initialize_session()
        self.login_page = LoginPage(self.page, wait_time=self.wait_time)
        self.chat_page = ChatPage(self.page, wait_time=self.wait_time)

    def authenticate(self, timeout_seconds: int = 300) -> bool:
        """
        Navega a WhatsApp Web y asegura que la sesión esté lista.
        Si la sesión ya fue guardada en el perfil, se inicia instantáneamente.
        """
        if not self.login_page:
            self.initialize()

        self.login_page.navigate_to_whatsapp()
        return self.login_page.wait_for_authentication(timeout_seconds=timeout_seconds)

    def send_message(self, phone: str, message: str) -> bool:
        """
        Envía un mensaje de texto a un destinatario a través de la interfaz gráfica.
        
        Args:
            phone: Número telefónico o nombre de contacto
            message: Contenido del mensaje a enviar
            
        Returns:
            bool: True si el mensaje se envió con éxito
        """
        self.authenticate()

        print(f"\n📨 Iniciando proceso de envío a: {phone}")
        
        # 1. Búsqueda y selección visual en la barra lateral
        chat_selected = self.chat_page.search_and_select_contact(phone)

        if not chat_selected:
            raise RuntimeError(f"No se pudo encontrar o abrir el chat para '{phone}' en la interfaz de WhatsApp.")

        # 2. Escribir y enviar el mensaje
        success = self.chat_page.type_and_send_message(message)
        
        if success:
            print("\n🎉 ¡PROCESO COMPLETADO! Mensaje entregado con éxito a través de la UI.")
            time.sleep(3.0)
            
        return success

    def send_merza_pattern_message(self, phone: str, custom_note: Optional[str] = None) -> bool:
        """
        Construye y envía el mensaje de la asignación con el encabezado 'merza'
        y el detalle técnico de los patrones de diseño aplicados.
        """
        print("📐 Generando mensaje estructurado con patrones de diseño...")
        builder = MessageBuilder(MerzaDesignPatternsStrategy())
        if custom_note:
            builder.set_custom_note(custom_note)
        
        formatted_message = builder.build()
        return self.send_message(phone=phone, message=formatted_message)

    def close(self) -> None:
        """Cierra el bot y guarda el estado."""
        self.session_manager.close()

    def __enter__(self):
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.auto_close:
            self.close()
