"""
Módulo LoginPage - Page Object Model (POM)
Gestiona la autenticación, detección de código QR, verificación de sesión y modales de bienvenida.
"""

import time
import logging
from typing import List
from .base_page import BasePage

logger = logging.getLogger("WhatsAppBot.LoginPage")


class LoginPage(BasePage):
    """Page Object para la pantalla de inicio y autenticación de WhatsApp Web."""

    # Selectores para el código QR
    QR_SELECTORS: List[str] = [
        'div[data-ref*="@"] canvas[role="img"]',
        'div._akau canvas[aria-label*="QR"]',
        'canvas[aria-label*="Scan me"]',
        'canvas[role="img"]',
        'div[data-testid="qrcode"]'
    ]

    # Selectores que confirman que la sesión ya está activa
    LOGGED_IN_SELECTORS: List[str] = [
        'div[data-testid="chat-list"]',
        'div[role="grid"]',
        'div[aria-label*="chat" i]',
        'div[data-tab="3"][role="textbox"]',
        'div[contenteditable="true"][data-tab="3"]',
        'header[data-testid="chatlist-header"]'
    ]

    # Selectores para modales / diálogos post-login
    MODAL_SELECTORS: List[str] = [
        'div[role="dialog"]',
        'div[data-testid="popup-contents"]'
    ]

    MODAL_CLOSE_BUTTONS: List[str] = [
        'div[role="dialog"] button',
        'div[role="dialog"] div[role="button"]',
        'div[role="button"][tabindex="0"]'
    ]

    def navigate_to_whatsapp(self, timeout_ms: int = 60000) -> None:
        """Navega a la URL oficial de WhatsApp Web."""
        print("🌐 Navegando a WhatsApp Web (https://web.whatsapp.com)...")
        self.page.goto("https://web.whatsapp.com", timeout=timeout_ms, wait_until="domcontentloaded")
        self.sleep(2.0)

    def is_logged_in(self) -> bool:
        """Verifica de inmediato si la sesión ya se encuentra autenticada."""
        for selector in self.LOGGED_IN_SELECTORS:
            try:
                locator = self.page.locator(selector).first
                if locator.is_visible(timeout=3000):
                    return True
            except Exception:
                continue
        return False

    def is_qr_present(self) -> bool:
        """Verifica si el código QR está visible en pantalla."""
        for selector in self.QR_SELECTORS:
            try:
                locator = self.page.locator(selector).first
                if locator.is_visible(timeout=2000):
                    return True
            except Exception:
                continue
        return False

    def wait_for_authentication(self, timeout_seconds: int = 300) -> bool:
        """
        Espera a que el usuario complete la autenticación.
        Si la sesión ya está guardada (cookies/storage), continúa de inmediato sin pedir QR.
        """
        print("🔍 Verificando estado de sesión...")
        
        # 1. Verificar si ya estamos logueados gracias al perfil persistente
        if self.is_logged_in():
            print("⚡ ¡Sesión persistente detectada! No es necesario escanear QR.")
            self.handle_post_login_modals()
            return True

        # 2. Si no estamos logueados, verificar si apareció el QR
        print("📱 Esperando código QR de autenticación...")
        qr_found = False
        start_time = time.time()

        while (time.time() - start_time) < 25:
            if self.is_qr_present():
                print("📷 Código QR generado. Por favor, escanéalo con tu teléfono.")
                qr_found = True
                break
            if self.is_logged_in():
                print("⚡ ¡Sesión iniciada exitosamente!")
                self.handle_post_login_modals()
                return True
            time.sleep(1)

        # 3. Esperar hasta que se complete el escaneo y desaparezca el QR
        if qr_found:
            print("⏳ Esperando que completes el escaneo en WhatsApp...")
            login_start = time.time()
            while (time.time() - login_start) < timeout_seconds:
                if self.is_logged_in():
                    print("✅ ¡Autenticación completada con éxito! Sesión guardada para futuros usos.")
                    self.handle_post_login_modals()
                    return True
                time.sleep(1)

            raise TimeoutError("Se agotó el tiempo de espera para escanear el código QR.")
        
        # 4. Verificación final tras carga lenta
        if self.is_logged_in():
            print("✅ Sesión activa confirmada.")
            self.handle_post_login_modals()
            return True
            
        return False

    def handle_post_login_modals(self, timeout_seconds: int = 5) -> None:
        """Cierra modales emergentes post-login si aparecen."""
        try:
            for modal_sel in self.MODAL_SELECTORS:
                modal = self.page.locator(modal_sel).first
                if modal.is_visible(timeout=timeout_seconds * 1000):
                    print("ℹ️ Modal post-login detectado. Cerrando...")
                    for btn_sel in self.MODAL_CLOSE_BUTTONS:
                        btn = self.page.locator(btn_sel).first
                        if btn.is_visible():
                            btn.click()
                            self.sleep(1.0)
                            return
                    # Fallback con Enter o Escape
                    self.page.keyboard.press("Escape")
                    self.sleep(0.5)
        except Exception:
            pass
