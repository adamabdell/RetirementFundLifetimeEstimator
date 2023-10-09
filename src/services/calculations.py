from src.models.model import RequestObject

class CalculateFundLifetimeService:


    def handle_data_from_api(self, data: RequestObject):

        data = data.dict()

        monthly_expense = data['estimated_monthly_expenses']
        expense_breakdown = data['estimated_expenses_breakdown']

        cash_amount = data['cash_amount']
        invested_amount = data['invested_amount']

        if (cash_amount is None and invested_amount is None) or (cash_amount == 0 and invested_amount == 0) or (cash_amount is not None and invested_amount is not None):
            raise InvalidWealthInput
        if monthly_expense is not None and expense_breakdown is not None:
            raise InvalidExpenseInput

        if monthly_expense is not None:
            data['estimated_yearly_expenses'] = self.calculate_yearly_expense(monthly_expense)
        if expense_breakdown is not None:
            data['estimated_yearly_expenses'] = self.calculate_yearly_expense_breakdown(expense_breakdown)

        del data['estimated_expenses_breakdown']
        del data['estimated_monthly_expenses']

        if invested_amount is not None:
            years_lasted = self.find_number_of_years_invested_amount_will_last(data)
        else:
            years_lasted = self.find_number_of_years_cash_amount_will_last(data)

        return years_lasted


    def calculate_yearly_expense(self, monthly_expense: float):
        yearly_expense = monthly_expense * 12
        return round(yearly_expense, 2)


    def calculate_yearly_expense_breakdown(self, expense_breakdown: dict):
        monthly_list = ['food', 'health_insurance', 'phone_bill', 'electricity_gas_bill', 'car_gas', 'clothing', 'misc']
        list_of_yearly_expenses = []

        for expenses in expense_breakdown:
            if expenses in monthly_list:
                list_of_yearly_expenses.append(expense_breakdown[expenses] * 12)
            else:
                list_of_yearly_expenses.append(expense_breakdown[expenses])

        yearly_expense = sum(list_of_yearly_expenses)
        return round(yearly_expense, 2)


    def find_number_of_years_invested_amount_will_last(self, data: dict):

        beginning_year_wealth = data['invested_amount']
        yearly_expenses = data['estimated_yearly_expenses']
        stock_growth_percentage = data['estimated_rate_of_return']
        year_number = 0

        while beginning_year_wealth > 0:

            expense = self.expense_amount_change_based_on_inflation(yearly_expenses, year_number)
            wealth_amount_after_expenses = round(beginning_year_wealth - expense, 2)

            end_year_amount = round(self.calculate_wealth_after_stock_growth(wealth_amount_after_expenses, stock_growth_percentage), 2)

            if (data['zakat'] is True) and (end_year_amount >= 4900.00):
                zakat_owed = self.zakat_owed_per_year(beginning_year_wealth, end_year_amount)
                end_year_amount = end_year_amount - zakat_owed

            beginning_year_wealth = end_year_amount
            print(beginning_year_wealth)
            year_number += 1

        return year_number - 1


    def find_number_of_years_cash_amount_will_last(self, data: dict):

        beginning_year_wealth = data['cash_amount']
        yearly_expenses = data['estimated_yearly_expenses']
        year_number = 0

        while beginning_year_wealth > 0:

            expense = self.expense_amount_change_based_on_inflation(yearly_expenses, year_number)
            end_year_amount_after_expenses = round(beginning_year_wealth - expense, 2)

            if data['zakat'] is True:
                zakat_owed = self.zakat_owed_per_year(beginning_year_wealth, end_year_amount_after_expenses)
                end_year_amount_after_expenses = end_year_amount_after_expenses - zakat_owed

            beginning_year_wealth = end_year_amount_after_expenses

            year_number += 1

        return year_number - 1


    def expense_amount_change_based_on_inflation(self, expenses: float, year_number: int):

        average_yearly_inflation = 1.03

        expenses_after_inflation = expenses * (average_yearly_inflation ** year_number)
        return round(expenses_after_inflation, 2)


    def zakat_owed_per_year(self, beginning_year_wealth: float, end_year_amount: float):

        zakat_percentage = 0.0257

        if beginning_year_wealth <= end_year_amount:
            unused_wealth_amount = beginning_year_wealth
        else:
            unused_wealth_amount = end_year_amount

        zakat_owed = unused_wealth_amount * zakat_percentage
        return round(zakat_owed, 2)


    def calculate_wealth_after_stock_growth(self, invested_amount: float, stock_growth_percentage: float):

        growth_percentage = 1 + (stock_growth_percentage / 100)
        amount_after_growth = invested_amount * growth_percentage
        return round(amount_after_growth, 2)


    def take_expenses_out(self, principal_amount: float, expenses: float):

        money_amount_after_expenses = principal_amount - expenses
        return round(money_amount_after_expenses, 2)


class InvalidExpenseInput(Exception):
    pass

class InvalidWealthInput(Exception):
    pass




