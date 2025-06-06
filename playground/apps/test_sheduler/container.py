from dependency_injector import providers
from dependency_injector.containers import (  # pylint: disable=no-name-in-module
    DeclarativeContainer,
)
from services.scheduler.container import SchedulerContainer

from infra.temporalio_utils.container import TemporalContainer

from .settings import Settings


class AppContainer(DeclarativeContainer):
    app_settings: providers.ThreadSafeSingleton[Settings] = (
        providers.ThreadSafeSingleton(Settings)
    )
    temporal_container: providers.Container[TemporalContainer] = providers.Container(
        TemporalContainer,
        app_settings=app_settings,
    )

    scheduler_container: providers.Container[SchedulerContainer] = providers.Container(
        SchedulerContainer,
        temporal_container=temporal_container,
        app_settings=app_settings,
    )
