## Description
A basic employee payroll manager using FastAPI and PostgreSQL.

## Setup

Steps to run program:
1. Install python3 (Recommended for project: `python3.9`)
2. Install python-poetry
```
curl -sSL https://install.python-poetry.org | python3
```
3. Install postgresql
```
brew install postgresql
```

4. Setup postgresql server
```env
DB_URL="postgresql://username:password@localhost:5432"
```

5. Setup poetry venv and packages
```
poetry env use python3.9
poetry install
```

6. Initialize table/s
```SQL
CREATE TABLE employees (
	id SERIAL PRIMARY KEY,
	name VARCHAR ( 50 ) NOT NULL,
	birthdate DATE NOT NULL,
	tin VARCHAR ( 50 ) NOT NULL,
	employee_type VARCHAR ( 20 ) NOT NULL,
	basic_rate FLOAT,
	created_at TIMESTAMP NOT NULL,
	updated_at TIMESTAMP NOT NULL,
	is_deleted BOOL
);
```

## How to Use:
Run the program:
```bash
poetry run uvicorn main:app --port 8000 --reload
```

API documentation can be seen in FastAPI's built-in swagger documentation at:
```
localhost:8000/docs
```
