import json
from fastapi import HTTPException, FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from web3 import Web3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Web3 and connect to Sepolia
infura_url = f'https://sepolia.infura.io/v3/{os.getenv("INFURA_PROJECT_ID")}'
w3 = Web3(Web3.HTTPProvider(infura_url))

# Check connection
if not w3.is_connected():
    raise Exception("Failed to connect to Sepolia")

# Load contract ABI
with open("contract_abi.json", "r") as file:
    contract_abi = json.load(file)

# Contract address (replace with your deployed contract address)
contract_address = "0x70E871053B8Fd96c43D6107BCfFb1d9E52949922"

# Create contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (replace with your front-end URL in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Pydantic models for request bodies
class DepositRequest(BaseModel):
    private_key: str
    amount_in_ether: float


class WithdrawRequest(BaseModel):
    private_key: str
    amount_in_ether: float


class TransferRequest(BaseModel):
    private_key: str
    to_address: str
    amount_in_ether: float


class BalanceRequest(BaseModel):
    address: str


# Helper function to send transactions
def send_transaction(private_key, transaction):
    account = w3.eth.account.from_key(private_key)
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    return w3.eth.wait_for_transaction_receipt(tx_hash)


# Endpoints
@app.post("/deposit")
def deposit(request: DepositRequest):
    try:
        amount_in_wei = w3.to_wei(request.amount_in_ether, 'ether')
        nonce = w3.eth.get_transaction_count(w3.eth.account.from_key(request.private_key).address)

        transaction = contract.functions.deposit().build_transaction({
            'from': w3.eth.account.from_key(request.private_key).address,
            'value': amount_in_wei,
            'gas': 210000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
            'chainId': 11155111,  # Sepolia chain ID
        })

        tx_receipt = send_transaction(request.private_key, transaction)
        print("Transaction Receipt:", tx_receipt)  # Log the receipt for debugging
        return {"message": "Deposit successful", "transaction_hash": tx_receipt.transactionHash.hex()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/withdraw")
def withdraw(request: WithdrawRequest):
    try:
        amount_in_wei = w3.to_wei(request.amount_in_ether, 'ether')
        nonce = w3.eth.get_transaction_count(w3.eth.account.from_key(request.private_key).address)

        transaction = contract.functions.withdraw(amount_in_wei).build_transaction({
            'from': w3.eth.account.from_key(request.private_key).address,
            'gas': 210000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
            'chainId': 11155111,
        })

        tx_receipt = send_transaction(request.private_key, transaction)
        return {"message": "Withdrawal successful", "transaction_hash": tx_receipt.transactionHash.hex()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/transfer")
def transfer(request: TransferRequest):
    try:
        amount_in_wei = w3.to_wei(request.amount_in_ether, 'ether')
        nonce = w3.eth.get_transaction_count(w3.eth.account.from_key(request.private_key).address)

        transaction = contract.functions.transfer(request.to_address, amount_in_wei).build_transaction({
            'from': w3.eth.account.from_key(request.private_key).address,
            'gas': 210000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
            'chainId': 11155111,
        })

        tx_receipt = send_transaction(request.private_key, transaction)
        return {"message": "Transfer successful", "transaction_hash": tx_receipt.transactionHash.hex()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/balance")
def get_balance(request: BalanceRequest):
    try:
        # Use the address from the request to call getBalance()
        balance_wei = contract.functions.getBalance().call({'from': request.address})
        balance_eth = w3.from_wei(balance_wei, 'ether')
        return {"address": request.address, "balance_eth": balance_eth}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/contract-balance")
def get_contract_balance():
    try:
        balance_wei = contract.functions.getContractBalance().call()
        balance_eth = w3.from_wei(balance_wei, 'ether')
        return {"contract_balance_eth": balance_eth}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# New endpoint to get transaction history
@app.get("/transactions")
def get_transactions():
    try:
        # Call the getTransactions function from the smart contract
        transactions = contract.functions.getTransactions().call()

        # Format the transactions for JSON response
        formatted_transactions = []
        for tx in transactions:
            formatted_transactions.append({
                "from": tx[0],
                "to": tx[1],
                "amount": w3.from_wei(tx[2], 'ether'),  # Convert amount from wei to ether
                "transactionType": tx[3],
                "timestamp": tx[4]
            })

        return {"transactions": formatted_transactions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
