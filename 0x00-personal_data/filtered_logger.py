#!/usr/bin/env python3
"""Obfuscate"""
import logging
import re
from typing import List, Tuple


PII_FIELDS: Tuple[str, str, str, str, str] = ('name', 'email',
                                              'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Return the log message obfuscated"""
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)

    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records"""
        message = super(RedactingFormatter, self).format(record)
        redacted = filter_datum(self.fields, self.REDACTION,
                                message, self.SEPARATOR)
        return redacted


def get_logger(self) -> logging.Logger:
    """Create a logger"""
    # create logger
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    # create handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter
    formatter = RedactingFormatter(PII_FIELDS)
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)

    return logger
