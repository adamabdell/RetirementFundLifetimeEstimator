import pytest
from src.services import calculations

def test_zakat_owed_per_year_should_return_correct_amount():

    amount = 100.0

    service = calculations.CalculateFundLifetimeService
    zakat_owed = service.zakat_owed_per_year(amount)

    assert zakat_owed == 2.57


def test_calculate_wealth_after_stock_growth_should_return_correct_amount():

    amount = 100.50
    growth_percentage = 7

    service = calculations.CalculateFundLifetimeService
    amount_after_growth = service.calculate_wealth_after_stock_growth(amount, growth_percentage)

    assert amount_after_growth == 107.54

