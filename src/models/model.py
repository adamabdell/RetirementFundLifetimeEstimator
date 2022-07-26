from pydantic import BaseModel
from typing import Optional
from typing_extensions import TypedDict



class ExpenseBreakdown(TypedDict, total=False):
    property_tax: Optional[float] = None
    county_tax: Optional[float] = None
    car_insurance: Optional[float] = None
    health_insurance: Optional[float] = None
    home_insurance: Optional[float] = None
    house_maintenance: Optional[float] = None
    home_owners_association: Optional[float] = None
    phone_bill: Optional[float] = None
    electricity_gas_bill: Optional[float] = None
    car_gas: Optional[float] = None
    car_maintenance: Optional[float] = None
    internet: Optional[float] = None
    travel: Optional[float] = None
    clothing: Optional[float] = None
    misc: Optional[float] = None


class RequestObject(BaseModel):
    age: Optional[int] = None
    zakat: bool
    cash_amount: Optional[float] = None
    invested_amount: Optional[float] = None
    additional_yearly_contribution: Optional[float] = None
    estimated_rate_of_return: Optional[float] = None
    income: Optional[float] = None
    estimated_monthly_expenses: Optional[float] = None
    estimated_expenses_breakdown: Optional[ExpenseBreakdown] = None


class ResponseObject(BaseModel):
    estimated_retirement_fund_lifetime_in_years: int






