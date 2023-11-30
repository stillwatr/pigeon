import asyncio
import inspect
import logging
import os.path

# ==================================================================================================


class LogStyle:
    """
    TODO
    """
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    RED_BOLD = "\033[31;1m"
    GREEN_BOLD = "\033[32;1m"
    YELLOW_BOLD = "\033[33;1m"
    BLUE_BOLD = "\033[34;1m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    NONE = "\033[0m"


class LogLevel:
    """
    TODO
    """
    ERROR = logging.ERROR
    WARN = logging.WARNING
    FOCUS = logging.INFO + 1
    INFO = logging.INFO
    DEBUG = logging.DEBUG


logging.addLevelName(LogLevel.FOCUS, "FOCUS")

# ==================================================================================================


class ConsoleLogFormat:
    """
    TODO
    """
    WITH_FILE_NAME_AND_LINE_NUM = f"%(asctime)s %(xstyle)s[%(levelname)s]{LogStyle.NONE} {LogStyle.ITALIC}%(xname)s:%(xline)d{LogStyle.NONE} - %(message)s"  # noqa


class ConsoleLogFormatter(logging.Formatter):
    """
    TODO
    """
    def __init__(self, format: str) -> None:
        """
        TODO
        """
        self.log_format = format

    def format(self, record) -> str:
        """
        TODO
        """
        msg = self.format_message(record)
        context = self.format_context(record)
        return f"{msg}{context}"

    def format_message(self, record: logging.LogRecord) -> str:
        """
        TODO
        """
        return logging.Formatter(self.log_format).format(record)

    def format_context(self, record) -> str:
        """
        TODO
        """
        if not record.args:
            return ""

        if not isinstance(record.args, dict):
            return ""

        context = "; ".join([f"{k}: {v}" for k, v in record.args.items()])

        return f" | {context}"


class ConsoleLogHandler(logging.StreamHandler):
    """
    TODO
    """

    def __init__(self, format: str = ConsoleLogFormat.WITH_FILE_NAME_AND_LINE_NUM):
        """
        TODO
        """
        super().__init__()
        self.formatter = ConsoleLogFormatter(format)

# ==================================================================================================


class TelegramLogFormat:
    """
    TODO
    """
    XXX = "%(message)s"


class TelegramLogFormatter(logging.Formatter):
    """
    TODO
    """
    def __init__(self, format: str) -> None:
        """
        TODO
        """
        self.log_format = format

    def format(self, record) -> str:
        """
        TODO
        """
        msg = self.format_message(record)
        context = self.format_context(record)
        return f"{msg}{context}"

    def format_message(self, record) -> str:
        """
        TODO
        """
        return logging.Formatter(self.log_format).format(record)

    def format_context(self, record) -> str:
        """
        TODO
        """
        if not record.args:
            return ""

        if not isinstance(record.args, dict):
            return ""

        context = "\n".join([f"{k}: {v}" for k, v in record.args.items()])

        return f"\n{context}"


class TelegramLogHandler(logging.Handler):
    """
    TODO
    """

    def __init__(self, bot, to_chat_id: int, format: str = TelegramLogFormat.XXX):
        """
        TODO
        """
        super().__init__()
        self.bot = bot
        self.to_chat_id = to_chat_id
        self.formatter = TelegramLogFormatter(format)

    def emit(self, record):
        """
        TODO
        """
        asyncio.get_event_loop().create_task(self.emit_async(self.formatter.format(record)))

    async def emit_async(self, message: str):
        """
        TODO
        """
        await self.bot.send_message(self.to_chat_id, message)

# ==================================================================================================


class Log:
    """
    TODO
    """

    def __init__(
            self,
            name: str,
            level: int = logging.INFO,
            handlers: list[logging.Handler] = []) -> None:
        """
        TODO
        """
        self.log = logging.getLogger(name)
        self.log.setLevel(level)
        for handler in handlers:
            self.log.addHandler(handler)

    # ----------------------------------------------------------------------------------------------

    def set_level(self, level: int):
        """
        TODO
        """
        self.log.setLevel(level)

    def add_handler(self, handler: logging.Handler) -> None:
        """
        TODO
        """
        self.log.addHandler(handler)

    # ----------------------------------------------------------------------------------------------

    def error(self, msg: str, print_stacktrace: bool = True, context: dict = {}):
        """
        TODO
        """
        if context:
            self.log.error(
                msg,
                context,
                extra=self.get_code_location(style=LogStyle.RED_BOLD),
                exc_info=print_stacktrace
            )
        else:
            self.log.error(
                msg,
                extra=self.get_code_location(style=LogStyle.RED_BOLD),
                exc_info=print_stacktrace
            )

    def warn(self, msg: str, context: dict = {}):
        """
        TODO
        """
        if context:
            self.log.warn(msg, context, extra=self.get_code_location(style=LogStyle.YELLOW_BOLD))
        else:
            self.log.warn(msg, extra=self.get_code_location(style=LogStyle.YELLOW_BOLD))

    def focus(self, msg: str, context: dict = {}):
        """
        TODO
        """
        if context:
            self.log._log(
                LogLevel.FOCUS,
                msg,
                context,
                extra=self.get_code_location(style=LogStyle.BLUE_BOLD)
            )
        else:
            self.log._log(
                LogLevel.FOCUS,
                msg,
                extra=self.get_code_location(style=LogStyle.BLUE_BOLD)
            )

    def info(self, msg: str, context: dict = {}):
        """
        TODO
        """
        if context:
            self.log.info(msg, context, extra=self.get_code_location(style=LogStyle.BLUE_BOLD))
        else:
            self.log.info(msg, extra=self.get_code_location(style=LogStyle.BLUE_BOLD))

    def debug(self, msg: str, context: dict = {}):
        """
        TODO
        """
        if context:
            self.log.debug(msg, context, extra=self.get_code_location(style=LogStyle.BOLD))
        else:
            self.log.debug(msg, extra=self.get_code_location(style=LogStyle.BOLD))

    # ----------------------------------------------------------------------------------------------

    def get_code_location(self, style: str):
        """
        TODO
        """
        c = inspect.getframeinfo(inspect.stack()[2][0])
        return {
            "xname": os.path.splitext(os.path.basename(c.filename))[0],
            "xline": c.lineno,
            "xstyle": style
        }
