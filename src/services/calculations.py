

class CalculateFundLifetime:

    def zakat_owed_per_year(unused_wealth_amount: float):

        zakat_owed = unused_wealth_amount * 0.0257
        return round(zakat_owed, 2)

    def calculate_wealth_after_stock_growth(invested_amount: float, stock_growth_percentage: float):

        growth_percentage = 1 + (stock_growth_percentage / 100)
        amount_after_growth = invested_amount * growth_percentage
        return round(amount_after_growth, 2)






