from dependency_injector import providers
from dependency_injector.containers import (  # pylint: disable=no-name-in-module
    DeclarativeContainer,
)
from pydantic_settings import BaseSettings

from infra.temporalio_utils.container import TemporalContainer, TemporalService

from .service import SchedulerService


def _get_scheduler_service(
    temporal_service: "TemporalService",
    app_settings: BaseSettings,
) -> SchedulerService:
    return SchedulerService(
        temporal_service=temporal_service,
        task_queue=app_settings.scheduler_task_queue,
        namespace=app_settings.scheduler_namespace,
        concurrency=app_settings.scheduler_concurrency,
        report_interval=app_settings.scheduler_report_interval,  # type: ignore
    )


class SchedulerContainer(DeclarativeContainer):
    app_settings: providers.Dependency = providers.Dependency()
    temporal_container: providers.Container[TemporalContainer] = providers.Container(
        TemporalContainer,
    )

    scheduler_service: providers.Factory[SchedulerService] = providers.Factory(
        _get_scheduler_service,
        temporal_service=temporal_container.services,
        app_settings=app_settings,
    )
