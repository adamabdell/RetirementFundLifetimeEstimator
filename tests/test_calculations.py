import pytest
from src.services import calculations

def test_zakat_owed_per_year_should_return_two_point_fifty_seven_percent_of_amount():

    amount = 100.0

    service = calculations.CalculateFundLifetime
    zakat_owed = service.zakat_owed_per_year(amount)

    assert zakat_owed == 2.57


def test_calculate_wealth_after_stock_growth():

    amount = 100.50
    growth_percentage = 7

    service = calculations.CalculateFundLifetime
    amount_after_growth = service.calculate_wealth_after_stock_growth(amount, growth_percentage)

    assert amount_after_growth == 107.54

