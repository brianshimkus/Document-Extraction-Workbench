import argparse
import base64
import json
import os
import time
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from contracts import Invoice

load_dotenv()
FIELDS = ["vendor", "invoice_number", "date", "currency", "total"]


def read_pages(path):
    # Implement this function in the matching tutorial lesson.
    raise NotImplementedError("Complete read_pages in the tutorial")


def normalize(name, value):
    # Implement this function in the matching tutorial lesson.
    raise NotImplementedError("Complete normalize in the tutorial")


def validate_record(invoice, pages, vision=False):
    # Implement this function in the matching tutorial lesson.
    raise NotImplementedError("Complete validate_record in the tutorial")


def extract_live(path, pages, vision=False, client=None):
    # Implement this function in the matching tutorial lesson.
    raise NotImplementedError("Complete extract_live in the tutorial")


def run(path, mode="mock", vision=False):
    start = time.perf_counter()
    pages = read_pages(path)
    if mode == "mock":
        fixture = Path("data/mock") / (Path(path).stem + ".json")
        invoice = Invoice.model_validate_json(fixture.read_text())
        usage = {}
    elif mode == "live":
        invoice, usage = extract_live(path, pages, vision)
    else:
        raise ValueError("mode must be mock or live")
    checked = validate_record(invoice, pages, vision)
    return {
        "file": str(path),
        "mode": mode,
        "vision": vision,
        "raw": invoice.model_dump(),
        **checked,
        "usage": usage,
        "latency_ms": round((time.perf_counter() - start) * 1000, 2),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--mode", choices=["mock", "live"], default="mock")
    parser.add_argument("--vision", action="store_true")
    args = parser.parse_args()
    result = run(args.path, args.mode, args.vision)
    Path("output").mkdir(exist_ok=True)
    target = Path("output") / (Path(args.path).stem + "-" + args.mode + ".json")
    target.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
