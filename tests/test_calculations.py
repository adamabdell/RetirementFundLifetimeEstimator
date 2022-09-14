from unittest import mock

import pytest
from src.services import calculations
from src.models.model import RequestObject, ExpenseBreakdown


def test_zakat_owed_per_year_when_finishing_year_with_more_money_than_the_start_should_return_correct_amount():
    beginning_year_amount = 100.0
    end_year_amount = 150.0
    expected_zakat_owed = 2.57

    service = calculations.CalculateFundLifetimeService()
    zakat_owed = service.zakat_owed_per_year(beginning_year_amount, end_year_amount)

    assert zakat_owed == expected_zakat_owed


def test_zakat_owed_per_year_when_finishing_year_with_less_money_than_the_start_should_return_correct_amount():
    beginning_year_amount = 100.0
    end_year_amount = 80.0
    expected_zakat_owed = 2.06

    service = calculations.CalculateFundLifetimeService()
    zakat_owed = service.zakat_owed_per_year(beginning_year_amount, end_year_amount)

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
    data_passed = RequestObject(zakat=True, invested_amount=650, estimated_rate_of_return=8,
                                estimated_monthly_expenses=3000)

    service = calculations.CalculateFundLifetimeService()
    service.handle_data_from_api(data_passed)
    mock.assert_called()


@mock.patch.object(calculations.CalculateFundLifetimeService, "calculate_yearly_expense_breakdown")
def test_handle_data_from_api_when_estimated_expenses_breakdown_has_value_should_call_calculate_yearly_expense_breakdown(mock, example_expense_breakdown):

    data_passed = RequestObject(zakat=True, invested_amount=650, estimated_rate_of_return=8,
                                estimated_expenses_breakdown=example_expense_breakdown)

    service = calculations.CalculateFundLifetimeService()
    service.handle_data_from_api(data_passed)
    mock.assert_called()


def test_handle_data_from_api_when_estimated_expenses_breakdown_and_estimated_monthly_expenses_has_value_should_raise_InvalidExpenseInput(example_expense_breakdown):

    data_passed = RequestObject(zakat=True, invested_amount=650, estimated_rate_of_return=8,
                                estimated_monthly_expenses=3000, estimated_expenses_breakdown=example_expense_breakdown)

    service = calculations.CalculateFundLifetimeService()

    with pytest.raises(calculations.InvalidExpenseInput):
        service.handle_data_from_api(data_passed)


def test_handle_data_from_api_when_cash_amount_and_invested_amount_are_none_should_raise_InvalidWealthInput():

    cash_and_invest_amount_none = RequestObject(zakat=True, estimated_rate_of_return=8, estimated_monthly_expenses=3000)

    service = calculations.CalculateFundLifetimeService()

    with pytest.raises(calculations.InvalidWealthInput):
        service.handle_data_from_api(cash_and_invest_amount_none)


def test_handle_data_from_api_when_cash_amount_and_invested_amount_are_zero_should_raise_InvalidWealthInput():

    cash_and_invest_amount_zero = RequestObject(zakat=True, cash_amount=0, invested_amount=0,
                                                estimated_rate_of_return=8, estimated_monthly_expenses=3000)

    service = calculations.CalculateFundLifetimeService()

    with pytest.raises(calculations.InvalidWealthInput):
        service.handle_data_from_api(cash_and_invest_amount_zero)


def test_handle_data_from_api_when_cash_amount_and_invested_amount_both_have_values_should_raise_InvalidInput():

    cash_and_invest_amount_zero = RequestObject(zakat=True, cash_amount=10, invested_amount=10,
                                                estimated_rate_of_return=8, estimated_monthly_expenses=3000)

    service = calculations.CalculateFundLifetimeService()

    with pytest.raises(calculations.InvalidWealthInput):
        service.handle_data_from_api(cash_and_invest_amount_zero)


def test_calculate_yearly_expense_should_return_correct_amount():
    monthly_expense = 3000
    expected_yearly_expense = 36000

    service = calculations.CalculateFundLifetimeService()
    yearly_expense = service.calculate_yearly_expense(monthly_expense)

    assert yearly_expense == expected_yearly_expense


def test_calculate_yearly_expense_breakdown_should_return_correct_amount(example_expense_breakdown):
    expected_yearly_expense = 25800

    service = calculations.CalculateFundLifetimeService()
    yearly_expense = service.calculate_yearly_expense_breakdown(example_expense_breakdown)

    assert yearly_expense == expected_yearly_expense


