from app.company_management import CompanyManagementSystem


def test_end_to_end_crud(tmp_path):
    db = tmp_path / "company.db"
    cms = CompanyManagementSystem(db)

    dep_id = cms.add_department("Engineering")
    emp_id = cms.add_employee("Alice", "alice@example.com", dep_id)
    proj_id = cms.add_project("Platform Revamp", 100000.0)
    cms.assign_employee_to_project(emp_id, proj_id)

    summary = cms.get_summary()
    assert summary == {
        "departments": 1,
        "employees": 1,
        "projects": 1,
        "assignments": 1,
    }

    cms.close()
