// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Bank {
    mapping(address => uint256) public balances;
    address public owner;

    event Deposit(address indexed account, uint256 amount);
    event Withdrawal(address indexed account, uint256 amount);
    event Transfer(address indexed from, address indexed to, uint256 amount);

    // Define the Transaction struct
    struct Transaction {
        address from;
        address to;
        uint256 amount;
        string transactionType; // "Deposit", "Withdrawal", or "Transfer"
        uint256 timestamp;
    }

    // Array to store all transactions
    Transaction[] public transactions;

    constructor() {
        owner = msg.sender;
    }

    function deposit() external payable {
        require(msg.value > 0, "Amount must be greater than 0");
        balances[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);

        // Record the deposit transaction
        transactions.push(Transaction({
            from: msg.sender,
            to: address(this), // The contract receives the funds
            amount: msg.value,
            transactionType: "Deposit",
            timestamp: block.timestamp
        }));
    }

    function withdraw(uint256 amount) external {
        require(amount > 0, "Amount must be greater than 0");
        require(balances[msg.sender] >= amount, "Insufficient balance");

        balances[msg.sender] -= amount;
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");

        emit Withdrawal(msg.sender, amount);

        // Record the withdrawal transaction
        transactions.push(Transaction({
            from: address(this), // The contract sends the funds
            to: msg.sender,
            amount: amount,
            transactionType: "Withdrawal",
            timestamp: block.timestamp
        }));
    }

    function transfer(address to, uint256 amount) external {
        require(to != address(0), "Invalid recipient address");
        require(amount > 0, "Amount must be greater than 0");
        require(balances[msg.sender] >= amount, "Insufficient balance");

        balances[msg.sender] -= amount;
        balances[to] += amount;

        emit Transfer(msg.sender, to, amount);

        // Record the transfer transaction
        transactions.push(Transaction({
            from: msg.sender,
            to: to,
            amount: amount,
            transactionType: "Transfer",
            timestamp: block.timestamp
        }));
    }

    function getBalance() external view returns (uint256) {
        return balances[msg.sender];
    }

    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }

    function getTransactions() external view returns (Transaction[] memory) {
        return transactions;
    }
}