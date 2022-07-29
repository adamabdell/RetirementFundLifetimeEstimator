from fastapi import FastAPI
from src.models.model import RequestObject
from src.services.calculations import CalculateFundLifetimeService

app = FastAPI()


@app.get("/")
def dummy():
    return "Hello Adam"



@app.get("/user_input", status_code=200)
def get_fund_lifetime(request: RequestObject):

    print(request)
    service = CalculateFundLifetimeService()
    lifetime_fund = service.handle_data_from_api(request)
    # return f"Your fund will last {lifetime_fund} - {lifetime_fund + 1}"
    return lifetime_fund



