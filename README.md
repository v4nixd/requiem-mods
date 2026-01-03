# Disnake Template

---

## Overview

**Disnake Bot Template** is a professional, production-ready Discord bot starter designed to help you launch new bots quickly with a consistent and scalable foundation.

It focuses on eliminating repetitive setup while keeping the codebase clean, extensible, and easy to host.

| Feature              | Description                                                                 |
| -------------------- | --------------------------------------------------------------------------- |
| Python 3.14          | Latest Python version with modern language features and async-first design  |
| Disnake              | Powerful and flexible Discord API wrapper for building bots                 |
| uv                   | Ultra-fast Python package manager and virtual environment tool              |
| Modular Architecture | Clean separation of core logic, cogs, services, and utilities               |
| Config System        | Environment variables via `python-dotenv` and structured YAML configuration |
| Logging Setup        | Centralized and configurable logging for debugging and production           |
| Error Handling       | Global exception handling for commands and background tasks                 |
| Docker-ready         | Prepared for Docker to simplify deployment and hosting                      |
| Reusable Template    | Designed to be reused across multiple bots without rewriting the core       |

## Useful commands

install dependencies

```bash
uv sync
```

run bot

```bash
uv run -m src.main
```

ruff

```bash
uv run ruff check
uv run ruff format
```

isort

```bash
uv run isort .
```

pyright

```bash
uv run pyright
```
