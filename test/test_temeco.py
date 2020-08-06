from temeco.temeco import BasicEntity, TelegramUTF16Text, HtmlFromMsg


def test_entities_utf16_awareness():
    """
    🙈 symbol has length of 2 in utf-16 and length of 1 in utf-8
    """
    txt = "hello!\n🙈 foo bla"
    e1 = BasicEntity(msg_text=TelegramUTF16Text(txt), offset=0, length=6, type="bold")
    assert e1.length() == 6
    assert e1.offset() == 0
    assert e1.as_html_str() == "<b>hello!</b>"

    e2 = BasicEntity(msg_text=TelegramUTF16Text(txt), type="bold", offset=14, length=3)
    assert e2.offset() == 14
    assert e2.length() == 3
    assert e2.as_html_str() == "<b>bla</b>"


def test_html_from_text():
    """
    Should translate the message with entities into an html message.
    The offsets correspond to the utf-16 version of the original text,
     as if it was a real telegram message with entities.
    """
    text = (
        "dolorem ipsum, quia dolor sit, 🔥🚒 amet, consectetur, adipisci velit, sed quia 🙃 non numquam eius modi"
        " tempora incidunt, 🙊\nut labore et dolore magnam aliquam quaerat voluptatem."
    )
    assert (
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
        == "dolorem <b>ipsum</b>, quia dolor sit, 🔥🚒 amet, consectetur, "
        '<code>adipisci</code> <a href="http://google.com/">velit</a>, sed quia 🙃 non '
        "numquam eius modi tempora incidunt, 🙊\n"
        "ut labore et dolore magnam <i>aliquam</i> quaerat voluptatem."
    )
