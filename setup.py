from setuptools import setup

setup(
    name="pigeon",
    version="0.1.0",
    description="A package with classes commonly required for implementing Telegram bots.",
    author="Cedric Stillwater",
    author_email="cedric.stillwater@gmail.com",
    packages=["pigeon"],
    install_requires=[
      "asyncio>=3.4.3",
      "ImageHash>=4.3.1",
      "python-telegram-bot>=20.6",
      "Telethon>=1.31.1",
      "tg-file-id>=0.0.4"
    ]
)
