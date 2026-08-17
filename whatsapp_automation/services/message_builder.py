"""
Módulo de Servicios: Constructor de Mensajes (Builder & Strategy Pattern)
Responsable de formatear y construir el mensaje de reporte técnico con la documentación
de los patrones de diseño, datos del desarrollador (Jose Rivero) y enlace al repositorio.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import datetime


class IMessageStrategy(ABC):
    """Interfaz para la estrategia de construcción de mensajes (Patrón Strategy)."""
    
    @abstractmethod
    def build(self, **kwargs) -> str:
        """Construye el contenido del mensaje como cadena de texto."""
        pass


class TechnicalReportStrategy(IMessageStrategy):
    """
    Estrategia de mensaje para el reporte técnico de la solución RPA,
    incluyendo el saludo a Merza, autor, repositorio y desglose de patrones de diseño.
    """
    
    def __init__(self, patterns: Optional[List[Dict[str, str]]] = None):
        self.patterns = patterns or [
            {
                "name": "Page Object Model (POM)",
                "type": "Estructural / UI Automation",
                "desc": "Separa la lógica de automatización de los selectores web (BasePage, LoginPage, ChatPage)."
            },
            {
                "name": "Facade Pattern (Fachada)",
                "type": "Estructural",
                "desc": "WhatsAppBotFacade ofrece una interfaz unificada y de alto nivel que oculta la complejidad interna de Playwright."
            },
            {
                "name": "Singleton Pattern",
                "type": "Creacional",
                "desc": "SessionManager centraliza la gestión del perfil de usuario, cookies de sesión e IndexedDB en disco."
            },
            {
                "name": "Builder / Strategy Pattern",
                "type": "Creacional / Comportamiento",
                "desc": "MessageBuilder desacopla la construcción y parametrización de mensajes dinámicos."
            }
        ]

    def build(self, **kwargs) -> str:
        recipient = kwargs.get("recipient", "Merza")
        developer = kwargs.get("developer", "Jose Rivero")
        repo_url = kwargs.get("repo_url", "https://github.com/jrivero20/whatsapp_automation")
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        lines = [
            f"Hola {recipient},",
            "",
            "🤖 *BOT DE AUTOMATIZACIÓN WHATSAPP (RPA)*",
            f"👤 *Desarrollador:* {developer}",
            f"🔗 *Repositorio:* {repo_url}",
            f"📅 _Ejecución automatizada: {timestamp}_",
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "📐 *PATRONES DE DISEÑO IMPLEMENTADOS*",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            ""
        ]
        
        for idx, pattern in enumerate(self.patterns, 1):
            lines.append(f"*{idx}. {pattern['name']}* [{pattern['type']}]")
            lines.append(f"   ↳ {pattern['desc']}")
            lines.append("")
            
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append("✅ *Persistencia de Sesión:* Cookies, LocalStorage e IndexedDB guardados en perfil local.")
        lines.append("🚀 *Entregable:* Ejecutable interactivo `.bat` para escritorio.")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        custom_note = kwargs.get("custom_note")
        if custom_note:
            lines.append("")
            lines.append(f"📝 *Nota adicional:* {custom_note}")
            
        return "\n".join(lines)


class CustomMessageStrategy(IMessageStrategy):
    """Estrategia para enviar mensajes de texto libres personalizados."""
    
    def build(self, **kwargs) -> str:
        text = kwargs.get("text", "Hola Merza")
        return text


class MessageBuilder:
    """
    Patrón Builder para configurar y producir mensajes para el Bot de WhatsApp.
    """
    
    def __init__(self, strategy: Optional[IMessageStrategy] = None):
        self._strategy: IMessageStrategy = strategy or TechnicalReportStrategy()
        self._params: Dict[str, any] = {}

    def set_strategy(self, strategy: IMessageStrategy) -> "MessageBuilder":
        self._strategy = strategy
        return self

    def set_recipient(self, recipient: str) -> "MessageBuilder":
        self._params["recipient"] = recipient
        return self

    def set_developer(self, developer: str) -> "MessageBuilder":
        self._params["developer"] = developer
        return self

    def set_repo_url(self, repo_url: str) -> "MessageBuilder":
        self._params["repo_url"] = repo_url
        return self

    def set_custom_note(self, note: str) -> "MessageBuilder":
        self._params["custom_note"] = note
        return self

    def set_text(self, text: str) -> "MessageBuilder":
        self._params["text"] = text
        return self

    def add_custom_param(self, key: str, value: any) -> "MessageBuilder":
        self._params[key] = value
        return self

    def build(self) -> str:
        """Genera el mensaje final formateado."""
        return self._strategy.build(**self._params)


def create_technical_report_message(
    recipient: str = "Merza",
    developer: str = "Jose Rivero",
    repo_url: str = "https://github.com/jrivero20/whatsapp_automation",
    custom_note: Optional[str] = None
) -> str:
    """Función de conveniencia para construir el reporte técnico completo."""
    builder = MessageBuilder(TechnicalReportStrategy())
    builder.set_recipient(recipient)
    builder.set_developer(developer)
    builder.set_repo_url(repo_url)
    if custom_note:
        builder.set_custom_note(custom_note)
    return builder.build()
