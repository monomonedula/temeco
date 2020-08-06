from abc import ABC, abstractmethod


class Entity(ABC):  # pragma: no cover
    @abstractmethod
    def offset(self) -> int:
        pass

    @abstractmethod
    def length(self) -> int:
        pass

    @abstractmethod
    def as_html_str(self) -> str:
        pass


class EncodingAwareText(ABC):   # pragma: no cover
    @abstractmethod
    def text_of(self, start: int, stop: int = None) -> str:
        pass

    @abstractmethod
    def entity_text(self, entity: Entity) -> str:
        pass
