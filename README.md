# 100DaysOfDevops

A starter **Company Management System** built with Python and SQLite.

## Features
- Department management
- Employee management
- Project management
- Employee-to-project assignment
- Summary report (counts of entities)

## Run
```bash
python -m app.company_management --help
```

### Example
```bash
python -m app.company_management add-department Engineering
python -m app.company_management add-employee "Alice" alice@example.com 1
python -m app.company_management add-project "Platform Revamp" 100000
python -m app.company_management assign-employee 1 1
python -m app.company_management summary
```

## Test
```bash
python -m pytest -q
```
