"""
Módulo SessionManager - Patrón Singleton
Gestiona el ciclo de vida del navegador y la persistencia de sesión (cookies, LocalStorage, IndexedDB)
utilizando el contexto persistente de Playwright.
"""

import os
import sys
import logging
from typing import Optional
from playwright.sync_api import sync_playwright, BrowserContext, Page, Playwright

logger = logging.getLogger("WhatsAppBot.SessionManager")


class SessionManager:
    """
    Patrón Singleton para administrar la sesión persistente de Playwright.
    Garantiza que la sesión de WhatsApp Web y sus cookies se guarden en disco.
    """
    _instance: Optional["SessionManager"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(
        self,
        session_dir: Optional[str] = None,
        headless: bool = False,
        wait_time: float = 2.0
    ):
        if self._initialized:
            # Actualizar configuraciones si se reinicializa
            if session_dir:
                self.session_dir = os.path.abspath(session_dir)
            self.headless = headless
            self.wait_time = wait_time
            return

        self.session_dir = os.path.abspath(session_dir or os.path.join(os.getcwd(), "session_data"))
        self.headless = headless
        self.wait_time = wait_time

        self.playwright: Optional[Playwright] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self._initialized = True

    def initialize_session(self) -> Page:
        """
        Inicia Playwright con un contexto persistente que almacena cookies,
        IndexedDB y estado de autenticación en la carpeta `session_dir`.
        """
        if self.page and not self.page.is_closed():
            return self.page

        # Asegurar existencia del directorio de sesión
        os.makedirs(self.session_dir, exist_ok=True)
        print(f"📁 Directorio de sesión persistente: {self.session_dir}")

        if not self.playwright:
            self.playwright = sync_playwright().start()

        # Argumentos para evitar detección de bot y garantizar estabilidad
        launch_args = [
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
            "--no-sandbox",
            "--disable-setuid-sandbox"
        ]

        print("🚀 Lanzando navegador con perfil de usuario persistente...")
        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.session_dir,
            headless=self.headless,
            args=launch_args,
            viewport=None,  # Usar tamaño de ventana real
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        if len(self.context.pages) > 0:
            self.page = self.context.pages[0]
        else:
            self.page = self.context.new_page()

        return self.page

    def get_page(self) -> Page:
        """Retorna la página activa o la inicializa si no existe."""
        if not self.page or self.page.is_closed():
            return self.initialize_session()
        return self.page

    def close(self) -> None:
        """Cierra el contexto y libera los recursos de Playwright."""
        try:
            if self.context:
                print("🔒 Guardando cookies y cerrando sesión del navegador...")
                self.context.close()
                self.context = None
                self.page = None
            if self.playwright:
                self.playwright.stop()
                self.playwright = None
        except Exception as e:
            logger.debug(f"Error al cerrar SessionManager: {e}")

    @classmethod
    def reset_instance(cls):
        """Reinicia la instancia singleton (útil para pruebas o reinicios completos)."""
        if cls._instance:
            cls._instance.close()
            cls._instance = None

    def __enter__(self):
        self.initialize_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
