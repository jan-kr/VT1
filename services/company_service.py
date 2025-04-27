from models import Company


def create_company(session, name: str, description: str, industry: str, employee_count: int):
    company = Company(
        name=name,
        description=description,
        industry=industry,
        employee_count=employee_count,
    )

    session.add(company)
    session.commit()
    company_id = company.id
    return company_id


def delete_company(session, company_id: int):
    company = session.get(Company, company_id)
    if not company:
        return False

    session.delete(company)
    session.commit()
    return True
