"Adds `parse_date` and `format_date` filters to Jinja."
__version__ = "1.0.0"

from datetime import date, datetime, time

import iso8601
from jinja2 import Environment, pass_environment
from jinja2.ext import Extension


@pass_environment
def parse_date(environment: Environment, datestring: str):
    return iso8601.parse_date(
        datestring=datestring, default_timezone=environment.default_timezone
    )


def format_date(dt: date | time | datetime, format: str):
    return dt.strftime(format)


class ISO8601Extension(Extension):
    def __init__(self, environment: Environment):
        super().__init__(environment)
        environment.extend(default_timezone=None)
        environment.filters["parse_date"] = parse_date
        environment.filters["format_date"] = format_date
