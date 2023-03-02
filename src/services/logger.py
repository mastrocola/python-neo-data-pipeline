import logging
from src.services.shared.singleton_meta import SingletonMeta
from src.settings import PROJECT


class Log(metaclass=SingletonMeta):
    def __init__(self):
        self.logger = logging.getLogger(PROJECT)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

    def __log(self, level, code, message, error=None):
        args = dict(level=logging.getLevelName(level), code=code.upper(), message=message)

        if error is not None:
            args['error'] = error

        self.logger.log(level, args)

    def error(self, code, message, error=None):
        self.__log(logging.ERROR, code, message, error)

    def info(self, code, message):
        self.__log(logging.INFO, code, message)

    def warning(self, code, message):
        self.__log(logging.WARNING, code, message)
