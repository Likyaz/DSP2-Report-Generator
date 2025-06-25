from app.adapter.dsp2_api_adapter import Dsp2ApiAdapter
from app.domain.port.dsp2_client import Dsp2Client


def get_dsp2_api() -> Dsp2Client:
    return Dsp2ApiAdapter()
