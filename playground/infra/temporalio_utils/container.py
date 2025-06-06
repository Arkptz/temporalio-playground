from dependency_injector import providers
from dependency_injector.containers import (
    DeclarativeContainer,
)  # pylint: disable=no-name-in-module
from pydantic_settings import BaseSettings
from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter
from temporalio.runtime import PrometheusConfig, Runtime, TelemetryConfig

from .service import TemporalService
from .settings import parse_env_temporalio_clients


async def get_clients() -> dict[str, Client]:
    # Отключаем Prometheus метрики для избежания конфликта портов
    new_runtime = Runtime(
        telemetry=TelemetryConfig(
            metrics=PrometheusConfig(bind_address="0.0.0.0:9000"),
        ),
    )
    # new_runtime = Runtime(telemetry=TelemetryConfig())
    clients_config = parse_env_temporalio_clients()
    clients = {}
    for client_config in clients_config.values():
        clients[client_config.temporal_namespace] = await Client.connect(
            client_config.temporal_url,
            data_converter=pydantic_data_converter,
            namespace=client_config.temporal_namespace,
            runtime=new_runtime,
            api_key=client_config.temporal_api_key,
            tls=client_config.temporal_tls,
        )
    return clients


def _get_service(clients: dict[str, Client]) -> "TemporalService":
    return TemporalService(temporal_clients=clients)


class TemporalContainer(DeclarativeContainer):
    app_settings: providers.Dependency[BaseSettings] = providers.Dependency()
    clients: providers.ThreadSafeSingleton[dict[str, Client]] = (
        providers.ThreadSafeSingleton(get_clients)
    )
    services: providers.Factory["TemporalService"] = providers.Factory(
        _get_service,
        clients=clients,
    )
