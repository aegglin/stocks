import logging

log = logging.getLogger(__name__)


def get_log(name=__name__, is_debug=False):

    level = logging.DEBUG if is_debug else logging.INFO
    logger = logging.getLogger(name)
    logging.basicConfig(level=level, format="{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M",)

    console_handler = logging.StreamHandler()
    # file_handler = logging.FileHandler(f"{name}.log", mode="a", encoding="utf-8")

    logger.addHandler(console_handler)
    # logger.addHandler(file_handler)

    return logger


    