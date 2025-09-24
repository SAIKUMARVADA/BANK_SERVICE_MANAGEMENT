from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ------------------ Account ------------------

class CreateAccountRequest(BaseModel):
    account_number: str
    name: str
    pin: str
    balance: float = 0.0   # default balance is 0.0
    created_at: datetime = datetime.utcnow()  # auto timestamp
    status: str = "active"  # default status
    kyc: Optional[str] = None  # optional field

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

class close_account_service(BaseModel):
    account_number: str
    pin: str

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



#------------Loan Application Request-------------------

class LoanRequest(BaseModel):
    account_number: str 
    pin: str 
    loan_amount: float 
    interest_rate: float # percentage
    tenure_months: int 


# Loan Repayment Request
class LoanRepayRequest(BaseModel):
    account_number: str 
    loan_id: str 
    pin: str 
    amount: float



