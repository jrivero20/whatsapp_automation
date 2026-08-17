"""
Módulo ChatPage - Page Object Model (POM)
Interacción 100% por interfaz gráfica con WhatsApp Web.
Basado en los elementos y selectores exactos del DOM de WhatsApp Web (Lexical editor, testids y data-tab).
Compatible con modo Claro y Oscuro, y con cualquier número o contacto.
"""

import time
import logging
from typing import List, Optional
from playwright.sync_api import Locator
from .base_page import BasePage

logger = logging.getLogger("WhatsAppBot.ChatPage")


class ChatPage(BasePage):
    """Page Object para la interacción y envío de mensajes vía Interfaz Gráfica."""

    # 1. Barra de búsqueda de la izquierda (DOM exacto)
    SEARCH_INPUT_SELECTORS: List[str] = [
        'input[data-tab="3"]',
        'input[role="textbox"][aria-label*="Buscar" i]',
        'input[role="textbox"][aria-label*="Search" i]',
        'input[placeholder*="Buscar un chat" i]',
        'input[placeholder*="Search" i]',
        'div.html-div input[type="text"]',
        'div[data-tab="3"][contenteditable="true"]'
    ]

    # 2. Ficha de contacto en los resultados de búsqueda (DOM exacto)
    CONTACT_ITEM_SELECTORS: List[str] = [
        'div[data-testid="cell-frame-container"]',
        'div[data-testid="cell-frame-title"]',
        'div[data-testid^="list-item-"]',
        'div[role="row"] div[role="gridcell"]',
        'div[role="listitem"] div[role="button"]'
    ]

    # 3. Caja de texto para redactar mensaje (DOM exacto con editor Lexical de WhatsApp)
    MESSAGE_INPUT_SELECTORS: List[str] = [
        'footer div[contenteditable="true"]',
        'p.selectable-text.copyable-text',
        'footer p[dir="auto"]',
        'div[contenteditable="true"][role="textbox"]',
        'div[data-tab="10"][contenteditable="true"]',
        'div[data-testid="conversation-compose-box-input"]',
        'footer [contenteditable="true"]'
    ]

    # 4. Botón de Enviar mensaje
    SEND_BUTTON_SELECTORS: List[str] = [
        'button[data-testid="compose-btn-send"]',
        'span[data-icon="send"]',
        'button[aria-label*="Send" i]',
        'button[aria-label*="Enviar" i]',
        'button[data-tab="11"]'
    ]

    def search_and_select_contact(self, query: str) -> bool:
        """
        Busca el contacto o número a través de la barra de búsqueda visual
        y hace clic en el primer resultado filtrado.
        """
        print(f"🔍 Localizando barra de búsqueda en la interfaz...")

        # 1. Encontrar la barra de búsqueda
        search_input = self.find_first_visible(self.SEARCH_INPUT_SELECTORS, timeout_ms=10000)
        if not search_input:
            raise RuntimeError("No se encontró la barra de búsqueda de chats en la interfaz.")

        print(f"✍️ Escribiendo '{query}' en la barra de búsqueda...")
        search_input.click()
        self.sleep(0.3)
        
        # Limpiar cualquier texto previo
        search_input.press("Control+a")
        search_input.press("Backspace")
        self.sleep(0.2)

        # Escribir el número o nombre del contacto
        search_input.fill(query)
        self.sleep(2.5)  # Espera para que la lista de resultados filtre

        # 2. Seleccionar el resultado en la lista
        print("🎯 Buscando contacto en los resultados filtrados...")
        
        # Primero intentar hacer clic en el contenedor del chat encontrado
        for selector in self.CONTACT_ITEM_SELECTORS:
            try:
                items = self.page.locator(selector)
                if items.count() > 0:
                    first_item = items.first
                    if first_item.is_visible():
                        first_item.click()
                        self.sleep(2.0)
                        if self.is_message_box_ready():
                            print("✅ Contacto seleccionado y chat abierto con éxito.")
                            return True
            except Exception:
                continue

        # Alternativa: presionar Enter directamente en el campo de búsqueda
        try:
            print("⌨️ Presionando Enter en la barra de búsqueda...")
            search_input.press("Enter")
            self.sleep(2.0)
            if self.is_message_box_ready():
                print("✅ Chat abierto mediante Enter.")
                return True
        except Exception:
            pass

        return False

    def is_message_box_ready(self, timeout_seconds: int = 5) -> bool:
        """Verifica si el área de redacción del mensaje está visible."""
        start = time.time()
        while (time.time() - start) < timeout_seconds:
            for selector in self.MESSAGE_INPUT_SELECTORS:
                try:
                    locator = self.page.locator(selector).first
                    if locator.is_visible():
                        return True
                except Exception:
                    continue
            time.sleep(0.5)
        return False

    def type_and_send_message(self, message: str) -> bool:
        """
        Hace clic en el cuadro de texto del chat, redacta el mensaje y lo envía.
        Soporta saltos de línea correctamente mediante Shift+Enter.
        """
        print("💬 Localizando cuadro de redacción de mensaje...")

        message_box = self.find_first_visible(self.MESSAGE_INPUT_SELECTORS, timeout_ms=15000)
        if not message_box:
            raise RuntimeError("No se encontró la caja de redacción del mensaje en el chat abierto.")

        # Enfocar la caja de texto
        message_box.click()
        self.sleep(0.4)

        print("✍️ Escribiendo mensaje...")
        lines = message.split("\n")
        for idx, line in enumerate(lines):
            if line:
                self.page.keyboard.insert_text(line)
            if idx < len(lines) - 1:
                # Salto de línea en el editor Lexical de WhatsApp
                self.page.keyboard.down("Shift")
                self.page.keyboard.press("Enter")
                self.page.keyboard.up("Shift")
                time.sleep(0.05)

        self.sleep(0.8)

        # Enviar mensaje con Enter
        print("📤 Enviando mensaje...")
        self.page.keyboard.press("Enter")
        self.sleep(self.wait_time)

        # Si aún estuviera visible el botón de enviar, hacer clic
        send_btn = self.find_first_visible(self.SEND_BUTTON_SELECTORS, timeout_ms=2000)
        if send_btn and send_btn.is_visible():
            try:
                send_btn.click()
                self.sleep(self.wait_time)
            except Exception:
                pass

        print("✅ Mensaje enviado exitosamente a través de la interfaz.")
        return True
