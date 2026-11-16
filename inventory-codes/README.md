# Inventory Codes — Plates (QR) & Pipes (Barcode)

Unlabeled identification codes for warehouse plates and pipes.  
**Printable PDF:** [`inventory-codes.pdf`](inventory-codes.pdf)

## Nomenclature

### Plate — QR `{column}{row}-{stack}`

| Part | Meaning | Example |
|------|---------|---------|
| Letter | Column | `A` |
| Digits before `-` | Row | `1` |
| Digits after `-` | Plate count in stack (1–15) | `1` … `15` |

Examples: `A1-1` = column A, row 1, plate #1 · `A1-15` = column A, row 1, plate #15

### Pipe — Barcode (Code128) `{sandbit}{bin}{layer}{position}`

| Part | Meaning | Example |
|------|---------|---------|
| 1st letter | Sandbit | `A` |
| 2nd letter | Bin | `A` |
| 1st digit | Layer | `1` |
| 2nd digit | Pipe left → right | `1` |

Examples: `AA11` = sandbit A, bin A, layer 1, pipe #1 (leftmost)

## Generated set

### 5 plate QR codes (no label overlay)

| Code | File |
|------|------|
| `A1-1` | `plates-qr/plate-qr-A1-1.png` |
| `A1-2` | `plates-qr/plate-qr-A1-2.png` |
| `A1-3` | `plates-qr/plate-qr-A1-3.png` |
| `A1-4` | `plates-qr/plate-qr-A1-4.png` |
| `A1-5` | `plates-qr/plate-qr-A1-5.png` |

### 5 pipe barcodes (no human-readable text under bars)

| Code | File |
|------|------|
| `AA11` | `pipes-barcode/pipe-barcode-AA11.png` |
| `AA12` | `pipes-barcode/pipe-barcode-AA12.png` |
| `AA13` | `pipes-barcode/pipe-barcode-AA13.png` |
| `AA14` | `pipes-barcode/pipe-barcode-AA14.png` |
| `AA15` | `pipes-barcode/pipe-barcode-AA15.png` |

## Regenerate

```bash
pip install 'qrcode[pil]' python-barcode pillow reportlab
python3 generate_codes.py
```

This rewrites the PNGs and `inventory-codes.pdf`.
