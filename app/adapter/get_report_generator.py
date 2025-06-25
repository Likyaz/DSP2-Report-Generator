from app.domain.port.report_generator import ReportGenerator
from app.adapter.report_generator_pandas import ReportGeneratorPandas


def get_report_generator() -> ReportGenerator:
    return ReportGeneratorPandas()
