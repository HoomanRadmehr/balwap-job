from web3 import Web3
from dotenv import load_dotenv
import threading
import os 
import logging
import traceback


load_dotenv()

provider = os.getenv("BALTIC_W3_HTTP_PROVIDER")
contract_address = os.getenv("BALTIC_CONTRACT_ADDRESS")
contract_abi = os.getenv("BALTIC_CONTRACT_ABI")
owner_public_key = os.getenv("BALTIC_OWNER_PUBLIC_KEY_ADDRESS")
private_key = os.getenv("BALTIC_PRIVATE_KEY")


def run_balwap():
    w3 = Web3(Web3.HTTPProvider(provider))
    baltic = w3.eth.contract(contract_address,abi=contract_abi)
    nonce = w3.eth.get_transaction_count(owner_public_key) 
    addresses = []
    i=0
    while True:
        try:
            addresses.append(baltic.functions.registeredUsers(i).call())
            i=+1
        except:
            break

    for address in addresses:
        try:
            balwap_txn = baltic.functions.balwap(address).build_transaction(
                {
                    'chainId': 137,
                    'gas': 7000000,
                    'maxFeePerGas': w3.to_wei('200', 'gwei'),
                    'maxPriorityFeePerGas': w3.to_wei('130', 'gwei'),
                    'nonce': nonce,
                }
            )
            
            sign_transaction = w3.eth.account.sign_transaction(balwap_txn,private_key=private_key)
            print(w3.to_hex(sign_transaction.hash))
            w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
            threading.Timer(1*60*60,run_balwap).start()
        except:
            logging.error(traceback.format_exc())

run_balwap()
