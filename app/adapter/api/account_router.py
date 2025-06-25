from datetime import date
import os
import json

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response

from app.domain.service.report_service import ReportService
from app.adapter.get_dsp2_api import get_dsp2_api
from app.domain.service.dsp2_service import Dsp2Service
from app.adapter.serializers.account_serializer import AccountSerializer
from app.domain.service.account_consistency_validator import AccountConsistencyValidator

router = APIRouter()


def get_dsp2_service():
    dsp2_api = get_dsp2_api()
    username = os.getenv("USERNAME", "")
    password = os.getenv("PASSWORD", "")
    return Dsp2Service(dsp2_api, username, password)


def get_report_service():
    dsp2_service = get_dsp2_service()
    return ReportService(dsp2_service)


dsp2_api = get_dsp2_api()


@router.get("", response_model=dict)
async def get_account(dsp2_service: Dsp2Service = Depends(get_dsp2_service)):
    try:
        account = dsp2_service.get_accounts()
        account_json = [AccountSerializer.to_dict(account) for account in account]
        return Response(content=account_json, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting account: {str(e)}")


@router.get("/{account_id}/report/json", response_model=dict)
async def get_report_json(
    account_id: str,
    date_start: date,
    date_end: date,
    report_service: ReportService = Depends(get_report_service),
):
    try:
        report = report_service.generate_report_json(account_id, date_start, date_end)

        return Response(content=report, media_type="application/json")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating report: {str(e)}"
        )


@router.get("/{account_id}/report/csv")
async def get_report_csv(
    account_id: str,
    date_start: date,
    date_end: date,
    report_service: ReportService = Depends(get_report_service),
):
    try:
        csv_content = report_service.generate_report_csv(
            account_id, date_start, date_end
        )

        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=account_consistency_report.csv"
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating CSV report: {str(e)}"
        )


@router.get("/consistency")
async def get_consistency(
    dsp2_service: Dsp2Service = Depends(get_dsp2_service),
):
    try:
        consistency = AccountConsistencyValidator.validate(dsp2_service)
        return Response(content=json.dumps(consistency), media_type="application/json")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting consistency: {str(e)}"
        )
