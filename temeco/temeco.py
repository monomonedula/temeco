from itertools import zip_longest
from typing import List

from temeco.interface import Entity, EncodingAwareText


class BasicEntity(Entity):
    """
    A class representing a Telegram message entity.
    Supporting the following entity types:
     - `bold`
     - `italic`
     - `text_link`
     - `code` (monospace text)
     - `pre` (preformatted text)
    """
    def __init__(
        self,
        msg_text: "EncodingAwareText",
        offset: int,
        length: int,
        type: str,
        data: dict = None,
    ):
        self._offset = offset
        self._len = length
        self._type = type
        self._msg = msg_text
        self._data = data or {}

    def offset(self) -> int:
        """
        :return: entity offset (int)
        """
        return self._offset

    def length(self) -> int:
        """
        :return: entity length (int)
        """
        return self._len

    def as_html_str(self,) -> str:
        """
        :return: an HTML version of the entity offset (str)
        If the entity type isn't supported, the entity text is returned untouched.
        """
        if self._type == "bold":
            return f"<b>{self._msg.entity_text(self)}</b>"
        elif self._type == "italic":
            return f"<i>{self._msg.entity_text(self)}</i>"
        elif self._type == "pre":
            return f"<pre>{self._msg.entity_text(self)}</pre>"
        elif self._type == "text_link":
            return f'<a href="{self._data["url"]}">{self._msg.entity_text(self)}</a>'
        elif self._type == "code":
            return f"<code>{self._msg.entity_text(self)}</code>"
        return self._msg.entity_text(self)


class TelegramUTF16Text(EncodingAwareText):
    """
    A class representing Telegram message with utf-16 encoding awareness
    """
    def __init__(self, txt: str):
        self._utf16_txt = txt.encode("utf-16-le")

    def text_of(self, start: int, stop: int = None):
        """
        start - start index
        stop - stop index.
        Only positive indices supported.
        :return: slice the text with the given indices.
        If stop=None then then the slice ends at the end of the string
        """
        if stop is None:
            stop = len(self._utf16_txt) // 2
        return self._utf16_txt[start * 2 : stop * 2].decode("utf-16-le")

    def entity_text(self, entity: Entity):
        """
        A shortcut for text_of method.
        :return: an HTML version of the entity offset (str)
        """
        return self.text_of(entity.offset(), entity.offset() + entity.length())


class HtmlFromMsg:
    """
    A class for entities to HTML translation
    """
    def __init__(self, msg_txt: "EncodingAwareText", entities: List[Entity]):
        self._txt = msg_txt
        self._entities = entities

    def as_str(self) -> str:
        """
        :return: HTML version of the original message
        """
        subs = []
        for e in self._entities:
            subs.append(e.as_html_str())
        txt_split = []
        prev = 0
        for e in self._entities:
            txt_split.append(self._txt.text_of(prev, e.offset()))
            prev = e.offset() + e.length()
        txt_split.append(self._txt.text_of(prev))
        return "".join([t + s for t, s in zip_longest(txt_split, subs, fillvalue="")])
