# ejemplo_individual.py
from whatsapp_automation import WhatsAppAutomation
import sys

def enviar_mensaje_avanzado():
    """Envía un mensaje de WhatsApp solicitando datos por consola"""
    try:
        # Solicitar número de teléfono
        telefono = input("📱 Ingresa el número de teléfono (formato internacional +1234567890): ").strip()
        
        # Validar formato básico
        if not telefono.startswith('+') or len(telefono) < 8:
            print("❌ Formato inválido. Debe comenzar con '+' y tener al menos 8 dígitos.")
            return
        
        # Solicitar mensaje
        mensaje = input("💬 Ingresa el mensaje a enviar: ").strip()
        if not mensaje:
            print("❌ El mensaje no puede estar vacío")
            return
        
        # Confirmación
        print(f"\n⚠️ ATENCIÓN: Se enviará este mensaje a {telefono}")
        confirmacion = input("¿Continuar? (s/n): ").strip().lower()
        
        if confirmacion != 's':
            print("🚫 Envío cancelado")
            return
        
        # Ejecutar envío
        print("\n⏳ Iniciando envío...")
        with WhatsAppAutomation(headless=False, wait_time=3) as wa:
            if wa.send_whatsapp_message(telefono, mensaje):
                print("\n✅ ¡Mensaje enviado con éxito!")
            else:
                print("\n❌ Error al enviar el mensaje")
    
    except KeyboardInterrupt:
        print("\n🚫 Operación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error crítico: {str(e)}")

if __name__ == "__main__":
    enviar_mensaje_avanzado()
    # Pausa adicional para Windows
    if sys.platform.startswith('win'):
        input("\nPresiona Enter para salir...")