def test_expense_amount_change_based_on_inflation_year_zero_to_one_should_return_correct_amount():
    expense_amount = 3000
    year_number = 0
    expected_expense_amount = 3000

    service = calculations.CalculateFundLifetimeService()
    after_inflation_expense = service.expense_amount_change_based_on_inflation(expense_amount, year_number)

    assert after_inflation_expense == expected_expense_amount


def test_expense_amount_change_based_on_inflation_year_five_to_six_should_return_correct_amount():
    expense_amount = 3000
    year_number = 5
    expected_expense_amount = 3477.82

    service = calculations.CalculateFundLifetimeService()
    after_inflation_expense = service.expense_amount_change_based_on_inflation(expense_amount, year_number)

    assert after_inflation_expense == expected_expense_amount


def test_find_number_of_years_invested_amount_will_last_with_zakat_should_return_correct_year():
    data_passed = dict(zakat=True, invested_amount=100_000, estimated_rate_of_return=8,
                                estimated_yearly_expenses=36000)
    expected_fund_lifetime = 2

    service = calculations.CalculateFundLifetimeService()
    fund_lifetime = service.find_number_of_years_invested_amount_will_last(data_passed)

    assert fund_lifetime == expected_fund_lifetime


def test_find_number_of_years_invested_amount_will_last_without_zakat_should_return_correct_year():
    data_passed = dict(zakat=False, invested_amount=100_000, estimated_rate_of_return=8,
                       estimated_yearly_expenses=36000)
    expected_fund_lifetime = 2

    service = calculations.CalculateFundLifetimeService()
    fund_lifetime = service.find_number_of_years_invested_amount_will_last(data_passed)

    assert fund_lifetime == expected_fund_lifetime


def test_find_number_of_years_cash_amount_will_last_with_zakat_should_return_correct_year():
    data_passed = dict(zakat=True, cash_amount=100_000, estimated_yearly_expenses=36000)
    expected_fund_lifetime = 2

    service = calculations.CalculateFundLifetimeService()
    fund_lifetime = service.find_number_of_years_cash_amount_will_last(data_passed)

    assert fund_lifetime == expected_fund_lifetime


def test_find_number_of_years_cash_amount_will_last_without_zakat_should_return_correct_year():
    data_passed = dict(zakat=False, cash_amount=100_000, estimated_yearly_expenses=36000)
    expected_fund_lifetime = 2

    service = calculations.CalculateFundLifetimeService()
    fund_lifetime = service.find_number_of_years_cash_amount_will_last(data_passed)

    assert fund_lifetime == expected_fund_lifetime


def test_find_how_many_years_until_social_security_is_relevent():
    age = 57
    expected_time_until_income_kicks_in = 5

    service = calculations.CalculateFundLifetimeService()
    time_until_income_is_relevent = service.find_how_many_years_until_social_security_is_relevent(age)

    assert expected_time_until_income_kicks_in == time_until_income_is_relevent


def test_income_amount_change_based_on_inflation():
    income = 1000
    year_number = 3
    expected_income_amount = 1092.73

    service = calculations.CalculateFundLifetimeService()
    income_after_inflation = service.income_amount_change_based_on_inflation(income, year_number)

    assert income_after_inflation == expected_income_amount
#IGNORE########################################################################################################################
def test_dummy_invested():
    data_passed = RequestObject(age=63, zakat=True, invested_amount=10_000, estimated_rate_of_return=5,
                                social_security_income=1000, estimated_monthly_expenses=200)

    service = calculations.CalculateFundLifetimeService()
    service.handle_data_from_api(data_passed)


def test_dummy_cash():
    data_passed = RequestObject(zakat=True, cash_amount=100_000, estimated_monthly_expenses=3000)

    service = calculations.CalculateFundLifetimeService()
    service.handle_data_from_api(data_passed)
#IGNORE########################################################################################################################



@pytest.fixture
def example_expense_breakdown():
    expense_breakdown = ExpenseBreakdown(property_tax=1000, county_tax=1000, food=200, car_insurance=1000, health_insurance=200,
                                         home_insurance=1000, house_maintenance=1000, home_owners_association=1000,
                                         phone_bill=200,
                                         electricity_gas_bill=200, car_gas=200, car_maintenance=1000, internet=1000,
                                         travel=1000,
                                         clothing=200, misc=200)
    return expense_breakdown
