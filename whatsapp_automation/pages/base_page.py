"""
Módulo Base Page - Page Object Model (POM)
Encapsula la instancia de Playwright Page y provee métodos de interacción robustos y multiidioma.
"""

import time
import logging
from typing import List, Optional, Union
from playwright.sync_api import Page, Locator

logger = logging.getLogger("WhatsAppBot.POM")


class BasePage:
    """Clase base para todos los Page Objects de WhatsApp Web."""

    def __init__(self, page: Page, wait_time: float = 2.0):
        self.page = page
        self.wait_time = wait_time

    def sleep(self, seconds: Optional[float] = None) -> None:
        """Pausa la ejecución por un tiempo determinado."""
        delay = seconds if seconds is not None else self.wait_time
        time.sleep(delay)

    def find_first_visible(self, selectors: List[str], timeout_ms: int = 5000) -> Optional[Locator]:
        """
        Evalúa una lista de selectores alternativos y retorna el primer Locator visible.
        Útil para selectores multiidioma y variaciones de interfaz de WhatsApp Web.
        """
        for selector in selectors:
            try:
                locator = self.page.locator(selector).first
                if locator.is_visible(timeout=timeout_ms):
                    return locator
            except Exception:
                continue
        return None

    def wait_for_any(self, selectors: List[str], state: str = "visible", timeout_ms: int = 15000) -> Optional[str]:
        """
        Espera hasta que cualquiera de los selectores coincida con el estado solicitado.
        Retorna el selector que tuvo éxito o None.
        """
        start_time = time.time()
        timeout_sec = timeout_ms / 1000.0
        
        while (time.time() - start_time) < timeout_sec:
            for selector in selectors:
                try:
                    locator = self.page.locator(selector).first
                    if state == "visible" and locator.is_visible():
                        return selector
                    elif state == "hidden" and not locator.is_visible():
                        return selector
                except Exception:
                    pass
            time.sleep(0.5)
        return None

    def safe_click(self, selector_or_locator: Union[str, Locator], timeout_ms: int = 5000) -> bool:
        """Hace clic de manera segura en un selector o Locator con reintentos."""
        try:
            if isinstance(selector_or_locator, str):
                loc = self.page.locator(selector_or_locator).first
            else:
                loc = selector_or_locator
            loc.wait_for(state="visible", timeout=timeout_ms)
            loc.click()
            self.sleep(0.5)
            return True
        except Exception as e:
            logger.debug(f"Error en safe_click: {e}")
            return False

    def safe_fill(self, selector_or_locator: Union[str, Locator], text: str, clear: bool = True) -> bool:
        """Escribe texto en un campo de entrada asegurando el foco y limpieza previa."""
        try:
            if isinstance(selector_or_locator, str):
                loc = self.page.locator(selector_or_locator).first
            else:
                loc = selector_or_locator
            loc.wait_for(state="visible", timeout=5000)
            loc.click()
            if clear:
                loc.press("Control+a")
                loc.press("Delete")
                self.sleep(0.2)
            loc.fill(text)
            self.sleep(0.5)
            return True
        except Exception as e:
            logger.debug(f"Error en safe_fill: {e}")
            return False
