# 🤖 Bot de Automatización de WhatsApp (RPA)

Solución profesional de **Robotic Process Automation (RPA)** para WhatsApp Web desarrollada en Python con **Playwright**, equipada con **persistencia de sesión (cookies, IndexedDB y LocalStorage)**, arquitectura modular basada en **Patrones de Diseño de Software** y ejecutable `.bat` listo para Windows.

---

## 🌟 Características Principales

- ✅ **Persistencia de Sesión y Cookies**: Gracias a `launch_persistent_context`, los datos de autenticación (cookies, tokens cifrados e IndexedDB) se guardan localmente en `./session_data`. **Solo necesitas escanear el código QR la primera vez**.
- 📐 **Patrones de Diseño de Software**:
  - **Page Object Model (POM)**: Clases `BasePage`, `LoginPage` y `ChatPage` que aíslan selectores y manipulación del DOM.
  - **Facade Pattern**: `WhatsAppBotFacade` simplifica el flujo completo a una sola llamada de método.
  - **Singleton Pattern**: `SessionManager` centraliza el ciclo de vida del navegador y el perfil de usuario.
  - **Builder / Strategy Pattern**: `MessageBuilder` y `MerzaDesignPatternsStrategy` estructuran de forma flexible el mensaje con el encabezado `"merza"` y el detalle técnico.
- 🚀 **Ejecución con 1 Clic (`.bat`)**: Archivo `ejecutar_bot.bat` para ejecutar en Windows con doble clic; autoverifica dependencias e instala Chromium de ser necesario.
- 🌐 **Selectores Robustos y Multiidioma**: Basados en roles, atributos `data-*` y estructuras visuales, funcionando en inglés, español y otros idiomas.
- 📝 **Configuración Centralizada**: Archivo `config.json` para definir números por defecto, notas y timeouts.

---

## 📐 Patrones de Diseño Implementados

```
                                  +-------------------+
                                  |  ejecutar_bot.bat |
                                  +---------+---------+
                                            |
                                            v
                                  +---------+---------+
                                  |      main.py      |
                                  +---------+---------+
                                            |
                                            v
+-------------------------------------------------------------------------------------------+
|                          PATRÓN FACADE: WhatsAppBotFacade                                 |
|                  Orquesta autenticación, navegación, búsqueda y entrega                   |
+---------------------+---------------------+---------------------+-------------------------+
                      |                     |                     |
                      v                     v                     v
            +-------------------+ +-------------------+ +-------------------+
            | PATRÓN SINGLETON  | |    PATRÓN POM     | | PATRÓN STRATEGY   |
            |  SessionManager   | | - BasePage        | |  MessageBuilder   |
            | - Persistent Data | | - LoginPage       | | - MerzaStrategy   |
            | - Cookies/Storage | | - ChatPage        | | - CustomStrategy  |
            +-------------------+ +-------------------+ +-------------------+
```

1. **Page Object Model (POM)**:
   - `BasePage`: Proporciona métodos resilientes (`find_first_visible`, `safe_click`, `safe_fill`).
   - `LoginPage`: Detecta códigos QR, estados de login y cierra diálogos emergentes.
   - `ChatPage`: Localiza contactos, escribe mensajes respetando saltos de línea y envía.
2. **Facade (Fachada)**:
   - `WhatsAppBotFacade`: Unifica la inicialización del navegador, verificación de login y entrega de mensajes sin exponer detalles de Playwright al usuario.
3. **Singleton (Gestor de Sesión)**:
   - `SessionManager`: Garantiza una única instancia de contexto del navegador persistente en disco.
4. **Builder / Strategy**:
   - `MessageBuilder`: Permite componer el mensaje de la asignación `"merza"` con la documentación técnica de patrones y notas adicionales.

---

## 🚀 Cómo Ejecutar el Bot

### Opción 1: Mediante el ejecutable `.bat` (Recomendado para Escritorio)
Simplemente haz **doble clic** en `ejecutar_bot.bat`.

El archivo `.bat`:
1. Verifica la presencia de Python.
2. Instala automáticamente `playwright` y `playwright install chromium` si faltan.
3. Inicia el bot y solicita el número telefónico por consola si no está en `config.json`.
4. Mantiene abierta la consola para ver los resultados del envío.

### Opción 2: Desde Línea de Comandos (Python)

```bash
# Envío con mensaje predeterminado "merza" + patrones de diseño:
python main.py --phone +584121234567

# Envío con mensaje personalizado:
python main.py --phone +584121234567 --message "Hola mundo"

# Modo interactivo (solicita datos en pantalla):
python main.py
```

### Opción 3: Como Librería Python en tu Código

```python
from whatsapp_automation import WhatsAppBotFacade

# Envío del mensaje "merza" con documentación de patrones:
with WhatsAppBotFacade(headless=False) as bot:
    bot.send_merza_pattern_message("+584121234567")

# Envío de mensaje personalizado:
with WhatsAppBotFacade(headless=False) as bot:
    bot.send_message("+584121234567", "Mensaje de prueba")
```

---

## ⚙️ Archivo de Configuración (`config.json`)

Puedes preconfigurar tu ejecución editando `config.json`:

```json
{
  "phone": "+584121234567",
  "session_dir": "session_data",
  "headless": false,
  "wait_time": 2,
  "message_mode": "merza_patterns",
  "custom_message": "",
  "custom_note": "Entregable RPA con persistencia y patrones de diseño."
}
```

---

## 📁 Estructura del Proyecto

```
RPA/
├── ejecutar_bot.bat                     # Script ejecutable para Windows
├── main.py                              # Entrypoint principal del bot RPA
├── config.json                          # Configuración de ejecución
├── requirements.txt                     # Dependencias de Python
└── whatsapp_automation/
    ├── __init__.py                      # Exportación de clases y facade
    ├── core/
    │   ├── __init__.py
    │   ├── session_manager.py           # Singleton: Persistencia de cookies/sesión
    │   └── bot_facade.py                # Facade: Orquestador RPA
    ├── pages/
    │   ├── __init__.py
    │   ├── base_page.py                 # POM: Clase base y esperas
    │   ├── login_page.py                # POM: Login, QR y modales
    │   └── chat_page.py                 # POM: Búsqueda, chat y envío
    ├── services/
    │   ├── __init__.py
    │   └── message_builder.py           # Builder/Strategy: Formateador "merza" + patrones
    ├── whatsapp_automation.py           # Módulo principal y compatibilidad
    ├── cli.py                           # CLI de comandos
    └── example/
        └── example.py                   # Script de ejemplo interactivo
```

---

## 🔒 Persistencia de Sesión

El bot utiliza el directorio `session_data/` para almacenar el perfil de usuario de Chromium:
- En la **primera ejecución**, el bot esperará a que escanees el código QR con WhatsApp en tu celular.
- En las **siguientes ejecuciones**, el bot cargará directamente la sesión guardada sin solicitar el código QR nuevamente.