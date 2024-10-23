import requests
from web3 import Web3
import time

# Replace these with your credentials and API info
INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
PRIVATE_KEY = "your_private_key"
COINBASE_WALLET_ADDRESS = "your_coinbase_wallet_address"
UNISWAP_ROUTER_ADDRESS = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"  # Uniswap V2 router
UNISWAP_ABI = '[...]'  # Replace with Uniswap ABI

web3 = Web3(Web3.HTTPProvider(INFURA_URL))

if web3.isConnected():
    print("Connected to Ethereum network!")
else:
    print("Failed to connect to Ethereum network.")

# Fetch token prices from Dexscreener API
def get_prices(pair_address, chain_id):
    url = f"https://api.dexscreener.com/latest/dex/pairs/{chain_id}/{pair_address}"
    response = requests.get(url)
    data = response.json()

    if 'pair' in data:
        price = float(data['pair']['priceUsd'])
        print(f"Price for {pair_address} on chain {chain_id}: ${price}")
        return price
    else:
        print("Failed to retrieve price.")
        return None

# Detect arbitrage opportunity
def detect_arbitrage(price_1, price_2, threshold=0.01):
    difference = abs(price_1 - price_2)
    if difference / min(price_1, price_2) > threshold:
        print("Arbitrage opportunity detected!")
        return True
    else:
        print("No arbitrage opportunity detected.")
        return False

# Execute a trade on Uniswap
def execute_trade(token_in, token_out, amount_in):
    uniswap_contract = web3.eth.contract(address=UNISWAP_ROUTER_ADDRESS, abi=UNISWAP_ABI)

    # Build the transaction
    tx = uniswap_contract.functions.swapExactTokensForTokens(
        amount_in, 0, [token_in, token_out], COINBASE_WALLET_ADDRESS, int(time.time()) + 60
    ).buildTransaction({
        'from': COINBASE_WALLET_ADDRESS,
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': web3.eth.getTransactionCount(COINBASE_WALLET_ADDRESS),
    })

    # Sign the transaction with your private key
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    print(f"Trade executed! Tx hash: {web3.toHex(tx_hash)}")

# Example usage
if __name__ == "__main__":
    # Replace with real pair addresses and chain IDs
    eth_pair = "0xC40D16476380e4037e6b1A2594cAF6a6cc8Da967"  # Example Ethereum pair
    bsc_pair = "0x0eD7e52944161450477ee417DE9Cd3a859b14fD0"  # Example BSC pair

    eth_price = get_prices(eth_pair, "ethereum")
    bsc_price = get_prices(bsc_pair, "bsc")

    if eth_price and bsc_price:
        if detect_arbitrage(eth_price, bsc_price):
            # Replace with the appropriate token addresses and amounts
            execute_trade(
                token_in="0x6B175474E89094C44Da98b954EedeAC495271d0F",  # DAI on Ethereum
                token_out="0xC40D16476380e4037e6b1A2594cAF6a6cc8Da967",  # Some other token
                amount_in=web3.toWei(1, 'ether')  # 1 DAI
            )
