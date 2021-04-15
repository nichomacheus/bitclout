import argparse
from typing import Union, Dict
import json

from networking.client import BitCloutBaseClient
from transactions.transactions import TransactionHistory, TransactionType


def transaction_info_search(
    client: BitCloutBaseClient, public_key: str, is_mempool: bool = True
) -> Dict[str, Union[int, dict, str]]:
    print("Getting transactions from BitClout servers...")
    http_response = client.get_transaction_info(public_key, is_mempool)
    print("Processing the transactions...")
    transactions = TransactionHistory(http_response.json()["Transactions"]).history
    # just doing something random here as an example of some info we can easily get
    stats = {
        "number_of_{}_type_transactions".format(transaction_type.name): sum(
            map(lambda x: x.transaction_type == transaction_type, transactions)
        )
        for transaction_type in TransactionType
    }
    return {"total_transactions": len(transactions), "per_type_stats": stats}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get transaction stats for some public key"
    )
    parser.add_argument(
        "--public_key", type=str, help="public key you want to look up", required=True
    )
    parser.add_argument("--is_mempool", action='store_true')
    args = parser.parse_args()
    print(
        json.dumps(
            transaction_info_search(
                client=BitCloutBaseClient(),
                public_key=args.public_key,
                is_mempool=args.is_mempool,
            ),
            indent=4,
            sort_keys=True,
        )
    )
