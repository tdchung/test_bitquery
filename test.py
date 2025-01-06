import time
import threading
import asyncio

# import socketio
# import nest_asyncio
# from aiohttp import web

from python_graphql_client import GraphqlClient

# from Libs.log import log
# from Libs.utils import (
#     utils_get_price,
# )

# from Libs.bitquery_subscription import (
#     ALL_SOL_TNX_SUBSCRIPTIONS,
#     SOL_PUMPFUN_ALL_BUYS,
#     SOL_PUMPFUN_TO_RAYDIUM,
#     NEW_PUMPFUN_TOKENS,
# )

# from CONFIG import BITQUERY_ACCESS_TOKEN
BITQUERY_ACCESS_TOKEN = f""

# from Libs.utils_trending import utils_trending_list, utils_sol_trending_list
# from CONFIG import TELEGRAM_CHANNEL_TRENDING, DEFAULT_MIN_BUY, MINIMUM_BUY


# from Libs.utils_buybot import (
#     list_tokens_sol,
#     utisl_buybot_channels_from_token,
# )

# from Libs.pumpfun.utils_pumpfun_trend   import utils_pumpfun_trend_tokens
# from Libs.sol.utils_send_sol        import utils_send_sol_buybot
# from Libs.pumpfun.utils_send_pumpfun    import utils_pumpfun_send_message, utils_pumpfun_test
# from Libs.pumpfun.utils_send_pumpfun_to_raydium import test_send_pumpfun_to_raydium

# from Libs.moonshot.utils_moonshot_trend import utils_moonshot_trend_tokens
# from Libs.moonshot.utils_send_moonshot  import utils_send_moonshot_buybot

# from Libs.pumpfun.custom_pumfun_new_launched import pumpfun_new_launch_handler

ALL_SOL_TNX_SUBSCRIPTIONS = """

subscription {
  buybot_sol: Solana {
    DEXTradeByTokens(
      where: {Transaction: 
        {Result: {Success: true}}, 
        Trade: {Side: {Currency: {MintAddress: {notIn: ["So11111111111111111111111111111111111111112", "11111111111111111111111111111111"]}}, 
            Type: {is: sell} }}}
      limit: {count: 500}
    ) {
      Trade {
        Amount
        AmountInUSD
        Currency {
          Symbol
          MintAddress
          Name
        }
        Side {
          Account {
            Address
            Token {
              Owner
            }
          }
          Amount
          AmountInUSD
          Currency {
            Symbol
            MintAddress
            Name
          }
          Order {
            BuySide
          }
          Type
        }
        Dex {
          ProtocolName
          ProtocolFamily
        }
      }
      Transaction {
        Result {
          Success
        }
        Signature
        Signer
      }
    }
  }
}

"""

def log(msg):
    print(f"{time.time()} :: {msg}")

#################################################################
YOUR_ACCESS_TOKEN = BITQUERY_ACCESS_TOKEN
auth_token = f"Bearer {YOUR_ACCESS_TOKEN}"


gWs = GraphqlClient(
    # endpoint="wss://streaming.bitquery.io/graphql",
    endpoint="wss://streaming.bitquery.io/eap",
    headers={"Authorization": auth_token},
)

gLastHashSol = ''


###########################################################################################
def callback_sol_txns(response):
    global gWs
    global gLastHashSol
    try:
        # log(f'[SOL] :: test tset')
        if 'data' in response:
            if 'buybot_sol' in response['data'] and 'DEXTradeByTokens' in response['data']['buybot_sol']:
                try:
                    data = response['data']['buybot_sol']['DEXTradeByTokens']
                    log(f'[SOL] :: new txns data: len {len(data) }')
                    
                    for info in data:
                        log(f"test {info}")
                        # TODO: thread to handle data here
                    
                except Exception as e:
                    log(f"ERROR :: [SOL] :: callback_sol_txns :: {e} ")   
                    
    except Exception as e:
        log(f"ERROR :: [SOL] :: callback_sol_txns :: {e} ")


###########################################################################################
async def  subscribe_sol_all_transfers():
    global gWs
    query = ALL_SOL_TNX_SUBSCRIPTIONS
    variables = {}
    while True:
        try:
            await gWs.subscribe(query=query, handle=callback_sol_txns, variables=variables)
            print(f'INFO  :: [SOL] :: subscribe_sol_all_transfers :: done')
        except Exception as e:
            log(f"ERROR :: [SOL] :: subscribe_sol_all_transfers :: {e} ")


def run_all_sol():
    try:
        asyncio.run(subscribe_sol_all_transfers())
    except Exception as e:
        log(f"ERROR :: [SOL] :: run_all_sol :: {e}")
    
def thread_run_all_sol():
    threading.Thread(
        target=run_all_sol,
        args=(),
    ).start()
    log(f"INFO  :: [SOL] :: thread_run_all_sol :: started")
    

    
    
###########################################################################################
if __name__ == '__main__':
    thread_run_all_sol()
    while True:
        time.sleep(10)
        print(f"12312321")