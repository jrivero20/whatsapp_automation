"""
Interfaz de línea de comandos para WhatsApp Automation (RPA)
"""

import argparse
import sys
from .core.bot_facade import WhatsAppBotFacade


def main():
    """CLI principal del bot de WhatsApp."""
    parser = argparse.ArgumentParser(
        description='Bot de Automatización de WhatsApp (RPA)',
        epilog='Ejemplo: whatsapp-send +1234567890 "Hola Mundo"'
    )
    
    parser.add_argument('phone', help='Número de teléfono o nombre del contacto')
    parser.add_argument('message', nargs='?', default=None,
                        help='Mensaje a enviar. Si se omite, envía el reporte técnico con patrones de diseño.')
    parser.add_argument('--wait-time', type=int, default=2, 
                        help='Tiempo de espera entre acciones en segundos (default: 2)')
    parser.add_argument('--headless', action='store_true',
                        help='Ejecutar en segundo plano sin interfaz gráfica')
    parser.add_argument('--session-dir', type=str, default='session_data',
                        help='Directorio de persistencia de sesión/cookies')
    parser.add_argument('--note', type=str, default=None,
                        help='Nota personalizada opcional para el reporte')
    parser.add_argument('--version', action='version', version='%(prog)s 2.0.0')
    
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
                bot.send_technical_report(phone=args.phone, custom_note=args.note)
                
            print("🎉 ¡Mensaje enviado con éxito!")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
