# BookStore Backend

A monorepo for a bookstore backend using microservices architecture with Chalice, Python, AWS Lambda, and DynamoDB.

## Structure
- `common/`: Shared utilities (e.g., DB helpers, HTTP utils).
- `scripts/`: Infrastructure scripts (e.g., `create_table.py` for DynamoDB).
- `services/inventory_service/`: Inventory service for managing books.

## Setup
1. Install dependencies: `pip install -r services/inventory_service/requirements.txt`
2. Create DynamoDB table: `python scripts/create_table.py`
3. Run locally: `cd services/inventory_service && chalice local --port=8000`

## Deploy
- Deploy `inventory_service`: `cd services/inventory_service && chalice deploy`
