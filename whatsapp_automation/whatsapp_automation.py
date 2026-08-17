"""
Módulo Principal de WhatsApp Automation
Mantiene compatibilidad hacia atrás e implementa la nueva arquitectura basada en Facade y POM.
"""

import sys
import argparse
from typing import Optional

from .core.bot_facade import WhatsAppBotFacade
from .services.message_builder import create_technical_report_message


class WhatsAppAutomation:
    """
    Clase de automatización compatible con la API anterior,
    respaldada internamente por WhatsAppBotFacade y SessionManager.
    """
    
    def __init__(
        self,
        headless: bool = False,
        wait_time: int = 2,
        session_dir: Optional[str] = None
    ):
        self.facade = WhatsAppBotFacade(
            session_dir=session_dir,
            headless=headless,
            wait_time=wait_time
        )
        
    def __enter__(self):
        self.facade.initialize()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.facade.close()

    def start_browser(self):
        """Inicia el navegador con persistencia de sesión."""
        self.facade.initialize()

    def wait_for_login(self, timeout: int = 300):
        """Espera el login o valida la sesión persistente."""
        return self.facade.authenticate(timeout_seconds=timeout)

    def search_contact(self, phone_or_name: str) -> bool:
        """Busca y abre un contacto."""
        if not self.facade.chat_page:
            self.facade.initialize()
        return self.facade.chat_page.search_and_select_contact(phone_or_name)

    def send_message(self, message: str) -> bool:
        """Escribe y envía un mensaje en el chat abierto."""
        if not self.facade.chat_page:
            raise RuntimeError("El chat no ha sido inicializado.")
        return self.facade.chat_page.type_and_send_message(message)

    def send_whatsapp_message(self, phone: str, message: str, auto_hide: bool = False) -> bool:
        """Envía un mensaje de forma completa y orquestada."""
        return self.facade.send_message(phone=phone, message=message)

    def send_technical_report(
        self,
        phone: str,
        recipient: str = "Merza",
        developer: str = "Jose Rivero",
        repo_url: str = "https://github.com/jrivero20/whatsapp_automation",
        custom_note: Optional[str] = None
    ) -> bool:
        """Envía el reporte técnico con el saludo a Merza y los patrones de diseño."""
        return self.facade.send_technical_report(
            phone=phone,
            recipient=recipient,
            developer=developer,
            repo_url=repo_url,
            custom_note=custom_note
        )

    def close(self):
        """Cierra el navegador y guarda sesión."""
        self.facade.close()


def send_whatsapp_message(
    phone: str,
    message: str,
    wait_time: int = 2,
    headless: bool = False,
    session_dir: Optional[str] = None
) -> bool:
    """
    Función de conveniencia para enviar un mensaje de WhatsApp.
    """
    with WhatsAppBotFacade(session_dir=session_dir, headless=headless, wait_time=wait_time) as bot:
        return bot.send_message(phone=phone, message=message)


def main():
    """Interfaz de línea de comandos estándar."""
    parser = argparse.ArgumentParser(
        description='Bot de Automatización de WhatsApp (RPA)',
        epilog='Ejemplo: python whatsapp_automation.py +1234567890 "Hola Mundo"'
    )
    
    parser.add_argument('phone', help='Número de teléfono o nombre del contacto')
    parser.add_argument('message', nargs='?', default=None,
                        help='Mensaje a enviar. Si se omite, envía el reporte técnico con patrones de diseño.')
    parser.add_argument('--wait-time', type=int, default=2, 
                        help='Tiempo de espera entre acciones (default: 2)')
    parser.add_argument('--headless', action='store_true',
                        help='Ejecutar sin interfaz visual')
    parser.add_argument('--session-dir', type=str, default='session_data',
                        help='Directorio para persistencia de sesión y cookies')
    
    args = parser.parse_args()
    
    try:
        with WhatsAppBotFacade(
            session_dir=args.session_dir,
            headless=args.headless,
            wait_time=args.wait_time
        ) as bot:
            if args.message:
                bot.send_message(phone=args.phone, message=args.message)
            else:
                bot.send_technical_report(phone=args.phone)
                
            print("🎉 ¡Proceso finalizado con éxito!")
            
    except Exception as e:
        print(f"❌ Error durante la ejecución: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()