import logging
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from temporalio.worker import (
    ResourceBasedSlotConfig,
    ResourceBasedSlotSupplier,
    ResourceBasedTunerConfig,
    WorkerTuner,
)

log = logging.getLogger(__name__)


class TemporalioClientSettings(BaseSettings):
    temporal_url: str = Field(examples=["localhost:7233"])
    temporal_namespace: str = Field(default="default", examples=["default"])
    temporal_api_key: str | None = Field(default=None, examples=["1234567890"])
    temporal_tls: bool = Field(default=False, examples=[True, False])


class TemporalioWorkerSettings(BaseSettings):
    temporal_worker_namespace: str = Field(examples=["default"])
    temporal_worker_task_queue: str = Field(examples=["default"])
    temporal_worker_target_cpu: float = Field(default=0.9, examples=[0.9])
    temporal_worker_target_ram: float = Field(default=0.8, examples=[0.8])
    temporal_worker_workflows_min_slots: int = Field(default=10, examples=[10])
    temporal_worker_workflows_max_slots: int = Field(default=500, examples=[500])
    temporal_worker_activities_min_slots: int = Field(default=50, examples=[50])
    temporal_worker_activities_max_slots: int = Field(default=500, examples=[500])
    temporal_worker_local_activities_min_slots: int = Field(default=50, examples=[50])
    temporal_worker_local_activities_max_slots: int = Field(default=500, examples=[500])
    temporal_worker_max_concurrent_workflow_task_polls: int = Field(
        default=100,
        examples=[100],
    )
    temporal_worker_max_concurrent_activity_task_polls: int = Field(
        default=100,
        examples=[100],
    )
    temporal_worker_nonsticky_to_sticky_poll_ratio: float = Field(
        default=0.8,
        examples=[0.8],
    )

    def temporal_worker_settings(self):
        resource_based_options = ResourceBasedTunerConfig(
            self.temporal_worker_target_cpu,
            self.temporal_worker_target_ram,
        )
        tuner = WorkerTuner.create_composite(
            workflow_supplier=ResourceBasedSlotSupplier(
                ResourceBasedSlotConfig(
                    minimum_slots=self.temporal_worker_workflows_min_slots,
                    maximum_slots=self.temporal_worker_workflows_max_slots,
                ),
                resource_based_options,
            ),
            activity_supplier=ResourceBasedSlotSupplier(
                ResourceBasedSlotConfig(
                    minimum_slots=self.temporal_worker_activities_min_slots,
                    maximum_slots=self.temporal_worker_activities_max_slots,
                ),
                resource_based_options,
            ),
            local_activity_supplier=ResourceBasedSlotSupplier(
                ResourceBasedSlotConfig(
                    minimum_slots=self.temporal_worker_local_activities_min_slots,
                    maximum_slots=self.temporal_worker_activities_max_slots,
                ),
                resource_based_options,
            ),
        )
        return {
            "tuner": tuner,
            # "build_id": self.app_version,
            "max_concurrent_workflow_task_polls": self.temporal_worker_max_concurrent_workflow_task_polls,
            "max_concurrent_activity_task_polls": self.temporal_worker_max_concurrent_activity_task_polls,
            "nonsticky_to_sticky_poll_ratio": self.temporal_worker_nonsticky_to_sticky_poll_ratio,
        }


def parse_env_temporalio_clients(
    storage: dict[str, str] = os.environ,
) -> dict[str, TemporalioClientSettings]:  # type: ignore
    result: dict[str, TemporalioClientSettings] = {}
    prefixes: set[str] = set()
    for key in storage:
        _key = key.upper()
        if "TEMPORAL_URL" in _key:
            prefix = _key.split("TEMPORAL_URL")[0]
            if len(prefix) < 20:
                prefixes.add(prefix)
    log.info(f"Success find {len(prefixes)} temporalio clients. {prefixes}")
    for prefix in prefixes:
        # human_prefix = prefix.lower()

        class PrefixedSettings(TemporalioClientSettings):
            model_config = SettingsConfigDict(env_prefix=prefix)

        settings = PrefixedSettings()  # type: ignore
        result[settings.temporal_namespace] = settings
    return result
