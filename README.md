# Org Details

Organization metadata (`name.txt`, `address.txt`, `employees.txt`) plus a small HTTP web service that exposes it as JSON and a simple HTML page.

## Web service

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run

```bash
python -m web_service.app
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000).

Optional environment variables:

| Variable       | Default                         | Purpose                          |
|----------------|---------------------------------|----------------------------------|
| `PORT`         | `5000`                          | Listen port                      |
| `ORG_DATA_DIR` | repository root                 | Directory with the `.txt` files  |
| `FLASK_DEBUG`  | unset                           | Set to `1` for Flask debug mode  |

Production-style run:

```bash
gunicorn --bind 0.0.0.0:5000 web_service.app:app
```

### API

| Method | Path             | Response                                      |
|--------|------------------|-----------------------------------------------|
| GET    | `/`              | HTML page (or JSON if `Accept: application/json`) |
| GET    | `/api/org`       | `{ "name", "address", "employees" }`          |
| GET    | `/api/name`      | `{ "name" }`                                  |
| GET    | `/api/address`   | `{ "address" }`                               |
| GET    | `/api/employees` | `{ "employees" }`                             |
| GET    | `/health`        | `{ "status": "ok" }`                          |

### Tests

```bash
pytest
```
