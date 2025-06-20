from playwright.sync_api import sync_playwright
import time
import argparse
import sys
from typing import Optional, Union

class WhatsAppAutomation:
    """
    Librería para automatizar envío de mensajes en WhatsApp Web usando Playwright.
    Utiliza selectores robustos que funcionan en múltiples idiomas.
    """
    
    def __init__(self, headless: bool = False, wait_time: int = 2):
        """
        Inicializa la automatización de WhatsApp.
        
        Args:
            headless: Si True, ejecuta el navegador sin interfaz visual
            wait_time: Tiempo de espera entre acciones en segundos
        """
        self.headless = headless
        self.wait_time = wait_time
        self.browser = None
        self.context = None
        self.page = None
        
    def __enter__(self):
        """Context manager entry"""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup"""
        self.close()
    
    def _get_selectors(self):
        """
        Define selectores robustos basados en atributos data y roles,
        no en texto ni estilos CSS para compatibilidad multiidioma.
        """
        return {
            # QR Code - Selector basado en estructura específica del QR
            'qr_container': 'div[data-ref*="@"] canvas[role="img"]',
            'qr_wrapper': 'div._akau canvas[aria-label*="QR"], canvas[role="img"]',
            
            # Chat list - Selector basado en data-testid
            'chat_list': 'div[data-testid="chat-list"]',
            'chat_list_alt': 'div[role="grid"], div[aria-label*="chat"], div[role="main"] div[role="list"]',
            
            # Search box - Selector basado en data-tab y role
            'search_box': 'div[data-tab="3"][role="textbox"]',
            'search_box_alt': 'div[contenteditable="true"][data-tab="3"]',
            'search_input': 'div[aria-label*="search" i][contenteditable="true"], div[data-tab="3"][contenteditable="true"]',
            
            # Contact item - Selector basado en estructura de lista
            'contact_item': 'div[role="listitem"] div[role="button"]',
            'contact_item_alt': 'div[role="listitem"] [tabindex="0"]',
            
            # Message input - Selector basado en data-tab específico para mensajes
            'message_input': 'div[data-tab="10"][contenteditable="true"]',
            'message_input_alt': 'div[contenteditable="true"][role="textbox"]:not([data-tab="3"])',
            
            # Send button - Selector basado en data-tab del botón enviar
            'send_button': 'button[data-tab="11"]',
            'send_button_alt': 'button[aria-label*="send" i], button[data-testid="send"]',
            
            # Loading indicators
            'loading': 'div[data-testid="loading"], div[role="progressbar"]',

            # Modal post-login
            'modal_container': 'div[role="dialog"]',  # Contenedor principal del modal
            'modal_button': 'div[role="dialog"] button',  # Botón dentro del modal
            'modal_button_alt': 'div[role="button"][tabindex="0"]',  # Alternativa
        }
    
    def start_browser(self):
        """Inicia el navegador y navega a WhatsApp Web"""
        if self.browser:
            return  # Ya iniciado
            
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        
        # Navegar a WhatsApp Web
        print("🌐 Navegando a WhatsApp Web...")
        self.page.goto("https://web.whatsapp.com", timeout=60000)
    
    def wait_for_login(self, timeout: int = 300):
        """
        Espera a que el usuario escanee el QR y complete el login.
        
        Args:
            timeout: Tiempo máximo de espera en segundos
        """
        selectors = self._get_selectors()
        
        try:
            print("📱 Por favor, escanea el código QR de WhatsApp Web...")
            
            # Esperar a que aparezca el QR
            qr_selectors = [selectors['qr_container'], selectors['qr_wrapper']]
            qr_found = False
            
            for selector in qr_selectors:
                try:
                    self.page.wait_for_selector(selector, state="visible", timeout=30000)
                    print("✅ Código QR detectado")
                    qr_found = True
                    break
                except:
                    continue
            
            if not qr_found:
                print("⚠️  No se detectó el QR, continuando...")
            
            # Esperar a que desaparezca el QR (login completado)
            print("⏳ Esperando inicio de sesión...")
            
            for selector in qr_selectors:
                try:
                    self.page.wait_for_selector(selector, state="hidden", timeout=timeout * 1000)
                    break
                except:
                    continue
            
            print("✅ Inicio de sesión detectado!")

            
            
            # Esperar a que cargue la interfaz principal
            chat_selectors = [selectors['chat_list'], selectors['chat_list_alt']]
            
            for selector in chat_selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=30000)
                    print("✅ Interfaz principal cargada")
                    
                     # -----Manejar modal post-login -----
                    self._handle_post_login_modal()
                    return
                except:
                    continue
                    
            print("⚠️  Interfaz principal cargada (método alternativo)")
            time.sleep(3)  # Tiempo adicional de seguridad
            
        except Exception as e:
            raise RuntimeError(f"Error durante el login: {str(e)}")
    
    def hide_browser(self):
        """Oculta la ventana del navegador movéndola fuera de la pantalla"""
        if self.page and not self.headless:
            try:
                self.page.evaluate("() => window.moveTo(-3000, -3000)")
                print("🔒 Navegador ocultado")
            except:
                pass  # Si falla, continúa sin ocultar
    
    def search_contact(self, phone_or_name: str) -> bool:
        """
        Busca un contacto por número de teléfono o nombre.
        
        Args:
            phone_or_name: Número de teléfono (ej: +1234567890) o nombre del contacto
            
        Returns:
            bool: True si se encontró el contacto
        """
        selectors = self._get_selectors()
        
        # Buscar la caja de búsqueda
        search_selectors = [selectors['search_box'], selectors['search_box_alt'], selectors['search_input']]
        search_box = None
        
        for selector in search_selectors:
            try:
                search_box = self.page.locator(selector).first
                if search_box.is_visible():
                    break
            except:
                continue
        
        if not search_box or not search_box.is_visible():
            raise RuntimeError("No se encontró la caja de búsqueda")
        
        # Limpiar y escribir en la búsqueda
        search_box.click()
        time.sleep(0.5)
        
        # Limpiar el campo (Ctrl+A + Delete)
        search_box.press("Control+a")
        search_box.press("Delete")
        time.sleep(0.5)
        
        # Escribir el contacto
        search_box.fill(phone_or_name)
        time.sleep(self.wait_time)
        
        # Buscar elemento del contacto
        contact_selectors = [selectors['contact_item'], selectors['contact_item_alt']]
        
        for selector in contact_selectors:
            try:
                contact_items = self.page.locator(selector)
                if contact_items.count() > 0:
                    # Hacer clic en el primer resultado
                    contact_items.first.click()
                    time.sleep(self.wait_time)
                    return True
            except:
                continue
        
        return False
    
    def send_message(self, message: str) -> bool:
        """
        Envía un mensaje al contacto actualmente seleccionado.
        
        Args:
            message: Texto del mensaje a enviar
            
        Returns:
            bool: True si el mensaje se envió correctamente
        """
        selectors = self._get_selectors()
        
        try:
            # Buscar el campo de entrada de mensaje
            input_selectors = [selectors['message_input'], selectors['message_input_alt']]
            message_input = None
            
            for selector in input_selectors:
                try:
                    message_input = self.page.locator(selector).first
                    if message_input.is_visible():
                        break
                except:
                    continue
            
            if not message_input or not message_input.is_visible():
                raise RuntimeError("No se encontró el campo de entrada de mensaje")
            
            # Escribir el mensaje
            message_input.click()
            time.sleep(0.5)
            message_input.fill(message)
            time.sleep(self.wait_time / 2)
            
            # Buscar y hacer clic en el botón de enviar
            send_selectors = [selectors['send_button'], selectors['send_button_alt']]
            
            for selector in send_selectors:
                try:
                    send_button = self.page.locator(selector).first
                    if send_button.is_visible():
                        send_button.click()
                        time.sleep(self.wait_time)
                        return True
                except:
                    continue
            
            # Si no se encuentra el botón, intentar con Enter
            message_input.press("Enter")
            time.sleep(self.wait_time)
            return True
            
        except Exception as e:
            raise RuntimeError(f"Error al enviar mensaje: {str(e)}")
    
    def send_whatsapp_message(self, phone: str, message: str, auto_hide: bool = True) -> bool:
        """
        Función principal para enviar un mensaje de WhatsApp.
        
        Args:
            phone: Número de teléfono con código de país (ej: +1234567890)
            message: Mensaje a enviar
            auto_hide: Si True, oculta el navegador después del login
            
        Returns:
            bool: True si el mensaje se envió correctamente
        """
        # Validación básica del número
        if not phone.startswith('+') or len(phone) < 8:
            raise ValueError("Formato de número inválido. Debe incluir código de país (ej: +1234567890)")
        
        try:
            # 1. Iniciar navegador
            self.start_browser()
            
            # 2. Esperar login del usuario
            self.wait_for_login()
            
            # 3. Ocultar navegador si se solicita
            if auto_hide:
                self.hide_browser()
            
            # 4. Buscar contacto
            print(f"🔍 Buscando contacto: {phone}")
            if not self.search_contact(phone):
                raise RuntimeError(f"No se encontró el contacto: {phone}")
            
            print("✅ Contacto encontrado")
            
            # 5. Enviar mensaje
            print("📤 Enviando mensaje...")
            if not self.send_message(message):
                raise RuntimeError("No se pudo enviar el mensaje")
            
            print("✅ Mensaje enviado correctamente")
            return True
            
        except Exception as e:
            raise RuntimeError(f"Error en la automatización: {str(e)}")
    
    def close(self):
        """Cierra el navegador y limpia recursos"""
        if self.browser:
            self.browser.close()
            self.browser = None
            self.context = None
            self.page = None

    def _handle_post_login_modal(self, timeout: int = 10):
        """
        Maneja el modal que aparece después del login.
        
        Args:
            timeout: Tiempo máximo de espera en segundos
        """
        selectors = self._get_selectors()
        
        try:
            print("🔄 Verificando modal post-login...")
            
            # Esperar a que aparezca el modal (si existe)
            modal_selectors = [selectors['modal_container']]
            
            for selector in modal_selectors:
                try:
                    self.page.wait_for_selector(selector, state="visible", timeout=timeout * 1000)
                    print("⚠️  Modal detectado, intentando cerrar...")
                    
                    # Intentar hacer clic en el botón del modal
                    button_selectors = [selectors['modal_button'], selectors['modal_button_alt']]
                    
                    for btn_selector in button_selectors:
                        try:
                            button = self.page.locator(btn_selector).first
                            if button.is_visible():
                                button.click()
                                print("✅ Modal cerrado")
                                time.sleep(self.wait_time)  # Pequeña pausa post-interacción
                                return
                        except:
                            continue
                    
                    # Si no se encontró el botón, intentar con Enter
                    self.page.keyboard.press("Enter")
                    print("✅ Modal cerrado (con teclado)")
                    return
                    
                except:
                    continue
            
            print("✅ No se detectó modal post-login")
            
        except Exception as e:
            print(f"⚠️  Error al manejar modal: {str(e)}")

def send_whatsapp_message(phone: str, message: str, wait_time: int = 2, headless: bool = False) -> bool:
    """
    Función de conveniencia para enviar un mensaje de WhatsApp.
    
    Args:
        phone: Número de teléfono con código de país
        message: Mensaje a enviar
        wait_time: Tiempo de espera entre acciones
        headless: Si True, ejecuta sin interfaz visual
        
    Returns:
        bool: True si el mensaje se envió correctamente
    """
    with WhatsAppAutomation(headless=headless, wait_time=wait_time) as wa:
        return wa.send_whatsapp_message(phone, message)


def main():
    """Interfaz de línea de comandos"""
    parser = argparse.ArgumentParser(
        description='Envía mensajes de WhatsApp desde la línea de comandos',
        epilog='Ejemplo: python whatsapp_sender.py +1234567890 "Hola Mundo"'
    )
    
    parser.add_argument('phone', help='Número de teléfono con código de país')
    parser.add_argument('message', help='Mensaje a enviar')
    parser.add_argument('--wait-time', type=int, default=2, 
                       help='Tiempo de espera entre acciones (default: 2)')
    parser.add_argument('--headless', action='store_true',
                       help='Ejecutar sin interfaz visual')
    
    args = parser.parse_args()
    
    try:
        print(f"📱 Enviando mensaje a {args.phone}...")
        success = send_whatsapp_message(
            phone=args.phone,
            message=args.message,
            wait_time=args.wait_time,
            headless=args.headless
        )
        
        if success:
            print("🎉 ¡Mensaje enviado con éxito!")
        else:
            print("❌ Error: No se pudo enviar el mensaje")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()