from datetime import timezone

import pytest
from iso8601 import ParseError
from jinja2 import Environment


def test_basic():
    env = Environment(extensions=["jinja2_iso8601.ISO8601Extension"])
    template = env.from_string(
        """
        no filter: {{ datestr }}
        parsed: {{ datestr|parse_date }}
        formatted: {{ datestr|parse_date|format_date("%a, %b %d %Y (%Z)") }}
    """
    )
    datestr = "2022-09-19T14:38:34.213001"
    result = template.render(datestr=datestr)
    expected = """
        no filter: 2022-09-19T14:38:34.213001
        parsed: 2022-09-19 14:38:34.213001
        formatted: Mon, Sep 19 2022 ()
    """
    assert result == expected


def test_default_utc():
    env = Environment(extensions=["jinja2_iso8601.ISO8601Extension"])
    env.default_timezone = timezone.utc
    template = env.from_string(
        """
        no filter: {{ datestr }}
        parsed: {{ datestr|parse_date }}
        formatted: {{ datestr|parse_date|format_date("%a, %b %d %Y (%Z)") }}
    """
    )
    datestr = "2022-09-19T14:38:34.213001"
    result = template.render(datestr=datestr)
    expected = """
        no filter: 2022-09-19T14:38:34.213001
        parsed: 2022-09-19 14:38:34.213001+00:00
        formatted: Mon, Sep 19 2022 (UTC)
    """
    assert result == expected


def test_invalid_datestr():
    env = Environment(extensions=["jinja2_iso8601.ISO8601Extension"])
    template = env.from_string(
        """
        no filter: {{ datestr }}
        parsed: {{ datestr|parse_date }}
        formatted: {{ datestr|parse_date|format_date("%a, %b %d %Y") }}
    """
    )
    with pytest.raises(ParseError):
        template.render(datestr="purple")


def test_no_format_string():
    env = Environment(extensions=["jinja2_iso8601.ISO8601Extension"])
    template = env.from_string(
        """
        no filter: {{ datestr }}
        parsed: {{ datestr|parse_date }}
        formatted: {{ datestr|parse_date|format_date }}
    """
    )
    datestr = "2022-09-19T14:38:34.213001"
    with pytest.raises(TypeError) as err:
        template.render(datestr=datestr)
    assert (
        str(err.value)
        == "format_date() missing 1 required positional argument: 'format'"
    )
