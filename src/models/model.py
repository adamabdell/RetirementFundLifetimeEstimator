from pydantic import BaseModel
from typing import Optional
from typing_extensions import TypedDict



class ExpenseBreakdown(TypedDict, total=False):
    property_tax: Optional[float] = 0
    county_tax: Optional[float] = 0
    car_insurance: Optional[float] = 0
    health_insurance: Optional[float] = 0
    home_insurance: Optional[float] = 0
    house_maintenance: Optional[float] = 0
    home_owners_association: Optional[float] = 0
    phone_bill: Optional[float] = 0
    electricity_gas_bill: Optional[float] = 0
    car_gas: Optional[float] = 0
    car_maintenance: Optional[float] = 0
    internet: Optional[float] = 0
    travel: Optional[float] = 0
    clothing: Optional[float] = 0
    misc: Optional[float] = 0


class RequestObject(BaseModel):
    zakat: bool
    cash_amount: Optional[float] = 0
    invested_amount: Optional[float] = 0
    estimated_rate_of_return: Optional[float] = 0
    income: Optional[float] = 0
    estimated_monthly_expenses: Optional[float] = 0
    estimated_expenses_breakdown: Optional[ExpenseBreakdown] = 0


class ResponseObject(BaseModel):
    years_until_money_runs_out: int






