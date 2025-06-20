"""
Interfaz de línea de comandos para WhatsApp Automation
"""

import argparse
import sys
from .whatsapp_automation import send_whatsapp_message

def main():
    """Interfaz de línea de comandos principal"""
    parser = argparse.ArgumentParser(
        description='Envía mensajes de WhatsApp desde la línea de comandos',
        epilog='Ejemplo: whatsapp-send +1234567890 "Hola Mundo"'
    )
    
    parser.add_argument('phone', help='Número de teléfono con código de país')
    parser.add_argument('message', help='Mensaje a enviar')
    parser.add_argument('--wait-time', type=int, default=2, 
                       help='Tiempo de espera entre acciones (default: 2)')
    parser.add_argument('--headless', action='store_true',
                       help='Ejecutar sin interfaz visual')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    
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
