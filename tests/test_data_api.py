import pytest
from fastapi.testclient import TestClient

from src.api.data_api import app
from src.models.model import RequestObject

client = TestClient(app)

def test_get_fund_lifetime_should_respond_HTTPResponse_200():
    data_passed = RequestObject(zakat=True, invested_amount=100_000, estimated_rate_of_return=8,
                                estimated_monthly_expenses=3000)

    response = client.get("/user_input", json={"zakat": data_passed.zakat, "invested_amount": data_passed.invested_amount,
                                               "estimated_rate_of_return": data_passed.estimated_rate_of_return,
                                               "estimated_monthly_expenses": data_passed.estimated_monthly_expenses})

    print(response.json(), '8888888888888888888888888888888888888888888888888')
    assert int(response.json()) == 2


