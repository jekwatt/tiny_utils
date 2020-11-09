#!/usr/bin/env python3

class TsvDialect(csv.Dialect):
    """Standard Unix-style TSV format."""

    delimiter = "\t"
    doublequote = False
    escapechar = "\\"
    lineterminator = "\n"
    extrasaction = "ignore"
    quotechar = '"'
    quoting = csv.QUOTE_MINIMAL
    skipinitialspace = False


def normalize_name(field_name):
    """lowercase with underscores, etc"""
    fixes = (
        (r"/", "_per_"),
        (r"%", "_pct_"),
        (r"\W", "_"),
        (r"^_+", ""),  # remove '_' if field_name begins with '_'
        (r"_+$", ""),
        (r"__+", "_"),
    )
    result = field_name.strip().lower() or None
    # result = field_name.strip().upper() or None
    if result:
        if result.endswith("?"):
            if not re.match(r"is[_\W]", result):
                result = "is_" + result
        for pattern, replacement in fixes:
            result = re.sub(pattern, replacement, result)
    return result


# Fix date format
def ymd_to_mdy(date_str, default=None):
    """
    2020-07-14 19:40:09 -> 7/14/2020  # assay_timestamp
    1987-03-11 -> 3/11/1987  # dob
    2020-07-14 -> 7/14/2020  # report_date
    8/31/2020 -> 8/31/2020  # report_date (manual entry)
    2020-07-13 08:40 -> 7/13/2020  # requisition_finished
    2020-07-13 12:05 -> 7/13/2020  # collection_datetime
    2020-07-13T12:05 -> 7/13/2020  # in case
    NaN -> ""
    nan -> ""
    "" -> ""
    "date-of-on is never" -> ValueError
    "2020-99-01 is never" -> ValueError
    "2020-02-30 is never" -> ValueError
    d: datetime.date(2019, 12, 4)  # datetime.date format
    """
    if date_str.lower() in ["nan", ""]:
        return default
    d = parser.parse(date_str).date()
    return f"{d.month}/{d.day}/{d.year}"
    # return f"{d.month:02d}/{d.day:02d}/{d.year}
