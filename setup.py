from setuptools import setup

setup(
    name="telegram_commons",
    version="0.1.0",
    description="A package with classes commonly required for implementing Telegram bots.",
    author="Claudius Korzen",
    author_email="cldskrzn@gmail.com",
    packages=["telegram_commons"],
    install_requires=["python-telegram-bot>=20.2",
                      "Telethon>=1.28.5",
                      "asyncio>=3.4.3"]
)
