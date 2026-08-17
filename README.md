# 🤖 Bot de Automatización de WhatsApp (RPA)

Solución profesional de **Robotic Process Automation (RPA)** para WhatsApp Web desarrollada en Python con **Playwright**, equipada con **persistencia de sesión (cookies, IndexedDB y LocalStorage)**, arquitectura modular basada en **Patrones de Diseño de Software** y ejecutable `.bat` listo para Windows.

---

## 🌟 Características Principales

- ✅ **Persistencia de Sesión y Cookies**: Gracias a `launch_persistent_context`, los datos de autenticación (cookies, tokens cifrados e IndexedDB) se guardan localmente en `./session_data`. **Solo necesitas escanear el código QR la primera vez**.
- 📐 **Patrones de Diseño de Software**:
  - **Page Object Model (POM)**: Clases `BasePage`, `LoginPage` y `ChatPage` que aíslan selectores y manipulación del DOM.
  - **Facade Pattern**: `WhatsAppBotFacade` simplifica el flujo completo a una sola llamada de método.
  - **Singleton Pattern**: `SessionManager` centraliza el ciclo de vida del navegador y el perfil de usuario.
  - **Builder / Strategy Pattern**: `MessageBuilder` y `TechnicalReportStrategy` estructuran de forma flexible el reporte técnico con el saludo a Merza, datos del autor (Jose Rivero), enlace al repositorio y detalle de patrones.
- 🚀 **Ejecución con 1 Clic (`.bat`)**: Archivo `ejecutar_bot.bat` para Windows; autoverifica y crea el entorno virtual aislado `.venv`, instala dependencias e instala Chromium automáticamente.
- 🌐 **Interacción 100% por Interfaz (UI)**: Basada en selectores exactos del DOM (`data-testid`, `data-tab`, roles accesibles y editor Lexical), funcionando independientemente del tema (modo claro/oscuro) y del destinatario (números o nombres).
- 📝 **Configuración Centralizada**: Archivo `config.json` para definir destinatario por defecto, notas y timeouts.

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
            | - Persistent Data | | - LoginPage       | | - TechReportStrat |
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
   - `MessageBuilder`: Permite componer el reporte técnico de patrones y notas adicionales de forma modular.

---

## 🚀 Cómo Ejecutar el Bot

### Opción 1: Mediante el ejecutable `.bat` (Recomendado para Escritorio)
Simplemente haz **doble clic** en `ejecutar_bot.bat`.

El archivo `.bat`:
1. Detecta o crea automáticamente el entorno virtual aislado `.venv`.
2. Instala automáticamente `playwright` y `playwright install chromium` si faltan.
3. Inicia el bot y solicita el contacto o número de teléfono por consola si no está en `config.json`.
4. Mantiene abierta la consola para ver los resultados del envío.

### Opción 2: Desde Línea de Comandos (Python)

```bash
# Envío con Reporte Técnico predeterminado:
python main.py --phone +584121234567

# Envío con mensaje personalizado:
python main.py --phone +584121234567 --message "Hola mundo"

# Modo interactivo (solicita datos en pantalla):
python main.py
```

### Opción 3: Como Librería Python en tu Código

```python
from whatsapp_automation import WhatsAppBotFacade

# Envío del reporte técnico de patrones de diseño:
with WhatsAppBotFacade(headless=False) as bot:
    bot.send_technical_report("+584121234567")

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
  "message_mode": "technical_report",
  "recipient": "Merza",
  "developer": "Jose Rivero",
  "repo_url": "https://github.com/jrivero20/whatsapp_automation",
  "custom_message": "",
  "custom_note": "Entregable RPA con persistencia y patrones de diseño."
}
```

---

## 📁 Estructura del Proyecto

```
whatsapp_automation/
├── .git/                                # Repositorio Git
├── .gitignore                           # Exclusión de .venv y session_data
├── ejecutar_bot.bat                     # Script ejecutable para Windows
├── main.py                              # Entrypoint principal del bot RPA
├── config.json                          # Configuración de ejecución
├── requirements.txt                     # Dependencias de Python
├── setup.py / pyproject.toml            # Empaquetado y metadatos
├── tests/
│   └── test_bot.py                      # Suite de pruebas unitarias
├── example/
│   └── example.py                       # Script de ejemplo interactivo
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
    └── services/
        ├── __init__.py
        └── message_builder.py           # Builder/Strategy: Reporte técnico
```

---

## 🔒 Persistencia de Sesión

El bot utiliza el directorio `session_data/` para almacenar el perfil de usuario de Chromium:
- En la **primera ejecución**, el bot esperará a que escanees el código QR con WhatsApp en tu celular.
- En las **siguientes ejecuciones**, el bot cargará directamente la sesión guardada sin solicitar el código QR nuevamente.