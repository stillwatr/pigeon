import logging
import traceback

from inspect import getframeinfo, stack
from os.path import basename, splitext
from typing import Optional

# ==================================================================================================

# TODO
BOLD: str = "\033[1m"   # bold
IT: str = "\033[3m"     # italic
RB: str = "\033[31;1m"  # red+bold
GB: str = "\033[32;1m"  # green+bold
YB: str = "\033[33;1m"  # yellow+bold
BB: str = "\033[34;1m"  # blue+bold
R: str = "\033[31m"     # red
G: str = "\033[32m"     # green
Y: str = "\033[33m"     # yellow
B: str = "\033[34m"     # blue
N: str = "\033[0m"      # none

# TODO
FORMAT: str = f"%(asctime)s %(xformat)s[%(levelname)s]{N} {IT}%(xname)s:%(xline)d{N} - %(message)s"

# TODO
DEBUG: int = logging.DEBUG
INFO: int = logging.INFO
SUCCESS: int = logging.INFO + 1
WARN: int = logging.WARN
ERROR: int = logging.ERROR

class LogFormatter(logging.Formatter):
    """
    TODO
    """
    def format(self, record):
        """
        TODO
        """
        return logging.Formatter(FORMAT).format(record)

# ==================================================================================================

logger = logging.getLogger("telegram_bot")
handler = logging.StreamHandler()
handler.setFormatter(LogFormatter())
logger.addHandler(handler)

logging.addLevelName(SUCCESS, "SUCCESS")

# ==================================================================================================

def set_level(level: int):
    """
    TODO
    """
    logger.setLevel(level)

def get_extra(format: str):
    """
    TODO
    """
    c = getframeinfo(stack()[2][0])
    return {"xname": splitext(basename(c.filename))[0], "xline": c.lineno, "xformat": format }

# ==================================================================================================

def error(msg: str, ex: Optional[BaseException]=None):
    """
    TODO
    """
    logger.error(msg, extra=get_extra(format=RB))
    if ex:
        debug(f"Traceback:\n{''.join(traceback.format_exception(ex))}")


def warn(msg: str):
    """
    TODO
    """
    logger.warn(msg, extra=get_extra(format=YB))


def success(msg: str):
    """
    TODO
    """
    logger._log(SUCCESS, msg, args=None, extra=get_extra(format=GB))


def info(msg: str):
    """
    TODO
    """
    logger.info(msg, extra=get_extra(format=BB))


def debug(msg: str):
    """
    TODO
    """
    logger.debug(msg, extra=get_extra(format=BOLD))
