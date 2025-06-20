"""
# WhatsApp Automation

Librería Python para automatizar el envío de mensajes en WhatsApp Web usando Playwright.

## Características

- ✅ **Multiidioma**: Selectores robustos que funcionan independientemente del idioma
- 🔒 **Seguro**: No requiere tokens ni APIs, usa WhatsApp Web oficial
- 🚀 **Fácil de usar**: API simple y limpia
- 🎯 **Selectores robustos**: Basados en atributos `data-*` y roles, no en texto o CSS
- 📱 **Login automático**: Detecta automáticamente cuando se completa el escaneo del QR

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/jrivero20/whatsapp_automation.git
```
2. Navega a la carpeta del proyecto:
```bash
cd whatsapp_automation/prueba-tecnica.2.0
```

3. Instala el paquete
```bash
pip install whatsapp-automation
```

### Instalar dependencias de Playwright

```bash
pip install playwright
playwright install chromium
```

## Uso

### Como librería

```python
from whatsapp_automation import send_whatsapp_message

# Forma simple
success = send_whatsapp_message("+1234567890", "¡Hola mundo!")

# Con opciones avanzadas
from whatsapp_automation import WhatsAppAutomation

with WhatsAppAutomation(wait_time=3) as wa:
    wa.send_whatsapp_message("+1234567890", "Mi mensaje")
```

### Desde línea de comandos

```bash
# Uso básico
whatsapp-send +1234567890 "Hola mundo"

# Con opciones
whatsapp-send +1234567890 "Mi mensaje" --wait-time 3
whatsapp-send +1234567890 "Mi mensaje" --headless
```

## Cómo funciona

1. 🌐 Abre WhatsApp Web en el navegador
2. 📱 Muestra el código QR para que escanees
3. 🔍 Detecta automáticamente cuando completas el login
4. 🔒 Oculta el navegador (opcional)
5. 📤 Busca el contacto y envía el mensaje

## Requisitos

- Python 3.8+
- Playwright
- Cuenta de WhatsApp

## Limitaciones

- Requiere escanear QR
- Funciona solo mientras la sesión esté activa
- Respeta los límites de WhatsApp

## Licencia

MIT License
"""