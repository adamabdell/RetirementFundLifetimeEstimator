from src.models.model import RequestObject

class CalculateFundLifetimeService:


    def handle_data_from_api(self, data: RequestObject):

        data = data.dict()
        monthly_expense = data['estimated_monthly_expenses']
        expense_breakdown = data['estimated_expenses_breakdown']

        if monthly_expense is not None and expense_breakdown is not None:
            raise InvalidInput
        if monthly_expense is not None:
            data['estimated_monthly_expenses'] = self.calculate_yearly_expense(monthly_expense)
        if expense_breakdown is not None:
            data['estimated_expenses_breakdown'] = self.calculate_yearly_expense_breakdown(expense_breakdown)


    def calculate_yearly_expense(self, monthly_expense: float):
        yearly_expense = monthly_expense * 12
        return round(yearly_expense, 2)


    def calculate_yearly_expense_breakdown(self, expense_breakdown: dict):
        monthly_list = ['health_insurance', 'phone_bill', 'electricity_gas_bill', 'car_gas', 'clothing', 'misc']
        list_of_yearly_expenses = []

        for expenses in expense_breakdown:
            if expenses in monthly_list:
                list_of_yearly_expenses.append(expense_breakdown[expenses] * 12)
            else:
                list_of_yearly_expenses.append(expense_breakdown[expenses])

        yearly_expense = sum(list_of_yearly_expenses)
        return round(yearly_expense, 2)


    def zakat_owed_per_year(self, unused_wealth_amount: float):

        zakat_percentage = 0.0257
        zakat_owed = unused_wealth_amount * zakat_percentage
        return round(zakat_owed, 2)


    def calculate_wealth_after_stock_growth(self, invested_amount: float, stock_growth_percentage: float):

        growth_percentage = 1 + (stock_growth_percentage / 100)
        amount_after_growth = invested_amount * growth_percentage
        return round(amount_after_growth, 2)


    def take_expenses_out(self, principal_amount: float, expenses: float):

        money_amount_after_expenses = principal_amount - expenses
        return round(money_amount_after_expenses, 2)


class InvalidInput(Exception):
    pass





