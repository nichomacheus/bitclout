"""
Wrapper Over Transactions
"""
from enum import Enum

TransactionType = Enum(
    "TransactionType",
    "BASIC_TRANSFER UPDATE_PROFILE FOLLOW CREATOR_COIN SUBMIT_POST LIKE BLOCK_REWARD BITCOIN_EXCHANGE PRIVATE_MESSAGE",
)


class TransactionHistory:
    def __init__(self, history: dict):
        self.history = [Transaction(x) for x in history]


class Transaction:
    def __init__(self, transaction_json: dict):
        # collecting some info for now -- will expand later
        self.transaction_json = transaction_json
        self.transaction_type = TransactionType[transaction_json["TransactionType"]]
        self.metadata = transaction_json.get("TransactionMetadata")
