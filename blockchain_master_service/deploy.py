from web3 import Web3
from eth_account import Account
import json
import os
from dotenv import load_dotenv
from solcx import compile_standard, install_solc


def deploy_contract():
    load_dotenv()

    # Install specific solc version
    install_solc("0.8.0")

    # Compile contract
    with open("../contracts/Bank.sol", "r") as file:
        contract_source = file.read()

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"Bank.sol": {"content": contract_source}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.8.0",
    )

    # Save the compilation output
    with open("contract_compiled.json", "w") as file:
        json.dump(compiled_sol, file)

    # Get bytecode and abi
    bytecode = compiled_sol["contracts"]["Bank.sol"]["Bank"]["evm"]["bytecode"]["object"]
    abi = compiled_sol["contracts"]["Bank.sol"]["Bank"]["abi"]

    # Save ABI
    with open("contract_abi.json", "w") as file:
        json.dump(abi, file)

    # Connect to Sepolia
    w3 = Web3(Web3.HTTPProvider(f'https://sepolia.infura.io/v3/{os.getenv("INFURA_PROJECT_ID")}'))

    # Get account from private key
    private_key = os.getenv("PRIVATE_KEY")
    account = Account.from_key(private_key)

    # Create contract
    Bank = w3.eth.contract(abi=abi, bytecode=bytecode)

    # Get nonce
    nonce = w3.eth.get_transaction_count(account.address)

    # Build transaction
    transaction = Bank.constructor().build_transaction(
        {
            "chainId": 11155111,  # Sepolia chain ID
            "gasPrice": w3.eth.gas_price,
            "from": account.address,
            "nonce": nonce,
        }
    )

    # Sign transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

    # Send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print("Deploying contract...")

    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Contract deployed at: {tx_receipt.contractAddress}")

    return tx_receipt.contractAddress, abi


if __name__ == "__main__":
    deploy_contract()
