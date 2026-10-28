"""FastAPI web calculator with input validation and operation/error logging."""

import logging
import math
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from operations import add, divide, multiply, power, root, subtract

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("calculator")
logger.setLevel(logging.INFO)
if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler(LOG_DIR / "calculator.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

app = FastAPI(title="Module 8 FastAPI Calculator", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

OPERATIONS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
    "power": power,
    "root": root,
}


class CalculationRequest(BaseModel):
    operation: str = Field(..., description="The math operation to perform")
    a: float = Field(..., description="First number")
    b: float = Field(..., description="Second number (root degree for root)")


class CalculationResponse(BaseModel):
    operation: str
    a: float
    b: float
    result: float


@app.get("/", response_class=HTMLResponse)
def home():
    """Display the calculator website."""
    return (BASE_DIR / "templates" / "index.html").read_text(encoding="utf-8")


@app.get("/health")
def health():
    """Show that the application is running."""
    return {"status": "ok"}


@app.get("/operations")
def list_operations():
    """List the available mathematical operations."""
    return {"operations": list(OPERATIONS)}


@app.post("/calculate", response_model=CalculationResponse)
def calculate(request: CalculationRequest):
    """Calculate a result and record success/errors in the log."""
    operation = request.operation.lower().strip()
    operation_function = OPERATIONS.get(operation)
    if operation_function is None:
        logger.warning("Unsupported operation requested: %s", request.operation)
        raise HTTPException(status_code=400, detail="Unsupported operation")
    if not math.isfinite(request.a) or not math.isfinite(request.b):
        logger.warning("Non-finite numbers submitted")
        raise HTTPException(status_code=400, detail="Numbers must be finite")
    try:
        result = operation_function(request.a, request.b)
        if not math.isfinite(result):
            raise ValueError("Result must be a finite real number")
    except (ValueError, OverflowError, ZeroDivisionError) as exc:
        logger.warning("Calculation failed: %s(%s, %s): %s", operation, request.a, request.b, exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    logger.info("Calculated %s(%s, %s) = %s", operation, request.a, request.b, result)
    return CalculationResponse(operation=operation, a=request.a, b=request.b, result=result)
