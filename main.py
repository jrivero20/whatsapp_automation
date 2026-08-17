"""
==============================================================================
BOT DE WHATSAPP RPA - PUNTO DE ENTRADA PRINCIPAL (MAIN)
==============================================================================
Este script automatiza el inicio de sesión y envío de mensajes mediante WhatsApp Web
utilizando Playwright con persistencia de cookies/sesión y patrones de diseño (POM, Facade, Singleton).
"""

import os
import sys
import json
import argparse

# Agregar directorio del paquete al path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from whatsapp_automation import WhatsAppBotFacade, create_technical_report_message


def load_config():
    """Carga la configuración desde config.json si existe."""
    config_paths = [
        os.path.join(current_dir, "config.json"),
        os.path.join(parent_dir, "config.json")
    ]
    for cfg_path in config_paths:
        if os.path.exists(cfg_path):
            try:
                with open(cfg_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return {}


def main():
    parser = argparse.ArgumentParser(description="Bot de Automatización de WhatsApp (RPA)")
    parser.add_argument("--phone", "-p", type=str, default=None, help="Número de teléfono o nombre del contacto")
    parser.add_argument("--message", "-m", type=str, default=None, help="Mensaje personalizado a enviar")
    parser.add_argument("--session-dir", "-s", type=str, default=None, help="Directorio de persistencia de sesión")
    parser.add_argument("--headless", action="store_true", help="Ejecutar sin interfaz gráfica")
    args = parser.parse_args()

    config = load_config()

    print("=" * 65)
    print("       🤖 BOT DE WHATSAPP RPA - AUTOMATIZACIÓN PLAYWRIGHT")
    print("=" * 65)
    print("📌 Características activas:")
    print("   • Persistencia de sesión y cookies (No requiere QR tras login)")
    print("   • Arquitectura modular con Patrones de Diseño (POM, Facade, Singleton)")
    print("   • Interacción 100% gráfica por interfaz (búsqueda y redacción)")
    print("=" * 65)

    # 1. Determinar destinatario (número o nombre)
    target = args.phone or config.get("phone")
    if not target:
        print("\n📱 Configuración de destinatario:")
        target = input("👉 Ingresa el número de teléfono (ej: +584121234567) o nombre del contacto: ").strip()

    if not target:
        print("❌ Error: No se especificó ningún destinatario.")
        return 1

    # 2. Determinar tipo de mensaje
    message = args.message or config.get("custom_message")
    message_mode = config.get("message_mode", "technical_report")

    if not message and message_mode != "technical_report":
        print("\n💬 Opciones de mensaje:")
        print("1. Reporte Técnico de Patrones de Diseño (Recomendado)")
        print("2. Mensaje personalizado libre")
        opc = input("Selecciona una opción (1/2, por defecto 1): ").strip()
        if opc == "2":
            message = input("👉 Escribe el mensaje personalizado: ").strip()

    session_dir = args.session_dir or config.get("session_dir", os.path.join(current_dir, "session_data"))
    headless = args.headless or config.get("headless", False)
    wait_time = config.get("wait_time", 2)
    recipient = config.get("recipient", "Merza")
    developer = config.get("developer", "Jose Rivero")
    repo_url = config.get("repo_url", "https://github.com/jrivero20/whatsapp_automation")
    custom_note = config.get("custom_note")

    print(f"\n⚙️  Configuración de ejecución:")
    print(f"   • Destinatario: {target}")
    print(f"   • Sesión persistente en: {session_dir}")
    print(f"   • Modo Headless: {'Activado' if headless else 'Desactivado (Visible)'}")
    print(f"   • Tipo de mensaje: {'Personalizado' if message else 'Reporte Técnico (Patrones de Diseño)'}")
    print("-" * 65)

    # 3. Ejecución del Bot mediante Facade
    try:
        with WhatsAppBotFacade(
            session_dir=session_dir,
            headless=headless,
            wait_time=wait_time
        ) as bot:
            if message:
                bot.send_message(phone=target, message=message)
            else:
                bot.send_technical_report(
                    phone=target,
                    recipient=recipient,
                    developer=developer,
                    repo_url=repo_url,
                    custom_note=custom_note
                )

        print("\n" + "=" * 65)
        print("✨ ¡EJECUCIÓN COMPLETADA EXITOSAMENTE! ✨")
        print("Las cookies y la sesión han quedado almacenadas para futuras ejecuciones.")
        print("=" * 65)
        return 0

    except Exception as e:
        print(f"\n❌ Ocurrió un error en el bot RPA: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
