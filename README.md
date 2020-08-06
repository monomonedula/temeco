# Telegram Message Copy (TeMeCo)

[![EO principles respected here](https://www.elegantobjects.org/badge.svg)](https://www.elegantobjects.org)
[![Build Status](https://travis-ci.org/monomonedula/temeco.svg?branch=master)](https://travis-ci.org/monomonedula/temeco)
[![codecov](https://codecov.io/gh/monomonedula/temeco/branch/master/graph/badge.svg)](https://codecov.io/gh/monomonedula/temeco)
[![PyPI version](https://badge.fury.io/py/temeco.svg)](https://badge.fury.io/py/temeco)

`temeco` is a simple Telegram message entities to html translator.
Telegram Bot API makes it cumbersome fro bots to copy a user's message
preserving its entities, since it is currently impossible for a bot to send
entities directly along with a message, 
so it needs to translate a message with entities into HTML or Markdown.

This little package solves this problem and provides a convenient way
to translate a message with entities to HTML. 

`TelegramUTF16Text` class is also aware of the fact that Telegram calculates
 offsets for entities using UTF-16 encoding. 
 This comes into play when text being copied contains symbols which have different lengths
 in UTF-8 and UTF-16 code units, like emojis.
 
 ## Installation
 `pip install temeco`
 
 ## Usage:
 ```python
from temeco.temeco import BasicEntity, TelegramUTF16Text, HtmlFromMsg

text = (
    "dolorem ipsum, quia dolor sit, 🔥🚒 amet, consectetur, adipisci velit, sed quia 🙃 non numquam eius modi"
    " tempora incidunt, 🙊\nut labore et dolore magnam aliquam quaerat voluptatem."
)
HtmlFromMsg(
    msg_txt=TelegramUTF16Text(text),
    entities=[
        BasicEntity(
            type="bold", offset=8, length=5, msg_text=TelegramUTF16Text(text)
        ),
        BasicEntity(
            type="code", offset=55, length=8, msg_text=TelegramUTF16Text(text)
        ),
        BasicEntity(
            type="text_link",
            offset=64,
            length=5,
            data={"url": "http://google.com/"},
            msg_text=TelegramUTF16Text(text),
        ),
        BasicEntity(
            type="italic",
            offset=153,
            length=7,
            msg_text=TelegramUTF16Text(text),
        ),
    ],
).as_str()
```
 
 ## Note:
 `BasicEntity` class supports the following types of entities:
 - `bold`
 - `italic`
 - `text_link`
 - `code` (monospace text)
 - `pre` (preformatted text)

Entities like hashtags and usernames are copied as is, since Telegram recognizes them
without extra code.

You may create your own class implementing `Entity` interface and use it instead of 
BasicEntity.
 