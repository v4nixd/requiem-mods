from __future__ import annotations

import os
import typing

import yaml

from dotenv import load_dotenv


class Config:
    instance: Config | None = None

    CONFIG_FILE = "config.yaml"

    def __init__(self) -> None:
        load_dotenv()

        assert os.path.exists(Config.CONFIG_FILE)

        with open(Config.CONFIG_FILE, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

    @staticmethod
    def get_instance() -> Config:
        if not Config.instance:
            Config.instance = Config()
        return Config.instance

    def get_config(self) -> typing.Any:
        return self.config

    def get_env_var(self, envvar: str) -> str:
        if envvar not in os.environ:
            raise ValueError(f"Please set the {envvar} environment variable")
        return os.environ[envvar]
