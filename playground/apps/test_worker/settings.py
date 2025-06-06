from dotenv import load_dotenv

from infra.temporalio_utils.settings import TemporalioWorkerSettings

load_dotenv()

WIRE_MODULES: list[str] = []


class Settings(TemporalioWorkerSettings):
    pass
