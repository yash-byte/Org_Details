# Inventory Codes — Plates (QR) & Pipes (Barcode)

Printable identification codes for warehouse plates and pipes.

## Nomenclature

### Plate — QR code `{column}{row}{stack}`

| Part | Meaning | Example |
|------|---------|---------|
| Letter | Column | `A` |
| 1st digit | Row | `1` |
| 2nd digit(s) | Plate count in stack (1–15) | `1` … `15` |

Examples: `A11` = column A, row 1, plate #1 · `A115` = column A, row 1, plate #15

### Pipe — Barcode (Code128) `{sandbit}{bin}{layer}{position}`

| Part | Meaning | Example |
|------|---------|---------|
| 1st letter | Sandbit | `A` |
| 2nd letter | Bin | `A` |
| 1st digit | Layer | `1` |
| 2nd digit | Pipe left → right | `1` |

Examples: `AA11` = sandbit A, bin A, layer 1, pipe #1 (leftmost)

## Generated set (this folder)

### 5 plate QR codes

| Code | Meaning | Files |
|------|---------|-------|
| `A11` | Col A · Row 1 · Stack #1 | `plates-qr/plate-qr-A11.png` (+ `-raw.png`) |
| `A12` | Col A · Row 1 · Stack #2 | `plates-qr/plate-qr-A12.png` |
| `A13` | Col A · Row 1 · Stack #3 | `plates-qr/plate-qr-A13.png` |
| `A14` | Col A · Row 1 · Stack #4 | `plates-qr/plate-qr-A14.png` |
| `A15` | Col A · Row 1 · Stack #5 | `plates-qr/plate-qr-A15.png` |

### 5 pipe barcodes

| Code | Meaning | Files |
|------|---------|-------|
| `AA11` | Sandbit A · Bin A · Layer 1 · Pos 1 | `pipes-barcode/pipe-barcode-AA11.png` |
| `AA12` | Sandbit A · Bin A · Layer 1 · Pos 2 | `pipes-barcode/pipe-barcode-AA12.png` |
| `AA13` | Sandbit A · Bin A · Layer 1 · Pos 3 | `pipes-barcode/pipe-barcode-AA13.png` |
| `AA14` | Sandbit A · Bin A · Layer 1 · Pos 4 | `pipes-barcode/pipe-barcode-AA14.png` |
| `AA15` | Sandbit A · Bin A · Layer 1 · Pos 5 | `pipes-barcode/pipe-barcode-AA15.png` |

Labeled variants (`*-labeled.png`) include a human-readable field breakdown under the barcode.

## Regenerate

```bash
pip install 'qrcode[pil]' python-barcode pillow
python3 generate_codes.py
```

Open `print-sheet.html` in a browser to print all 10 codes on one page.
