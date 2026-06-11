"""
src package - ETL Job and Database utilities
"""

__version__ = "1.0.0"
__author__ = "Data Engineering Student"

from .config import DB_CONFIG
from .utils import (
    get_db_connection,
    log_message,
    validate_email,
    validate_phone
)
from .etl_job import ETLJob
from .query_data import DataAnalyzer

__all__ = [
    'DB_CONFIG',
    'get_db_connection',
    'log_message',
    'validate_email',
    'validate_phone',
    'ETLJob',
    'DataAnalyzer'
]
