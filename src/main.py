from __future__ import annotations

from src.bot import Bot
from src.config import Config
from src.utils import Utils


class Main:
    instance: Main | None = None

    def __init__(self) -> None:
        self.bot = Bot(reload=True)

    @staticmethod
    def get_instance() -> Main:
        if not Main.instance:
            Main.instance = Main()
        return Main.instance


if __name__ == "__main__":
    main = Main.get_instance()
    bot = main.bot.client
    config = Config.get_instance()
    TOKEN = config.get_env_var("DISCORD_TOKEN")
    Utils.load_cogs(bot)
    bot.run(TOKEN)
