"""Simple Company Management System (CLI + SQLite).

Features:
- Departments CRUD (create + list)
- Employees CRUD (create + list)
- Projects CRUD (create + list)
- Employee assignment to projects
- Company summary report
"""

from __future__ import annotations

import argparse
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_DB_PATH = Path("company.db")


@dataclass(frozen=True)
class Department:
    id: int
    name: str


@dataclass(frozen=True)
class Employee:
    id: int
    name: str
    email: str
    department_id: int


@dataclass(frozen=True)
class Project:
    id: int
    name: str
    budget: float


class CompanyManagementSystem:
    def __init__(self, db_path: Path | str = DEFAULT_DB_PATH) -> None:
        self.db_path = str(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        self.conn.executescript(
            """
            PRAGMA foreign_keys = ON;

            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                department_id INTEGER NOT NULL,
                FOREIGN KEY(department_id) REFERENCES departments(id)
            );

            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                budget REAL NOT NULL CHECK(budget >= 0)
            );

            CREATE TABLE IF NOT EXISTS employee_projects (
                employee_id INTEGER NOT NULL,
                project_id INTEGER NOT NULL,
                PRIMARY KEY(employee_id, project_id),
                FOREIGN KEY(employee_id) REFERENCES employees(id) ON DELETE CASCADE,
                FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
            );
            """
        )
        self.conn.commit()

    def add_department(self, name: str) -> int:
        cursor = self.conn.execute(
            "INSERT INTO departments(name) VALUES (?)", (name.strip(),)
        )
        self.conn.commit()
        return int(cursor.lastrowid)

    def list_departments(self) -> list[Department]:
        rows = self.conn.execute("SELECT id, name FROM departments ORDER BY id").fetchall()
        return [Department(id=row["id"], name=row["name"]) for row in rows]

    def add_employee(self, name: str, email: str, department_id: int) -> int:
        cursor = self.conn.execute(
            "INSERT INTO employees(name, email, department_id) VALUES (?, ?, ?)",
            (name.strip(), email.strip().lower(), department_id),
        )
        self.conn.commit()
        return int(cursor.lastrowid)

    def list_employees(self) -> list[Employee]:
        rows = self.conn.execute(
            "SELECT id, name, email, department_id FROM employees ORDER BY id"
        ).fetchall()
        return [
            Employee(
                id=row["id"],
                name=row["name"],
                email=row["email"],
                department_id=row["department_id"],
            )
            for row in rows
        ]

    def add_project(self, name: str, budget: float) -> int:
        cursor = self.conn.execute(
            "INSERT INTO projects(name, budget) VALUES (?, ?)", (name.strip(), budget)
        )
        self.conn.commit()
        return int(cursor.lastrowid)

    def list_projects(self) -> list[Project]:
        rows = self.conn.execute("SELECT id, name, budget FROM projects ORDER BY id").fetchall()
        return [Project(id=row["id"], name=row["name"], budget=row["budget"]) for row in rows]

    def assign_employee_to_project(self, employee_id: int, project_id: int) -> None:
        self.conn.execute(
            "INSERT OR IGNORE INTO employee_projects(employee_id, project_id) VALUES (?, ?)",
            (employee_id, project_id),
        )
        self.conn.commit()

    def get_summary(self) -> dict[str, int]:
        return {
            "departments": self._count("departments"),
            "employees": self._count("employees"),
            "projects": self._count("projects"),
            "assignments": self._count("employee_projects"),
        }

    def _count(self, table_name: str) -> int:
        row = self.conn.execute(f"SELECT COUNT(*) AS total FROM {table_name}").fetchone()
        return int(row["total"])

    def close(self) -> None:
        self.conn.close()


def format_rows(rows: Iterable[object]) -> str:
    return "\n".join(str(row) for row in rows) if rows else "No records found."


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Company Management System")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="Path to SQLite database")

    subparsers = parser.add_subparsers(dest="command", required=True)

    dep_add = subparsers.add_parser("add-department", help="Add a department")
    dep_add.add_argument("name")

    subparsers.add_parser("list-departments", help="List departments")

    emp_add = subparsers.add_parser("add-employee", help="Add an employee")
    emp_add.add_argument("name")
    emp_add.add_argument("email")
    emp_add.add_argument("department_id", type=int)

    subparsers.add_parser("list-employees", help="List employees")

    proj_add = subparsers.add_parser("add-project", help="Add a project")
    proj_add.add_argument("name")
    proj_add.add_argument("budget", type=float)

    subparsers.add_parser("list-projects", help="List projects")

    assign = subparsers.add_parser(
        "assign-employee", help="Assign an employee to a project"
    )
    assign.add_argument("employee_id", type=int)
    assign.add_argument("project_id", type=int)

    subparsers.add_parser("summary", help="Show system summary")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    cms = CompanyManagementSystem(args.db)
    try:
        if args.command == "add-department":
            dep_id = cms.add_department(args.name)
            print(f"Department added with id={dep_id}")
        elif args.command == "list-departments":
            print(format_rows(cms.list_departments()))
        elif args.command == "add-employee":
            emp_id = cms.add_employee(args.name, args.email, args.department_id)
            print(f"Employee added with id={emp_id}")
        elif args.command == "list-employees":
            print(format_rows(cms.list_employees()))
        elif args.command == "add-project":
            proj_id = cms.add_project(args.name, args.budget)
            print(f"Project added with id={proj_id}")
        elif args.command == "list-projects":
            print(format_rows(cms.list_projects()))
        elif args.command == "assign-employee":
            cms.assign_employee_to_project(args.employee_id, args.project_id)
            print("Assignment completed")
        elif args.command == "summary":
            print(cms.get_summary())
    finally:
        cms.close()


if __name__ == "__main__":
    main()
