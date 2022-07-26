from unittest import mock

import pytest
from src.services import calculations
from src.models.model import RequestObject, ExpenseBreakdown


def test_zakat_owed_per_year_should_return_correct_amount():
    amount = 100.0
    expected_zakat_owed = 2.57

    service = calculations.CalculateFundLifetimeService()
    zakat_owed = service.zakat_owed_per_year(amount)

    assert zakat_owed == expected_zakat_owed


def test_calculate_wealth_after_stock_growth_should_return_correct_amount():
    amount = 100.50
    growth_percentage = 7
    expcted_amount_after_growth = 107.54

    service = calculations.CalculateFundLifetimeService()
    amount_after_growth = service.calculate_wealth_after_stock_growth(amount, growth_percentage)

    assert amount_after_growth == expcted_amount_after_growth


def test_take_expenses_out_should_return_correct_amount():
    amount = 231.44
    expenses = 144.98

    service = calculations.CalculateFundLifetimeService()
    amount_after_expenses = service.take_expenses_out(amount, expenses)

    assert amount_after_expenses == 86.46


@mock.patch.object(calculations.CalculateFundLifetimeService, "calculate_yearly_expense")
def test_handle_data_from_api_when_estimated_monthly_expenses_has_value_should_call_calculate_yearly_expense(mock):
    data_passed = RequestObject(zakat=True, cash_amount=200, invested_amount=650, estimated_rate_of_return=8,
                                estimated_monthly_expenses=3000)

    t = calculations.CalculateFundLifetimeService()
    t.handle_data_from_api(data_passed)
    mock.assert_called()


@mock.patch.object(calculations.CalculateFundLifetimeService, "calculate_yearly_expense_breakdown")
def test_handle_data_from_api_when_estimated_expenses_breakdown_has_value_should_call_calculate_yearly_expense_breakdown(mock, example_expense_breakdown):

    data_passed = RequestObject(zakat=True, cash_amount=200, invested_amount=650, estimated_rate_of_return=8,
                                estimated_expenses_breakdown=example_expense_breakdown)

    t = calculations.CalculateFundLifetimeService()
    t.handle_data_from_api(data_passed)
    mock.assert_called()


def test_handle_data_from_api_when_estimated_expenses_breakdown_and_estimated_monthly_expenses_has_value_should_raise_InvalidInput(example_expense_breakdown):

    data_passed = RequestObject(zakat=True, cash_amount=200, invested_amount=650, estimated_rate_of_return=8,
                                estimated_monthly_expenses=3000, estimated_expenses_breakdown=example_expense_breakdown)

    service = calculations.CalculateFundLifetimeService()

    with pytest.raises(calculations.InvalidInput):
        service.handle_data_from_api(data_passed)


def test_calculate_yearly_expense_should_return_correct_amount():
    monthly_expense = 3000
    expected_yearly_expense = 36000

    service = calculations.CalculateFundLifetimeService()
    yearly_expense = service.calculate_yearly_expense(monthly_expense)

    assert yearly_expense == expected_yearly_expense


def test_calculate_yearly_expense_breakdown_should_return_correct_amount(example_expense_breakdown):
    expected_yearly_expense = 23400

    service = calculations.CalculateFundLifetimeService()
    yearly_expense = service.calculate_yearly_expense_breakdown(example_expense_breakdown)

    assert yearly_expense == expected_yearly_expense





@pytest.fixture
def example_expense_breakdown():
    expense_breakdown = ExpenseBreakdown(property_tax=1000, county_tax=1000, car_insurance=1000, health_insurance=200,
                                         home_insurance=1000, house_maintenance=1000, home_owners_association=1000,
                                         phone_bill=200,
                                         electricity_gas_bill=200, car_gas=200, car_maintenance=1000, internet=1000,
                                         travel=1000,
                                         clothing=200, misc=200)
    return expense_breakdown
