# Jinja2-ISO8601

Adds `parse_date` and `format_date` filters to Jinja.
The [`iso8601`](https://github.com/micktwomey/pyiso8601) module handles date parsing,
hence the name of this project. The
[`.strftime()`](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior)
method handles date formatting.

## Install

First install the Python module:

```bash
pip install jinja2-iso8601
```

Then add the extension into your Jinja environment:

```python
from jinja2 import Environment

jinja_env = Environment(extensions=['jinja2_iso8601.ISO8601Extension'])
```

## Use

You can now use two new filters when writing your Jinja templates:
`parse_date` and `format_date`.
`parse_date` will turn an ISO-8601 formatted string into a
[Python `datetime`](https://docs.python.org/3/library/datetime.html#datetime-objects) object.
`format_date` will call the `.strftime()` method on whatever you pass to it;
this works well with `datetime`, `date`, and `time` objects. You'll need to
provide a format string for the `format_date` filter;
[check the Python documentation for how to write a format string](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).

For example, let's say you have a variable called `datestr` which is
a string representing a datetime in valid ISO-8601 format, such as
`"2022-09-19T14:38:34.213001"`. You can write your Jinja template like this:

```jinja
no filter: {{ datestr }}
parsed: {{ datestr|parse_date }}
formatted: {{ datestr|parse_date|format_date("%a, %b %d %Y") }}
```

and the rendered result will be:

```
no filter: 2022-09-19T14:38:34.213001
parsed: 2022-09-19 14:38:34.213001
formatted: Mon, Sep 19 2022
```

## Timezones

In Python, date and time objects may include timezone information.
Date and time objects that have an associated timezone are "aware", and
those that do not have an associated timezone are "naive".

By default, when parsing ISO-8601 strings without any timezone information,
the result is a "naive" datetime object. However, in some cases, you may
want to assume a default timezone, so that you always get an "aware"
datetime object even if no timezone is specified. For example, if you know
that the ISO-8601 string is in the UTC timezone, you may want the
`parse_date` filter to return an "aware" datetime with the UTC timezone.

The `default_timezone` value on the Jinja environment controls which
timezone to use when none is specified in the string. By default, this
value is `None`, which makes `parse_date` return a "naive" datetime.
Here's how to make all datetimes parse as UTC:

```python
from datetime import timezone
from jinja2 import Environment

jinja_env = Environment(extensions=['jinja2_iso8601.ISO8601Extension'])
jinja_env.default_timezone = timezone.utc
```

## See Also

These filters can be paired with other Jinja filters that process datetimes,
such as [`jinja2_humanize_extension`](https://github.com/metwork-framework/jinja2_humanize_extension).
You can parse strings into datetime using the `parse_date` filter from this
project, and then "humanize" the datetime using the `humanize_naturalday` filter
from `jinja2_humanize_extension`. They work together seamlessly!
