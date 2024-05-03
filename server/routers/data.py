from math import ceil

from fastapi import APIRouter, HTTPException

from server.connection import mo
from server.utils.data import (
    get_stargazers_time_series,
    get_metrics_information,
    get_metric_time_series,
    get_releases_time_series,
    get_size_time_series,
)
from server.utils.time_series import group_metric_by_month, group_size_by_month

# Initialize the router
router = APIRouter()


@router.get("/data/repository/")
def get_repositories_names():
    """Get all repositories names in the DB"""
    repositories = mo.db["repositories_data"].find(
        {"statistics": {"$exists": True}}, {"_id": 0, "full_name": 1}
    )
    repositories_names = [repository["full_name"] for repository in repositories]
    return {"data": repositories_names}


@router.get("/data/repository/{repository_owner}/{repository_name}/")
def get_repository_information(repository_owner: str, repository_name: str):
    """Get information for the given repository"""
    repository_full_name = f"{repository_owner}/{repository_name}"

    repository = mo.db["repositories_data"].find_one(
        {"statistics": {"$exists": True}, "full_name": repository_full_name}, {"_id": 0}
    )
    if not repository:
        raise HTTPException(
            status_code=404, detail=f"{repository_full_name} not found in the database"
        )

    return {"data": repository}


@router.get("/data/repository/{repository_owner}/{repository_name}/metrics/")
def get_repository_metrics(repository_owner: str, repository_name: str):
    """Get metrics data for the given repository"""
    repository_full_name = f"{repository_owner}/{repository_name}"

    repository = mo.db["repositories_data"].find_one(
        {"statistics": {"$exists": True}, "full_name": repository_full_name}
    )
    if not repository:
        raise HTTPException(
            status_code=404, detail=f"{repository_full_name} not found in the database"
        )

    repository_age_months = ceil(repository["age"] / 2629746)
    repository_age_start = repository["created_at"].replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )

    stargazers_dates, _ = get_stargazers_time_series(repository)

    releases_dates, _ = get_releases_time_series(repository)

    time_series_dates = {
        "stargazers": stargazers_dates,
        "releases": releases_dates,
    }

    for metric in get_metrics_information():
        metric_dates, _ = get_metric_time_series(
            repository,
            metric[0],
            metric[1],
            metric[2],
            metric[3],
        )

        time_series_dates[metric[1]] = metric_dates

    time_series_metrics_by_month = {}
    for metric, metric_dates in time_series_dates.items():
        metric_by_month = group_metric_by_month(
            metric_dates, repository_age_months, repository_age_start
        )
        time_series_metrics_by_month[metric] = metric_by_month

    (
        repository_actions_dates,
        repository_actions_total,
        _,
    ) = get_size_time_series(repository)
    time_series_dates["size"] = repository_actions_dates
    size_by_month = group_size_by_month(
        repository_actions_dates,
        repository_actions_total,
        repository_age_months,
        repository_age_start,
    )
    time_series_metrics_by_month["size"] = size_by_month

    return {"data": time_series_metrics_by_month}
