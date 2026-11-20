"""Org Details web service — serves organization name, address, and employees."""

from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request

# Repo root (parent of web_service/) holds name.txt, address.txt, employees.txt
DATA_DIR = Path(os.environ.get("ORG_DATA_DIR", Path(__file__).resolve().parent.parent))

FIELD_FILES = {
    "name": "name.txt",
    "address": "address.txt",
    "employees": "employees.txt",
}


def create_app(data_dir: Path | None = None) -> Flask:
    app = Flask(__name__)
    root = Path(data_dir) if data_dir is not None else DATA_DIR

    def read_field(field: str) -> str:
        filename = FIELD_FILES[field]
        path = root / filename
        if not path.is_file():
            raise FileNotFoundError(f"Missing data file: {filename}")
        return path.read_text(encoding="utf-8").strip()

    def org_payload() -> dict:
        return {
            "name": read_field("name"),
            "address": read_field("address"),
            "employees": read_field("employees"),
        }

    @app.get("/")
    def index():
        accept = request.headers.get("Accept", "")
        if "application/json" in accept and "text/html" not in accept:
            return jsonify(org_payload())
        try:
            data = org_payload()
            error = None
        except FileNotFoundError as exc:
            data = {"name": "", "address": "", "employees": ""}
            error = str(exc)
        return render_template("index.html", org=data, error=error)

    @app.get("/api/org")
    def api_org():
        try:
            return jsonify(org_payload())
        except FileNotFoundError as exc:
            return jsonify({"error": str(exc)}), 404

    @app.get("/api/name")
    def api_name():
        try:
            return jsonify({"name": read_field("name")})
        except FileNotFoundError as exc:
            return jsonify({"error": str(exc)}), 404

    @app.get("/api/address")
    def api_address():
        try:
            return jsonify({"address": read_field("address")})
        except FileNotFoundError as exc:
            return jsonify({"error": str(exc)}), 404

    @app.get("/api/employees")
    def api_employees():
        try:
            return jsonify({"employees": read_field("employees")})
        except FileNotFoundError as exc:
            return jsonify({"error": str(exc)}), 404

    @app.get("/health")
    def health():
        missing = [f for f in FIELD_FILES.values() if not (root / f).is_file()]
        if missing:
            return jsonify({"status": "degraded", "missing": missing}), 503
        return jsonify({"status": "ok"})

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
