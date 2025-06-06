from dependency_injector import providers
from dependency_injector.containers import (  # pylint: disable=no-name-in-module
    DeclarativeContainer,
)
from tasks.activities import echo
from tasks.workflows import EchoWorkflow
from temporalio.client import Client
from temporalio.worker import Worker

from infra.temporalio_utils.container import TemporalContainer

from .settings import Settings


def get_temporal_worker(
    app_settings: Settings,
    temporal_clients: dict[str, Client],
) -> Worker:
    return Worker(
        task_queue=app_settings.temporal_worker_task_queue,
        client=temporal_clients[app_settings.temporal_worker_namespace],
        workflows=[EchoWorkflow],
        activities=[echo],
        **app_settings.temporal_worker_settings(),
    )


class AppContainer(DeclarativeContainer):
    app_settings: providers.ThreadSafeSingleton[Settings] = (
        providers.ThreadSafeSingleton(Settings)
    )
    temporal_container: providers.Container[TemporalContainer] = providers.Container(
        TemporalContainer,
        app_settings=app_settings,
    )

    temporal_worker: providers.ThreadSafeSingleton[Worker] = (
        providers.ThreadSafeSingleton(
            get_temporal_worker,
            temporal_clients=temporal_container.clients,
            app_settings=app_settings,
        )
    )
