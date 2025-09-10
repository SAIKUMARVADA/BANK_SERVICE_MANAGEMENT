from datetime import datetime
from fastapi import HTTPException
from pymongo import MongoClient
from models import (
    LoanRepayRequest, CreateAccountRequest, DepositRequest, WithdrawRequest,
    TransferRequest, AccountRequest, ChangePinRequest, KYCUpdateRequest, LoanRequest
)

# ----------------- MongoDB Connection -----------------
client = MongoClient(
    "mongodb+srv://saikumarvada23:Saikumar143@resumestore.arpzpqu.mongodb.net/?retryWrites=true&w=majority&appName=Resumestore"
)
db = client["bank_service_poc"]

accounts_collection = db["accounts"]
loans_collection = db["loans"]
transactions_collection = db["transactions"]

# ----------------- Helper function -----------------
def log_transaction(data: dict):
    """Insert a transaction record with UTC timestamp"""
    data["timestamp"] = datetime.utcnow()
    transactions_collection.insert_one(data)

# ----------------- Accounts -----------------
def create_account_service(request: CreateAccountRequest):
    existing = accounts_collection.find_one({"account_number": request.account_number})
    if existing:
        raise HTTPException(status_code=400, detail="Account already exists")
    
    account = {
        "account_number": request.account_number,
        "name": request.name,
        "pin": request.pin,
        "balance": 0.0,
        "created_at": datetime.utcnow(),
        "status": "active",
        "kyc": {}
    }
    accounts_collection.insert_one(account)
    return {"message": "Account created successfully"}


def deposit_service(request: DepositRequest):
    acc = accounts_collection.find_one({"account_number": request.account_number, "pin": request.pin})
    if not acc:
        raise HTTPException(status_code=404, detail="Invalid account or PIN")
    
    new_balance = acc["balance"] + request.amount
    accounts_collection.update_one({"_id": acc["_id"]}, {"$set": {"balance": new_balance}})
    
    log_transaction({
        "account_number": request.account_number,
        "type": "deposit",
        "amount": request.amount
    })
    return {"message": "Deposit successful", "balance": new_balance}


def withdraw_service(request: WithdrawRequest):
    acc = accounts_collection.find_one({"account_number": request.account_number, "pin": request.pin})
    if not acc:
        raise HTTPException(status_code=404, detail="Invalid account or PIN")
    if acc["balance"] < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    new_balance = acc["balance"] - request.amount
    accounts_collection.update_one({"_id": acc["_id"]}, {"$set": {"balance": new_balance}})
    
    log_transaction({
        "account_number": request.account_number,
        "type": "withdraw",
        "amount": request.amount
    })
    return {"message": "Withdrawal successful", "balance": new_balance}


def transfer_service(request: TransferRequest):
    from_acc = accounts_collection.find_one({"account_number": request.from_account, "pin": request.pin})
    to_acc = accounts_collection.find_one({"account_number": request.to_account})
    
    if not from_acc or not to_acc:
        raise HTTPException(status_code=404, detail="Invalid accounts")
    if from_acc["balance"] < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    accounts_collection.update_one({"_id": from_acc["_id"]}, {"$inc": {"balance": -request.amount}})
    accounts_collection.update_one({"_id": to_acc["_id"]}, {"$inc": {"balance": request.amount}})

    log_transaction({
        "from_account_number": request.from_account,
        "to_account_number": request.to_account,
        "pin": request.pin,
        "type": "transfer",
        "amount": request.amount
    })
    return {"message": "Transfer successful"}


def check_balance_service(request: AccountRequest):
    acc = accounts_collection.find_one({"account_number": request.account_number, "pin": request.pin})
    if not acc:
        raise HTTPException(status_code=404, detail="Invalid account or PIN")
    return {"balance": acc["balance"]}


def change_pin_service(request: ChangePinRequest):
    acc = accounts_collection.find_one({"account_number": request.account_number, "pin": request.old_pin})
    if not acc:
        raise HTTPException(status_code=404, detail="Invalid account or old PIN")
    
    accounts_collection.update_one({"_id": acc["_id"]}, {"$set": {"pin": request.new_pin}})

    accounts_collection.insert_one(change_pin_service)

    return {"message": "PIN updated successfully"}


def kyc_update_service(request: KYCUpdateRequest):
    acc = accounts_collection.find_one({"account_number": request.account_number, "pin": request.pin})
    if not acc:
        raise HTTPException(status_code=404, detail="Invalid account or PIN")
    
    accounts_collection.update_one({"_id": acc["_id"]}, {"$set": {
        "kyc": {
            "aadhaar": request.aadhaar,
            "pan": request.pan,
            "address": request.address,
            "updated_at": datetime.utcnow()
        }
    }})
    accounts_collection.insert_one(kyc_update_service)
    
    return {"message": "KYC updated successfully"}


# ----------------- Loans -----------------
def apply_loan_service(request: LoanRequest):
    acc = accounts_collection.find_one({"account_number": request.account_number, "pin": request.pin})
    if not acc:
        raise HTTPException(status_code=404, detail="Invalid account or PIN")
    
    loan = {
        "account_number": request.account_number,
        "loan_amount": request.loan_amount,
        "pin": request.pin,
        "interest_rate": request.interest_rate,
        "tenure_months": request.tenure_months,

    }
    result = loans_collection.insert_one(loan)
    return {"message": "Loan applied successfully", "loan_id": str(result.inserted_id)}


def repay_loan_service(request: LoanRepayRequest):
    acc = accounts_collection.find_one({"account_number": request.account_number, "pin": request.pin})
    if not acc:
        raise HTTPException(status_code=404, detail="Invalid account or PIN")
    
    repay = {
            "account_number": request.account_number,
            "loan_id": request.loan_id,
            "pin": request.pin,
            "amount": request.amount
    }
    result = loans_collection.insert_one(repay)
    return {"message": "Loan repayment successful", }



def get_loans_service(account_number: str):
    loans = list(loans_collection.find({"account_number": account_number}))
    return {"loans": loans}
