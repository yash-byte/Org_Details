#!/usr/bin/env python3
"""Generate unlabeled plate QR codes and pipe barcodes, then pack into a PDF.

Plate:  {column}{row}-{stack}      e.g. A1-1  (col A, row 1, stack #1 of up to 15)
Pipe:   {sandbit}{bin}{layer}{pos} e.g. AA11  (sandbit A, bin A, layer 1, L→R #1)
"""

from __future__ import annotations

import csv
import shutil
from pathlib import Path

import qrcode
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image
from qrcode.constants import ERROR_CORRECT_M
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
PLATES_DIR = ROOT / "plates-qr"
PIPES_DIR = ROOT / "pipes-barcode"
PDF_PATH = ROOT / "inventory-codes.pdf"

PLATES = [
    {"code": "A1-1", "column": "A", "row": 1, "stack": 1},
    {"code": "A1-2", "column": "A", "row": 1, "stack": 2},
    {"code": "A1-3", "column": "A", "row": 1, "stack": 3},
    {"code": "A1-4", "column": "A", "row": 1, "stack": 4},
    {"code": "A1-5", "column": "A", "row": 1, "stack": 5},
]

PIPES = [
    {"code": "AA11", "sandbit": "A", "bin": "A", "layer": 1, "position": 1},
    {"code": "AA12", "sandbit": "A", "bin": "A", "layer": 1, "position": 2},
    {"code": "AA13", "sandbit": "A", "bin": "A", "layer": 1, "position": 3},
    {"code": "AA14", "sandbit": "A", "bin": "A", "layer": 1, "position": 4},
    {"code": "AA15", "sandbit": "A", "bin": "A", "layer": 1, "position": 5},
]


def reset_dirs() -> None:
    for d in (PLATES_DIR, PIPES_DIR):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)


def generate_plates() -> list[dict]:
    rows: list[dict] = []
    for p in PLATES:
        qr = qrcode.QRCode(
            version=1,
            error_correction=ERROR_CORRECT_M,
            box_size=12,
            border=2,
        )
        qr.add_data(p["code"])
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        out_path = PLATES_DIR / f"plate-qr-{p['code']}.png"
        img.save(out_path, "PNG")
        rows.append({**p, "file": out_path.name, "type": "QR"})
        print(f"QR  {p['code']} -> {out_path.name}")
    return rows


def generate_pipes() -> list[dict]:
    rows: list[dict] = []
    for pipe in PIPES:
        base = PIPES_DIR / f"pipe-barcode-{pipe['code']}"
        code128 = Code128(pipe["code"], writer=ImageWriter())
        saved = code128.save(
            str(base),
            options={
                "module_width": 0.4,
                "module_height": 18.0,
                "font_size": 0,
                "text_distance": 1,
                "quiet_zone": 4.0,
                "write_text": False,
            },
        )
        # Crop any leftover text margin so the PNG is barcode-only
        img = Image.open(saved).convert("RGB")
        # python-barcode still leaves bottom padding when write_text=False; trim white edges
        bbox = Image.eval(img.convert("L"), lambda px: 255 - px).getbbox()
        if bbox:
            # keep a small quiet-zone padding
            left, top, right, bottom = bbox
            pad = 8
            left = max(0, left - pad)
            top = max(0, top - pad)
            right = min(img.width, right + pad)
            bottom = min(img.height, bottom + pad)
            img = img.crop((left, top, right, bottom))
            img.save(saved, "PNG")
        rows.append({**pipe, "file": Path(saved).name, "type": "Code128"})
        print(f"BAR {pipe['code']} -> {Path(saved).name}")
    return rows


def write_manifests(plates: list[dict], pipes: list[dict]) -> None:
    with open(ROOT / "manifest-plates.csv", "w", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=["code", "column", "row", "stack", "type", "file"]
        )
        w.writeheader()
        w.writerows(plates)

    with open(ROOT / "manifest-pipes.csv", "w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "code",
                "sandbit",
                "bin",
                "layer",
                "position",
                "type",
                "file",
            ],
        )
        w.writeheader()
        w.writerows(pipes)


def build_pdf(plates: list[dict], pipes: list[dict]) -> None:
    """One-page PDF: 5 unlabeled plate QRs + 5 unlabeled pipe barcodes (images only)."""
    c = canvas.Canvas(str(PDF_PATH), pagesize=A4)
    page_w, page_h = A4
    margin = 18 * mm

    qr_size = 32 * mm
    gap = 5 * mm
    total_w = 5 * qr_size + 4 * gap
    x0 = (page_w - total_w) / 2
    y_qr = page_h - margin - qr_size

    for i, p in enumerate(plates):
        x = x0 + i * (qr_size + gap)
        c.drawImage(
            str(PLATES_DIR / p["file"]),
            x,
            y_qr,
            width=qr_size,
            height=qr_size,
            preserveAspectRatio=True,
            mask="auto",
        )

    bar_w = 34 * mm
    bar_h = 18 * mm
    total_bar_w = 5 * bar_w + 4 * gap
    x0b = (page_w - total_bar_w) / 2
    y_bar = y_qr - 25 * mm - bar_h

    for i, pipe in enumerate(pipes):
        x = x0b + i * (bar_w + gap)
        c.drawImage(
            str(PIPES_DIR / pipe["file"]),
            x,
            y_bar,
            width=bar_w,
            height=bar_h,
            preserveAspectRatio=True,
            mask="auto",
        )

    c.showPage()
    c.save()
    print(f"PDF -> {PDF_PATH.name}")


def main() -> None:
    reset_dirs()
    plates = generate_plates()
    pipes = generate_pipes()
    write_manifests(plates, pipes)
    build_pdf(plates, pipes)
    print(f"Wrote {len(plates)} plate QRs and {len(pipes)} pipe barcodes under {ROOT}")


if __name__ == "__main__":
    main()
