from fastapi import APIRouter, Depends, Query
from typing import List
from services.data_service import get_data
from core.security import verify_token

router = APIRouter()

# Declaring the route data
@router.get("/data")
def read_data(
    start: str,
    end: str,
    variables: List[str] = Query(...),
    credentials = Depends(verify_token),
):
    return get_data(start, end, variables)