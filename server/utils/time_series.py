from itertools import groupby

from dateutil.relativedelta import relativedelta


def group_util(date, min_date):
    return (date - min_date).days // 31


def group_metric_by_month(dates, total_months, min_date, monotonic=True):
    """Group given list of dates by month."""
    if not dates:
        return []

    dates_grouped = []
    dates.sort()

    for key, val in groupby(dates, key=lambda date: group_util(date, min_date)):
        # Keep only months that are >= 0
        if key >= 0:
            dates_grouped.append((key, list(val)))

    time_series_cumulative_by_month = []
    metric_counter = 0
    dates_grouped_idx = 0
    grouped_months_count = len(dates_grouped)
    for month_idx in range(total_months):
        if (
            dates_grouped_idx < grouped_months_count
            and month_idx == dates_grouped[dates_grouped_idx][0]
        ):
            if monotonic:
                metric_counter += len(dates_grouped[dates_grouped_idx][1])
            else:
                metric_counter = len(dates_grouped[dates_grouped_idx][1])
            dates_grouped_idx += 1

        time_series_cumulative_by_month.append(
            (min_date + relativedelta(months=month_idx), metric_counter)
        )

    return time_series_cumulative_by_month


def group_size_by_month(dates, size_values, total_months, min_date, monotonic=True):
    """Group given list of size metric dates and values by month."""
    if not dates:
        return []

    values_by_date = {dates[i]: size_values[i] for i in range(len(dates))}

    dates_grouped = []
    dates.sort()

    for key, val in groupby(dates, key=lambda date: group_util(date, min_date)):
        # Keep only months that are >= 0
        if key >= 0:
            dates_grouped.append((key, list(val)))

    time_series_cumulative_by_month = []
    metric_counter = 0
    dates_grouped_idx = 0
    grouped_months_count = len(dates_grouped)
    for month_idx in range(total_months):
        if (
            dates_grouped_idx < grouped_months_count
            and month_idx == dates_grouped[dates_grouped_idx][0]
        ):
            month_counter = 0
            for month_date in dates_grouped[dates_grouped_idx][1]:
                month_counter += values_by_date[month_date]

            if monotonic:
                metric_counter += month_counter
            else:
                metric_counter = month_counter

            dates_grouped_idx += 1

        time_series_cumulative_by_month.append(
            (min_date + relativedelta(months=month_idx), metric_counter)
        )

    return time_series_cumulative_by_month
