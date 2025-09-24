import os
import json
from fastapi import APIRouter, HTTPException
from models import (
    CreateAccountRequest,
    AccountRequest,
    ChangePinRequest,
    KYCUpdateRequest,
    DepositRequest,
    WithdrawRequest,
    TransferRequest,
    LoanRequest,
    LoanRepayRequest,
)
import utility   # import the utility module, not individual functions

DATA_FILE = os.path.join("storage", "data.json")

def read_data():
    """Read JSON data from storage"""
    if not os.path.exists(DATA_FILE):
        return {"accounts": [], "transactions": [], "loans": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def write_data(data):
    """Write JSON data to storage"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

router = APIRouter()

# ----------------- Accounts -----------------
@router.post("/account/create")
def create_account(req: CreateAccountRequest):
    return utility.create_account_service(req)

@router.get("/account/balance")
def check_balance(req: AccountRequest):
    return utility.check_balance_service(req)

@router.put("/account/change_pin")
def change_pin(req: ChangePinRequest):
    return utility.change_pin_service(req)

@router.put("/account/kyc_update")
def kyc_update(req: KYCUpdateRequest):
    return utility.kyc_update_service(req)

@router.delete("/account/close_account")
def close_account(req: AccountRequest):
    return utility.close_account_service(req)

# ----------------- Transactions -----------------
@router.post("/transaction/deposit")
def deposit(req: DepositRequest):
    return utility.deposit_service(req)

@router.post("/transaction/withdraw")
def withdraw(req: WithdrawRequest):
    return utility.withdraw_service(req)

@router.get("/transaction/transfer")
def transfer(req: TransferRequest):
    return utility.transfer_service(req)

# ----------------- Loans -----------------
@router.post("/loan/apply")
def apply_loan(req: LoanRequest):
    return utility.apply_loan_service(req)

@router.put("/loan/repay")
def repay_loan(req: LoanRepayRequest):
    return utility.repay_loan_service(req)
