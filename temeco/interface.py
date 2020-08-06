from abc import ABC, abstractmethod


class Entity(ABC):  # pragma: no cover
    """
    An interface representing a Telegram message entity.
    """
    @abstractmethod
    def offset(self) -> int:
        """
        :return: entity offset (int)
        """
        pass

    @abstractmethod
    def length(self) -> int:
        """
        :return: entity length (int)
        """
        pass

    @abstractmethod
    def as_html_str(self) -> str:
        """
        :return: an HTML version of the entity offset (str)
        """
        pass


class EncodingAwareText(ABC):   # pragma: no cover
    """
    An interface representing Telegram message with utf-16 encoding awareness
    """
    @abstractmethod
    def text_of(self, start: int, stop: int = None) -> str:
        """
        start - start index
        stop - stop index.
        Only positive indices supported.
        :return: slice the text with the given indices.
        If stop=None then then the slice ends at the end of the string
        """
        pass

    @abstractmethod
    def entity_text(self, entity: Entity) -> str:
        """
        A shortcut for text_of method.
        :return: an HTML version of the entity offset (str)
        """
        pass
