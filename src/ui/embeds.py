from disnake import Embed, Colour


def success_embed(msg: str, desc: str | None = None, **kwargs) -> Embed:
    return Embed(title=msg, description=desc, colour=Colour.green(), **kwargs)


def error_embed(error_msg: str, **kwargs) -> Embed:
    return Embed(
        title="Ошибка!",
        description=error_msg,
        colour=Colour.red(),
        **kwargs
    )
