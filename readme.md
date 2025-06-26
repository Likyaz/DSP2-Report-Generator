# DSP2 Report Generator

## Installation

### Requirements
- Python 3.11 or higher
- `pip` or `uv`

### Setup

```bash
uv venv
uv pip install -r requirements.txt
```

### API

#### .env Configuration
Copy the .env.example file, rename it to .env, and fill in the required variables.

To start the API server, run `uvicorn app.main:app --reload`

#### Available Routes
- GET `/account`
Returns a JSON with all the user's accounts.

- GET `/account/{account_id}/report/json?date_start=2024-01-01&date_end=2025-01-01`
Returns a JSON report for a specific account, for a given date range.

- GET /account/{account_id}/report/csv
Same as above, but returns the report as a CSV file.

- GET /account/consistency
Returns consistency information between account balances and the sum of all related transactions.


### Partie Interface de cmd
Just run the script `python3 run_console.py` and let it guide you step by step.

