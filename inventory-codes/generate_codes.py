#!/usr/bin/env python3
"""Generate plate QR codes and pipe barcodes from warehouse nomenclature.

Plate:  {column}{row}{stack}     e.g. A11  (col A, row 1, stack #1 of up to 15)
Pipe:   {sandbit}{bin}{layer}{pos} e.g. AA11 (sandbit A, bin A, layer 1, L→R #1)
"""

from __future__ import annotations

import csv
from pathlib import Path

import qrcode
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
from qrcode.constants import ERROR_CORRECT_M

ROOT = Path(__file__).resolve().parent
PLATES_DIR = ROOT / "plates-qr"
PIPES_DIR = ROOT / "pipes-barcode"

PLATES = [
    {"code": "A11", "column": "A", "row": 1, "stack": 1},
    {"code": "A12", "column": "A", "row": 1, "stack": 2},
    {"code": "A13", "column": "A", "row": 1, "stack": 3},
    {"code": "A14", "column": "A", "row": 1, "stack": 4},
    {"code": "A15", "column": "A", "row": 1, "stack": 5},
]

PIPES = [
    {"code": "AA11", "sandbit": "A", "bin": "A", "layer": 1, "position": 1},
    {"code": "AA12", "sandbit": "A", "bin": "A", "layer": 1, "position": 2},
    {"code": "AA13", "sandbit": "A", "bin": "A", "layer": 1, "position": 3},
    {"code": "AA14", "sandbit": "A", "bin": "A", "layer": 1, "position": 4},
    {"code": "AA15", "sandbit": "A", "bin": "A", "layer": 1, "position": 5},
]


def _fonts():
    try:
        return (
            ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22
            ),
            ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14),
        )
    except OSError:
        default = ImageFont.load_default()
        return default, default


def labeled_image(img: Image.Image, title: str, subtitle: str) -> Image.Image:
    pad = 24
    label_h = 72
    w, h = img.size
    out = Image.new("RGB", (w + pad * 2, h + pad + label_h), "white")
    out.paste(img.convert("RGB"), (pad, pad))
    draw = ImageDraw.Draw(out)
    font_big, font_sm = _fonts()
    y = h + pad + 8
    draw.text((pad, y), title, fill=(20, 20, 20), font=font_big)
    draw.text((pad, y + 28), subtitle, fill=(80, 80, 80), font=font_sm)
    return out


def generate_plates() -> list[dict]:
    PLATES_DIR.mkdir(parents=True, exist_ok=True)
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
        labeled = labeled_image(
            img,
            f"PLATE  {p['code']}",
            f"Column {p['column']}  ·  Row {p['row']}  ·  Stack #{p['stack']}/15",
        )
        out_path = PLATES_DIR / f"plate-qr-{p['code']}.png"
        raw_path = PLATES_DIR / f"plate-qr-{p['code']}-raw.png"
        labeled.save(out_path, "PNG")
        img.save(raw_path, "PNG")
        rows.append({**p, "file": out_path.name, "raw_file": raw_path.name, "type": "QR"})
        print(f"QR  {p['code']} -> {out_path.name}")
    return rows


def generate_pipes() -> list[dict]:
    PIPES_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    for pipe in PIPES:
        base = PIPES_DIR / f"pipe-barcode-{pipe['code']}"
        code128 = Code128(pipe["code"], writer=ImageWriter())
        saved = code128.save(
            str(base),
            options={
                "module_width": 0.4,
                "module_height": 18.0,
                "font_size": 14,
                "text_distance": 4,
                "quiet_zone": 4.0,
                "write_text": True,
            },
        )
        img = Image.open(saved)
        labeled = labeled_image(
            img,
            f"PIPE  {pipe['code']}",
            (
                f"Sandbit {pipe['sandbit']}  ·  Bin {pipe['bin']}  ·  "
                f"Layer {pipe['layer']}  ·  Pos {pipe['position']} (L→R)"
            ),
        )
        labeled_path = PIPES_DIR / f"pipe-barcode-{pipe['code']}-labeled.png"
        labeled.save(labeled_path, "PNG")
        rows.append(
            {
                **pipe,
                "file": Path(saved).name,
                "labeled_file": labeled_path.name,
                "type": "Code128",
            }
        )
        print(f"BAR {pipe['code']} -> {Path(saved).name}")
    return rows


def write_manifests(plates: list[dict], pipes: list[dict]) -> None:
    with open(ROOT / "manifest-plates.csv", "w", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=["code", "column", "row", "stack", "type", "file", "raw_file"]
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
                "labeled_file",
            ],
        )
        w.writeheader()
        w.writerows(pipes)


def main() -> None:
    plates = generate_plates()
    pipes = generate_pipes()
    write_manifests(plates, pipes)
    print(f"Wrote {len(plates)} plate QRs and {len(pipes)} pipe barcodes under {ROOT}")


if __name__ == "__main__":
    main()
