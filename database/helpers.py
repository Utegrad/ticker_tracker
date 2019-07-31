import logging

from decimal import Decimal, InvalidOperation

from .exceptions import InvalidDecimalRecordDataException

logger = logging.getLogger(__name__)


def decimal_from_string(str):
    try:
        return Decimal(str)
    except InvalidOperation as e:
        logger.warning(f"Invalid Decimal string: {str}")
        raise InvalidDecimalRecordDataException
    except Exception as e:
        logger.warning(f"Invalid Decimal string: {str}")
        raise e
