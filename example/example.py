"""
Ejemplo interactivo de uso de WhatsApp Automation (RPA)
"""

import sys
import os

# Asegurar que se pueda importar el paquete local
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from whatsapp_automation import WhatsAppBotFacade


def main():
    print("=" * 60)
    print("🤖 BOT DE WHATSAPP RPA - ENVÍO CON PATRONES DE DISEÑO")
    print("=" * 60)
    
    try:
        phone = input("\n📱 Ingresa el número de teléfono (ej: +584121234567) o contacto: ").strip()
        if not phone:
            print("❌ El destinatario no puede estar vacío.")
            return

        print("\nSelecciona el tipo de mensaje a enviar:")
        print("1. Reporte Técnico con Patrones de Diseño (Recomendado)")
        print("2. Mensaje personalizado")
        opcion = input("Opción (1/2, default 1): ").strip()

        custom_message = None
        if opcion == "2":
            custom_message = input("💬 Ingresa tu mensaje personalizado: ").strip()
            if not custom_message:
                print("❌ El mensaje no puede estar vacío.")
                return

        print("\n🚀 Iniciando automatización RPA...")
        with WhatsAppBotFacade(headless=False, wait_time=2) as bot:
            if custom_message:
                bot.send_message(phone=phone, message=custom_message)
            else:
                bot.send_technical_report(phone=phone)

        print("\n✅ ¡Automatización ejecutada exitosamente!")

    except KeyboardInterrupt:
        print("\n🛑 Proceso cancelado por el usuario.")
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")


if __name__ == "__main__":
    main()
    if sys.platform.startswith("win"):
        input("\nPresiona Enter para finalizar...")