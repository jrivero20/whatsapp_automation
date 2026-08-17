"""
Módulo de Servicios: Constructor de Mensajes (Builder & Strategy Pattern)
Responsable de formatear y construir el mensaje que contiene 'merza'
y la documentación técnica de los patrones de diseño utilizados en el bot.
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


class MerzaDesignPatternsStrategy(IMessageStrategy):
    """
    Estrategia de mensaje que incluye 'merza' y la explicación detallada
    de los patrones de diseño de software utilizados en la solución RPA.
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
        header = kwargs.get("header", "merza")
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        lines = [
            f"*{header}*",
            "",
            "🤖 *BOT DE AUTOMATIZACIÓN WHATSAPP (RPA)*",
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
        text = kwargs.get("text", "merza")
        return text


class MessageBuilder:
    """
    Patrón Builder para configurar y producir mensajes para el Bot de WhatsApp.
    """
    
    def __init__(self, strategy: Optional[IMessageStrategy] = None):
        self._strategy: IMessageStrategy = strategy or MerzaDesignPatternsStrategy()
        self._params: Dict[str, any] = {}

    def set_strategy(self, strategy: IMessageStrategy) -> "MessageBuilder":
        self._strategy = strategy
        return self

    def set_header(self, header: str) -> "MessageBuilder":
        self._params["header"] = header
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


def create_merza_pattern_message(custom_note: Optional[str] = None) -> str:
    """Función de conveniencia para construir el mensaje predeterminado con 'merza' y los patrones."""
    builder = MessageBuilder(MerzaDesignPatternsStrategy())
    if custom_note:
        builder.set_custom_note(custom_note)
    return builder.build()
