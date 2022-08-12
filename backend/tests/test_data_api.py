from fastapi.testclient import TestClient

from backend.src.api.data_api import app
from backend.src.models.model import RequestObject

client = TestClient(app)

def test_get_fund_lifetime_should_respond_HTTPResponse_200():
    data_passed = RequestObject(zakat=True, invested_amount=100_000, estimated_rate_of_return=8,
                                estimated_monthly_expenses=3000)

    response = client.get("/user_input", json={"zakat": data_passed.zakat, "invested_amount": data_passed.invested_amount,
                                               "estimated_rate_of_return": data_passed.estimated_rate_of_return,
                                               "estimated_monthly_expenses": data_passed.estimated_monthly_expenses})
    assert response.status_code == 200
    assert response.json() == 'Your fund will last 2 - 3 years'


def test_get_fund_lifetime_when_cash_amount_and_invested_amount_is_None_should_respond_HTTPResponse_400():
    data_passed = RequestObject(zakat=True, invested_amount=None, estimated_rate_of_return=8,
                                estimated_monthly_expenses=3000)

    response = client.get("/user_input", json={"zakat": data_passed.zakat, "invested_amount": data_passed.invested_amount,
                                               "estimated_rate_of_return": data_passed.estimated_rate_of_return,
                                               "estimated_monthly_expenses": data_passed.estimated_monthly_expenses})
    assert response.status_code == 400


def test_get_fund_lifetime_when_cash_amount_and_invested_amount_is_not_None_should_respond_HTTPResponse_400():
    data_passed = RequestObject(zakat=True, cash_amount=10, invested_amount=10, estimated_rate_of_return=8,
                                estimated_monthly_expenses=3000)

    response = client.get("/user_input", json={"zakat": data_passed.zakat, "invested_amount": data_passed.invested_amount,
                                               "cash_amount": data_passed.cash_amount, "estimated_rate_of_return": data_passed.estimated_rate_of_return,
                                               "estimated_monthly_expenses": data_passed.estimated_monthly_expenses})
    assert response.status_code == 400


def test_get_fund_lifetime_when_cash_amount_and_invested_amount_is_zero_should_respond_HTTPResponse_400():
    data_passed = RequestObject(zakat=True, cash_amount=0, invested_amount=0, estimated_rate_of_return=8,
                                estimated_monthly_expenses=3000)

    response = client.get("/user_input", json={"zakat": data_passed.zakat, "invested_amount": data_passed.invested_amount,
                                               "cash_amount": data_passed.cash_amount, "estimated_rate_of_return": data_passed.estimated_rate_of_return,
                                               "estimated_monthly_expenses": data_passed.estimated_monthly_expenses})
    assert response.status_code == 400


def test_get_fund_lifetime_when_estimated_monthly_expenses_and_estimated_expenses_breakdown_is_not_None_should_respond_HTTPResponse_400():
    data_passed = RequestObject(zakat=True, invested_amount=650, estimated_rate_of_return=8,
                                estimated_monthly_expenses=3000, estimated_expenses_breakdown={"field": 20})

    response = client.get("/user_input", json={"zakat": data_passed.zakat, "invested_amount": data_passed.invested_amount,
                                               "cash_amount": data_passed.cash_amount, "estimated_rate_of_return": data_passed.estimated_rate_of_return,
                                               "estimated_monthly_expenses": data_passed.estimated_monthly_expenses,
                                               "estimated_expenses_breakdown": data_passed.estimated_expenses_breakdown})
    assert response.status_code == 400



