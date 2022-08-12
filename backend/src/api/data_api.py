from fastapi import FastAPI, HTTPException
from backend.src.models.model import RequestObject
from backend.src.services.calculations import CalculateFundLifetimeService, InvalidWealthInput, InvalidExpenseInput

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


@app.get("/")
def dummy():
    return "Hello Adam"



@app.get("/user_input", status_code=200)
def get_fund_lifetime(request: RequestObject):

    service = CalculateFundLifetimeService()
    try:
        lifetime_fund = service.handle_data_from_api(request)
        return f"Your fund will last {lifetime_fund} - {lifetime_fund + 1} years"
    except InvalidWealthInput:
        raise HTTPException(status_code=400, detail="Cash amount or invested amount must have a value but not both")
    except InvalidExpenseInput:
        raise HTTPException(status_code=400, detail="Only monthly expense or break down can be filled out but not both")



