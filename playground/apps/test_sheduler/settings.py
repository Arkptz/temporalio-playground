from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

WIRE_MODULES: list[str] = []


class Settings(BaseSettings):
    # Scheduler settings
    scheduler_task_queue: str = "benchmark"
    scheduler_namespace: str = "default"
    scheduler_concurrency: int = 10
    scheduler_total_workflows: int = 100
    scheduler_message: str = "Test scheduler"

    # Infinite mode settings
    scheduler_infinite_mode: bool = False
    scheduler_report_interval: int = 10  # seconds
    scheduler_max_runtime: int = 0  # 0 = infinite, >0 = max seconds to run
