from datetime import datetime, timedelta


def generate_nearby_dates(selected_date: str, days_range: int) -> list[str]:
    """
    Generate nearby dates before and after the selected date.

    Example:
        selected_date = "2026-07-30"
        days_range = 3

    Output:
        ["2026-07-27", "2026-07-28", ..., "2026-08-02"]
    """

    try:
        date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format, for example: 2026-07-30")

    if days_range < 0:
        raise ValueError("Range must be 0 or greater")

    dates = []

    for i in range(-days_range, days_range + 1):
        new_date = date_obj + timedelta(days=i)
        dates.append(new_date.strftime("%Y-%m-%d"))

    return dates
