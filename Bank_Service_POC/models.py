from pydantic import BaseModel
from typing import Optional

# ------------------ Account ------------------

class CreateAccountRequest(BaseModel):
    account_number: str
    name: str
    pin: str

class AccountRequest(BaseModel):
    account_number: str
    pin: str

class ChangePinRequest(BaseModel):

    account_number: str
    old_pin: str
    new_pin: str

class KYCUpdateRequest(BaseModel):
    account_number: str
    pin: str
    aadhaar: str
    pan: str
    address: str

# ------------------ Transactions ------------------

class DepositRequest(BaseModel):
    account_number: str
    pin: str
    amount: float

class WithdrawRequest(BaseModel):
    account_number: str
    pin: str
    amount: float

class TransferRequest(BaseModel):
    from_account: str
    to_account: str
    pin: str
    amount: float

from pydantic import BaseModel, Field

#------------Loan Application Request-------------------

class LoanRequest(BaseModel):
    account_number: str = Field(..., example="12345")
    pin: str = Field(..., example="1111")
    loan_amount: float = Field(..., gt=0, example=5000)
    interest_rate: float = Field(..., gt=0, example=10)  # percentage
    tenure_months: int = Field(..., gt=0, example=12)


# Loan Repayment Request
class LoanRepayRequest(BaseModel):
    account_number: str = Field(..., example="12345")
    loan_id: str = Field(..., example="265hsyqtwu826")
    pin: str = Field(..., example="1111")
    amount: float = Field(..., gt=0, example=1000)



