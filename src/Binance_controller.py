import sys
import os
import json
import hmac
import time
import hashlib
import requests
from urllib.parse import urlencode
from binance.client import Client
import pandas as pd
# import http.client
# import itertools
import string
import random
from colorama import init, Fore
# init(convert=True)
# from MarketTracker import MarketTracker
# from binance.enums import *
# import json
from requests.exceptions import ReadTimeout
from urllib3.exceptions import ReadTimeoutError
from binance.exceptions import BinanceAPIException
# from requests.exceptions import ConnectTimeout
# from urllib3.exceptions import MaxRetryError
# from urllib3.exceptions import ConnectTimeoutError
from socket import timeout
# from colorama import Fore
import math
from urllib3.exceptions import ProtocolError
# from binance.enums import *
from binance.enums import *
import ccxt

# from Get_Etoro_Data import response
# """❤️"""


pd.set_option('display.max_rows', 50000)
pd.set_option('display.max_columns', 50000)
pd.set_option('display.width', 50000)









class Binance_controller:
    def      __init__(self,
                      ticker,
                      demo=False,
                      source="binance_FUTURES",
                      leverage=20,
                      API_KEY=None,
                      SECRET_KEY=None):

        self.demo = demo

        self.source = source

        self.ticker = ticker


        if self.demo is True:


            print(Fore.LIGHTWHITE_EX + "Binance_controller lounched in" + Fore.YELLOW + " DEMO " + Fore.LIGHTWHITE_EX + "mode")
            print("\n")

            if "SPOT" in self.source or "MARGIN" in self.source:
                self.base_url = "https://testnet.binance.vision"

            elif "FUTURES" in self.source or "FUTURES_COIN" in self.source:
                self.base_url = 'https://testnet.binancefuture.com'

            python_client_testnet = True

        else:
            if "SPOT" in self.source or "MARGIN" in self.source:
                self.base_url = 'https://api.binance.com'
            elif "FUTURES" in self.source or "FUTURES_COIN" in self.source:
                self.base_url = 'https://fapi.binance.com'

            print(Fore.LIGHTWHITE_EX + "Binance_controller lounched in" + Fore.GREEN + " REAL TRADING " + Fore.LIGHTWHITE_EX + "mode")
            print("\n")

            python_client_testnet = False

        # if API_KEY is None:

        def get_file_path(initial_file_path: str) -> str:

            base_path = os.path.dirname(os.path.abspath(__file__))

            if getattr(sys, 'frozen', False):
                base_path = os.path.dirname(sys.executable)

            return os.path.join(base_path, initial_file_path)



        if API_KEY and SECRET_KEY:

            self.API_KEY, self.SECRET_KEY = API_KEY, SECRET_KEY

        else:

            with open(get_file_path("bc_keys.json"), "r") as read_file:
                self.bc_API_KEYS = json.load(read_file)
            pass


            if "." not in self.source:

                self.API_KEYS = {

                    'https://api.binance.com': (self.bc_API_KEYS["Main"]["API"],
                                                self.bc_API_KEYS["Main"]["SECRET"]),

                    'https://fapi.binance.com': (self.bc_API_KEYS["Main"]["API"],
                                                self.bc_API_KEYS["Main"]["SECRET"]),
                                 'https://testnet.binancefuture.com':("e81dc4c99c6b2b9f45d0ed7b453220cd4426be350f4422e1a3462260fcf1369d",
                                                                      "730179adf52b1e943e4b2c7420eff43ffdbe7b435bee2df4f6973f3c5daa846d"),
                                 "https://testnet.binance.vision":("NVEI8lqfvIDi6F2jMalQ1iZ7GBenSiTe4Ar3YUB0pvQLJacIl98uIczGq2Wht3qb",
                                                                   "Ss2ywUOlm8UPHyqkYQna1plpcjIRrxnG58YxdDfdTycNmqWdwPkiEPjnmOaE5Lw8")}





            else:

                self.API_KEYS = self.bc_API_KEYS[self.source[::][self.source[::].find(".")+1:][::]]

                self.API_KEYS = {
                    'https://api.binance.com': (self.API_KEYS["API"],
                                                self.API_KEYS["SECRET"]),
                    'https://fapi.binance.com': (self.API_KEYS["API"],
                                                self.API_KEYS["SECRET"]), }


            self.API_KEY, self.SECRET_KEY = self.API_KEYS[self.base_url]



        while True:
            try:


                self.client = Client(api_key=self.API_KEY, api_secret=self.SECRET_KEY, testnet=python_client_testnet)

                self.ccxt_client = ccxt.binanceusdm({
                'apiKey': self.API_KEY,
                'secret': self.SECRET_KEY,
            })

                break

            except Exception as e:

                print(Fore.RED + f"Connection Error occured, while lounching binance python client... Retrying...")
                time.sleep(3)
                pass




        while True:
            try:
                if "FUTURES" in self.source:
                    if "COIN" in self.source:
                        self.client.futures_coin_change_leverage(symbol=ticker,
                                                                 leverage=leverage)
                    else:
                        self.client.futures_change_leverage(symbol=ticker,
                                                            leverage=leverage)

                self.symbol_info = self.get_symbol_info(ticker=self.ticker)


                break

            except Exception as e:
                print(f"{e}")
                time.sleep(5)


        print("self.symbol_info = ", self.symbol_info)

        self.tickers_price_precision = abs(math.floor(math.log(float(self.symbol_info["filters"][0]["tickSize"]), 10)))

        if "FUTURES" in self.source:
            self.tickers_min_lot_size = self.symbol_info["filters"][1]["minQty"]
        elif "SPOT" in self.source:

            self.tickers_min_lot_size = self.symbol_info["filters"][1]["minQty"]



        self.tickers_units_precision = abs(math.floor(math.log(float(self.tickers_min_lot_size), 10)))

        print(Fore.WHITE + f"{self.ticker} symbol_info = \n", self.symbol_info)
        print(Fore.WHITE + f"{self.ticker} price_precision = ", self.tickers_price_precision)
        print(Fore.WHITE + f"{self.ticker} tickers_min_lot_size = ", self.tickers_min_lot_size)
        print(Fore.WHITE + f"{self.ticker} units_precision = ", self.tickers_units_precision)

        """
        Done on Bitcoin. px (magnitude) was 36000 approx
        """

        self.data_path = "D:/SmartSynthetics/WORK/data/"
        self.portfolio_path = self.data_path + "portfolio/"





    def get_ms_timestamp(self, from_Binance=False):


        if from_Binance is True:

            endpoint = "/fapi/v1/time"

            ts = self.request_Binance(http_method="GET", endpoint=endpoint, signed=False)

            ts = ts["serverTime"]

        else:

            ts = int(time.time()*1000)

        return ts




    def hash(self,query_string, SECRET_KEY):
        return hmac.new(key=SECRET_KEY.encode("utf-8"), msg=query_string.encode("utf-8"), digestmod=hashlib.sha256).hexdigest()



    def request_Binance(self,http_method, endpoint, base_url=None, signed=False, payload={}):


        if base_url is None:
            base_url = self.base_url

        API_KEY, SECRET_KEY = self.API_KEYS[base_url]





        session = requests.Session()
        session.headers.update({
                                'Content-Type': 'application/json;charset=utf-8',
                                'X-MBX-APIKEY': API_KEY
                                })

        session = {
                    'GET': session.get,
                    'DELETE': session.delete,
                    'PUT': session.put,
                    'POST': session.post,
                    }[http_method]

        query_string = urlencode(query=payload, doseq=True)



        url = base_url + endpoint

        if signed is True:

            if endpoint != "/fapi/v1/time" and endpoint != "/fapi/v1/ping" and endpoint != "/fapi/v1/exchangeInfo":

                if query_string:
                    query_string = f"{query_string}&timestamp={self.get_ms_timestamp(from_Binance=False)}"

                else:

                    query_string = f"timestamp={self.get_ms_timestamp(from_Binance=False)}"

            url = url + "?" + query_string + "&signature=" + self.hash(query_string, SECRET_KEY=SECRET_KEY)

        else:

            if query_string:
                url = url + "?" + query_string


        print(Fore.WHITE + "sending request to url = ", url)



        response = session(url=url)


        print(Fore.WHITE + "response inside request_Binance = ", response)

        return response.json()



    def set_stop_limit_order(self,
                             ticker,
                             px,
                             stop_price,
                             units,
                             direction
                             ):


        units_precision_string = "{" + f":.{self.tickers_units_precision}" + "f}"

        # print("")

        print(Fore.WHITE + "units, before abs(units) = ", units)

        units = abs(units)

        print(Fore.WHITE + "units, after abs(units) = ", units)

        units = units_precision_string.format(units)

        print(Fore.WHITE + "units, after units_precision_string.format(units) = ", units)

        units = float(units)

        print(Fore.WHITE + "units, after float(units) = ", units)

        print(Fore.WHITE + "units inside set_order = ", units)



        if "FUTURES" in self.source:

            payload = {}

            payload["symbol"] = ticker
            payload["price"] = px
            payload["stopPrice"] = stop_price
            payload["quantity"] = units
            payload["type"] = "STOP"
            payload["priceProtect"] = True
            payload["side"] = ["BUY" if direction > 0 else "SELL"][0]

            order_sent = self.client.futures_create_order(**payload)





        elif "SPOT" in self.source:


            order_sent = self.client.create_oco_order(symbol=ticker,
                                                 side=[SIDE_BUY if direction > 0 else SIDE_SELL][0],
                                                 stopLimitTimeInForce=TIME_IN_FORCE_GTC,
                                                 quantity=units,
                                                 stopPrice=stop_price,
                                                 price=px)




        return order_sent



    def get_order_book(self,
                       ticker=None,
                       depth=50):

        """
        minimum depth is 5

        :param ticker:
        :param depth:
        :return:
        """

        if ticker is None:
            ticker = self.ticker



        payload = {"symbol": ticker,
                   "limit":depth
                   }


        if "FUTURES" in self.source:

            """
            I was not thinking about FUTURES_COIN , when writing this, but it should probably work for them also
            """

            endpoint = "/fapi/v1/depth"
        else:
            """
            not configured
            """
            raise AttributeError

        order_book = self.request_Binance(http_method="GET",
                                          endpoint=endpoint,
                                          signed=True,
                                          payload=payload)


        return order_book



    def set_order(self,
                  px,
                  direction,
                  ticker=None,
                  limit_offset_k = 0,
                  # order_type="LIMIT",
                  order_type="MARKET",
                  units=1,
                  reduce_only=False):




        if order_type == "STOP":
            limit_offset_k = 0.0025

        if ticker is None:
            ticker = self.ticker



        """
        Если в течении минуты ордер не исполнен - отменить ордер
        """

        gen = string.ascii_uppercase + string.ascii_lowercase + string.digits


        """
        Margin order seem to have range of 21
        """


        if self.demo is False:
            coid_rg = 21
        else:
            coid_rg = 22



        ClientOrderId = "".join((random.choice(gen) for n in range(coid_rg)))


        if type(direction) is str:
            side = direction

        else:
            side = ["SELL" if direction < 0 else "BUY"][0]

        units_precision_string = "{" + f":.{self.tickers_units_precision}" + "f}"


        units = abs(units)


        units = units_precision_string.format(units)


        units = float(units)




        payload = {"symbol": ticker,
                   "side": side,
                   "quantity": units,
                   "newClientOrderId": ClientOrderId,
                   }

        # "reduce_only":reduce_only

        if "FUTURES" in self.source:
            payload["reduce_only"] = reduce_only

        binance_market_stops = ["STOP_MARKET", "STOP_LOSS"]
        binance_market__targets = ["TAKE_PROFIT_MARKET", "TAKE_PROFIT"]

        binance_limit_stops = ["STOP", "STOP_LOSS_LIMIT"]

        binance_limit_targets = ["TAKE_PROFIT", "TAKE_PROFIT_LIMIT "]


        price_precision_string = "{" + f":.{self.tickers_price_precision}" + "f}"



        if type(px) == str:
            px = px.replace(",",".")


        print("order_type = ", order_type)


        if px != "market":
            px = float(px)



        if order_type == "LIMIT":

            px = px
            if "FUTURES" in self.source:
                payload["timeInForce"] = "GTX"
            else:
                payload["timeInForce"] = "GTC"



        elif order_type == "LIMIT_MARKET":

            order_book = self.get_order_book(ticker=ticker, depth=5)

            # print("order_book = \n", order_book)
            #
            "ask красный - вверху - продать по ask-у -> продать подороже"
            "bid зеленый - внизу - купить по bid-у -> купить подешевле"

            order_book_bid = order_book["bids"][0][0]
            order_book_ask = order_book["asks"][0][0]



            px = [order_book_bid if direction > 0 else order_book_ask][0]
            # payload["timeInForce"] = "GTC"

            if "FUTURES" in self.source:
                payload["timeInForce"] = "GTX"
            else:
                payload["timeInForce"] = "GTC"



        elif order_type in binance_limit_stops:
            # print("Yes, order is in binance_limit_stops")
            if direction == 1:
                # px = px + px * limit_offset_k
                limit_2_px = px + px * limit_offset_k

                # if limit_offset_k == ""

            elif direction == -1:
                # px = px - px * limit_offset_k
                limit_2_px = px - px * limit_offset_k



            limit_2_px = price_precision_string.format(limit_2_px)
            limit_2_px = float(limit_2_px)

            print(Fore.WHITE + "limit_2_px after price_precision_string.format(limit_2_px) = ", limit_2_px)



        if px == "market":
            order_type = "MARKET"

        else:

            if order_type != "LIMIT_MARKET":
                px = price_precision_string.format(px)
            else:
                order_type = "LIMIT"


            px = float(px)

            """
            36000 BTC = 3.6 USDT slippage
            """


            if order_type == "LIMIT" or order_type == "LIMIT_MARKET":
                payload["price"] = px



            # elif order_type in binance_limit_stops or order_type == "LIMIT_MARKET":
            elif order_type in binance_limit_stops:

                payload["price"] = px
                payload["priceProtect"] = True


                payload["stopPrice"] = px

                # if order_type != "STOP_MARKET":
                payload["price"] = limit_2_px

                # # elif order_type ==

                # else:
                #     """Это же синтетический лимит - мы его переписываем здесь"""
                #     order_type = "LIMIT"

            elif order_type in binance_market_stops:

                payload["stopPrice"] = px



                # if order_type != "MARKET":

                    # if order_type == "LIMIT":
                    #
                    # elif order_type == "LIMIT_MARKET":




                    # else:
                    #     units = "{:.4f}".format(units)
                    #     units = float(units)
                    #     print("units inside set_order = ", units)




            elif order_type in binance_limit_targets:
                """
                Not tested yer
                """

                raise AttributeError

        payload["type"] = order_type

        # print("self.source inside bc.set_order = ", self.source)

        if "FUTURES" in self.source:

            # print(Fore.WHITE + "payload = ", payload)

            if "COIN" in self.source:

                order_sent = self.client.futures_coin_create_order(**payload)



            else:


                """
                Замени на безбиблиотечный посыл
                """

                order_sent = self.client.futures_create_order(**payload)

                """
                binance.exceptions.BinanceAPIException: APIError(code=0): Invalid JSON error message from Binance: <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
                <HTML><HEAD><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">
                <TITLE>ERROR: The request could not be satisfied</TITLE>
                </HEAD><BODY>
                <H1>502 ERROR</H1>
                <H2>The request could not be satisfied.</H2>
                <HR noshade size="1px">
                The origin closed the connection.
                We can't connect to the server for this app or website at this time. There might be too much traffic or a configuration error. Try again later, or contact the app or website owner.
                <BR clear="all">
                If you provide content to customers through CloudFront, you can find steps to troubleshoot and help prevent this error by reviewing the CloudFront documentation.
                <BR clear="all">
                <HR noshade size="1px">
                <PRE>
                Generated by cloudfront (CloudFront)
                Request ID: CcHDq7MkdEVDYjw0vrc9w7P4aCNUker-1xwy-Pqbh6JjA5CRBurt_g==
                </PRE>
                <ADDRESS>
                </ADDRESS>
                </BODY></HTML>
                """


        elif "SPOT" in self.source:

            endpoint = "/api/v3/order"




            if order_type == "LIMIT" or order_type == "LIMIT_MARKET":
                if direction == 1:
                    order_sent = self.client.order_limit_buy(symbol=ticker,
                                                             quantity=payload["quantity"],
                                                             price=payload["price"])

                elif direction == -1:
                    order_sent = self.client.order_limit_sell(symbol=ticker,
                                                              quantity=payload["quantity"],
                                                              price=payload["price"])

            elif order_type == "MARKET":
                if direction == 1:
                    order_sent = self.client.order_market_buy(symbol=ticker,
                                                              quantity=payload["quantity"])

                elif direction == -1:
                    order_sent = self.client.order_market_sell(symbol=ticker,
                                                               quantity=payload["quantity"])


            #
            # elif order_type == "STOP_LIMIT":
            #
            #
            #     if direction == -1:
            #         order = self.client.create_oco_order(
            #                                             symbol=ticker,
            #                                             side=SIDE_SELL,
            #                                             stopLimitTimeInForce=TIME_IN_FORCE_GTC,
            #                                             quantity=payload["quantity"],
            #                                             stopPrice=payload[""],
            #                                             price=px)
            #     elif direction == 1:
            #         order = self.client.create_oco_order(
            #                                             symbol=ticker,
            #                                             side=SIDE_BUY,
            #                                             stopLimitTimeInForce=TIME_IN_FORCE_GTC,
            #                                             quantity=payload["quantity"],
            #                                             stopPrice=payload[""],
            #                                             price=px)


        if "MARGIN" in self.source:


            endpoint = "/sapi/v1/margin/order"


            payload["isIsolated"] = True

            # print("payload = ", payload)


            order_sent = self.request_Binance(http_method="POST",
                                     endpoint=endpoint,
                                     signed=True,
                                     payload=payload
                                     )







        print(Fore.MAGENTA + f"Order with {ClientOrderId} ClientOrderId sent to Binance")

        print(Fore.WHITE + "order which was sent = ", order_sent)

        try:
            if order_sent["msg"] == "Filter failure: MIN_NOTIONAL":
                print(Fore.RED + "Dropping size is smaller than MINIMUM - TB should append it to common drop size to drop it later")
                raise BufferError

            if order_sent["msg"] == "Stop price would trigger immediately.":
                print(Fore.RED + "Stop price would trigger immediately.")
                raise BufferError

        except KeyError:
            print("Order Integrity confirmed...")
            pass

        orderId = order_sent["orderId"]




        return orderId, ClientOrderId, order_sent




            # """
            # test order
            # """

            # order_sent = self.client.create_test_order(
            #     symbol='BTCUSDT',
            #     side=SIDE_BUY,
            #     type=ORDER_TYPE_LIMIT,
            #     timeInForce=TIME_IN_FORCE_GTC,
            #     quantity=1,
            #     price=10000)
            #
            #
            # return order_sent



    def get_order(self,ticker,orderId,ClientOrderId=None):

        while True:
            try:
                if "FUTURES" in self.source:


                    if "COIN" in self.source:

                        if ClientOrderId is None:

                            order = self.client.futures_coin_get_order(symbol=ticker, orderId=orderId)
                        else:
                            order = self.client.futures_coin_get_order(symbol=ticker, orderId=orderId,origClientOrderId=ClientOrderId)

                    else:

                        if ClientOrderId is None:

                            order = self.client.futures_get_order(symbol=ticker,orderId=orderId)
                        else:
                            order = self.client.futures_get_order(symbol=ticker,orderId=orderId,origClientOrderId=ClientOrderId)




                break
            except (ConnectionError,ProtocolError,ConnectionResetError,BinanceAPIException) as e:
                time.sleep(1)
                print(Fore.YELLOW + f"{e} occured in bc.get_order - sleeping for 1 second and retrying")
                pass


        return order


    """
    status "all" сейчас выдает все ордера, кроме открытых
    """
    def get_current_orders(self, ticker=None, status="open"):


        if "FUTURES" in self.source:

            if "COIN" in self.source:

                if status == "open":

                    while True:
                        try:
                            current_orders = self.client.futures_coin_get_open_orders(symbol=ticker)
                            break

                        except Exception as e:
                            print(Fore.YELLOW + f"{e} occured inside get_current_orders -> sleeping and retrying")
                            time.sleep(1)

                elif status == "all":
                    current_orders = self.client.futures_coin_get_all_orders(symbol=ticker)

            else:

                if status == "open":

                    while True:
                        try:
                            current_orders = self.client.futures_get_open_orders(symbol=ticker)
                            break

                        except Exception as e:
                            print(Fore.YELLOW + f"{e} occured inside get_current_orders -> sleeping and retrying")
                            time.sleep(1)


                elif status == "all":

                    current_orders = self.client.futures_get_all_orders(symbol=ticker)



        elif "SPOT" in self.source:

                if status == "open":
                    endpoint = "/api/v3/openOrders"

                    # current_orders = self.client.get_open_orders(symbol=ticker)
                elif status == "all":
                    endpoint = "/api/v3/allOrders"

                    # current_orders = self.client.get_all_orders(symbol=ticker)


                payload = {"symbol":ticker}

                current_orders = self.request_Binance(http_method="GET",
                                                endpoint=endpoint,
                                                signed=True,
                                                payload=payload)




        elif "MARGIN" in self.source:

            if status == "open":


                endpoint = "/sapi/v1/margin/openOrders"




                # current_orders = self.client.get_open_margin_orders(symbol=ticker, isIsolated=True)

            elif status == "all":
                # current_orders = self.client.get_all_margin_orders(symbol=ticker, isIsolated=True)

                endpoint = "/sapi/v1/margin/allOrders"




            payload = {"symbol":ticker,
                       "isIsolated":True}

            current_orders = self.request_Binance(http_method="GET",
                                            endpoint=endpoint,
                                            signed=True,
                                            payload=payload)


        else:
            raise AttributeError

        return current_orders





    @staticmethod
    def random_sleep(minimum, max_k=3):
        """time in seconds
        minimum multiplied on mzxk = maximum"""
        t = random.random() * (max_k - minimum) + minimum
        print(f"Sleeping for {t} seconds...")
        time.sleep(t)
        return t




    def cancel_order(self, ticker=None, orderId=None, ClientOrderId=None):

        if "FUTURES" in self.source:


            if "COIN" in self.source:

                while True:
                    try:
                        canceled_order = self.client.futures_coin_cancel_order(
                                                                               symbol=ticker,
                                                                               orderId=orderId)
                        break
                    except (ReadTimeout, ReadTimeoutError, timeout):
                        Binance_controller.random_sleep(minimum=1)

                        print(Fore.YELLOW + "(ReadTimeout,ReadTimeoutError,timeout) occured in bc.cancel_order - rebooting it...")
                        pass


            else:

                while True:
                    try:
                        canceled_order = self.client.futures_cancel_order(
                                                                        symbol=ticker,
                                                                        orderId=orderId)
                        break
                    except (ReadTimeout,ReadTimeoutError,timeout):
                        Binance_controller.random_sleep(minimum=1)
                        print(Fore.YELLOW + "(ReadTimeout,ReadTimeoutError,timeout) occured in bc.cancel_order - rebooting it...")
                        pass

        elif "SPOT" in self.source:

            canceled_order = self.client.cancel_order(symbol=ticker,
                                                      orderId=orderId)



        elif "MARGIN" in self.source:


            canceled_order = self.client.cancel_margin_order(
                symbol=ticker,
                isIsolated=True,
                orderId=orderId)

        try:
            if canceled_order["msg"] == "Unknown order sent.":
                print(Fore.YELLOW + "There is no such order to cancel!")
                raise BufferError
        except KeyError:
            print("Order cancelation posted successfully")
            pass



        return canceled_order



    def get_futures_margin(self):

        return self.client.futures()


    def get_positions(self,tickers=[]):

        if "FUTURES" in self.source:
            if "COIN" in self.source:


                balance_on_Binance = self.client.futures_account_balance()



                positions = {}

                """
                quote assets
                """
                for b in balance_on_Binance:
                    if b["asset"] in ["BTC","BNB"]:
                        quote_asset = float(b["balance"])
                        positions["q" + b["asset"]] = (quote_asset,1)

                positions_info = self.client.futures_position_information()

                for pi in positions_info:
                    if float(pi["positionAmt"]) != 0:
                        positions[pi["symbol"]] = (float(pi["positionAmt"]), int(pi["leverage"]))

            else:

                balance_on_Binance = self.client.futures_account_balance()

                positions = {}

                """
                quote assets
                """
                for b in balance_on_Binance:
                    if b["asset"] in ["USDT","BUSD","BNB"]:
                        quote_asset = float(b["balance"])
                        positions["q" + b["asset"]] = (quote_asset,1)

                positions_info = self.client.futures_position_information()

                # print("positions_info = ", positions_info)

                for pi in positions_info:
                    if float(pi["positionAmt"]) != 0:
                        # positions[pi["symbol"]] = (float(pi["positionAmt"]), int(pi["leverage"]))
                        positions[pi["symbol"]] = float(pi["positionAmt"])



        elif "SPOT" in self.source:

            endpoint = "/api/v3/account"

            positions = self.request_Binance(http_method="GET",
                                             endpoint=endpoint,
                                             signed=True)

            print("positions = ", positions)

            positions = positions["balances"]


        elif "MARGIN" in self.source:

            endpoint = "/sapi/v1/margin/isolated/account"

            # payload = {"symbols":",USDT".join(asset)}

            payload = {"symbols":ticker}

            balance = self.request_Binance(http_method="GET",
                                            endpoint=endpoint,
                                            signed=True,
                                            payload=payload)

        return positions


    def get_balance(self,
                    # quote_asset="USDT",
                    quote_asset="USDT",
                    positions=None
                    ):

        if "FUTURES" in self.source:




            if positions is None:

                balance = self.client.futures_account_balance()

                # self.ccxt_client.fetch_balance()

                # print("balance = ", balance)


                try:
                    balance = [float(b["balance"]) for b in balance if b["asset"] == quote_asset][0] + [float(b["balance"]) for b in balance if b["asset"] == "BNFCR"][0]
                except IndexError:
                    balance = [float(b["balance"]) for b in balance if b["asset"] == quote_asset][0]


            else:

                print("positions = ", positions)


                balance = float(positions[f"q{quote_asset}"][0])

        elif "SPOT" in self.source:

            balance = float([p["free"] for p in positions if p["asset"] == quote_asset][0])

        return balance




    def get_avg_price(self, ticker, type="all"):

        base_url = 'https://api.binance.com'

        endpoint = "/api/v3/avgPrice"

        payload = {"symbol": ticker}




        current_price = self.request_Binance(http_method="GET",
                                              endpoint=endpoint,
                                              signed=False,
                                              payload=payload,
                                              base_url=base_url)

        current_price = float(current_price["price"])


        if type == "all":

            client_avg_price = self.client.get_avg_price(symbol=ticker)

            client_avg_price = float(client_avg_price["price"])

            endpoint = "/fapi/v1/premiumIndex"


            payload = {"symbol": ticker}


            current_mark_px = self.request_Binance(http_method="GET",
                                                  endpoint=endpoint,
                                                  signed=False,
                                                  payload=payload)

            endpoint = "/fapi/v1/continuousKlines"


            payload = {"pair": ticker,
                       "contractType":"PERPETUAL",
                       "interval":"1m",
                       "limit":"1"}


            perp_contr_px = self.request_Binance(http_method="GET",
                                                  endpoint=endpoint,
                                                  signed=False,
                                                  payload=payload)


            return current_price, client_avg_price, current_mark_px, perp_contr_px

        return current_price

    def get_exchange_info(self):

        if "FUTURES" in self.source:


            if "COIN" in self.source:
                response = self.client.futures_coin_exchange_info()

            else:
                response = self.client.futures_exchange_info()

        elif "SPOT" in self.source:

            response = self.client.get_exchange_info()

        return response

    def get_tradable_tickers(self):

        # if "FUTURES" in self.source:

        ei = self.get_exchange_info()

        ss = ei['symbols']

        tickers = []

        for s in ss:
            t = s["symbol"]
            tickers.append(t)


        return tickers



    def get_symbol_info(self,ticker=None):

        if ticker is None:
            ticker = self.ticker


        if "FUTURES" in self.source:


            if "COIN" in self.source:

                payload = {"symbol": self.ticker}

                response = self.client.futures_coin_exchange_info()

                response = [t for t in response["symbols"] if t["symbol"] == ticker][0]

            else:
                payload = {"symbol":self.ticker}

                response = self.client.futures_exchange_info()

                response = [t for t in response["symbols"] if t["symbol"] == ticker][0]

        else:
            response = self.client.get_symbol_info(ticker)

            print("response = \n", response)





        if "SPOT" in self.source:


            response = self.client.get_symbol_info(ticker)





        return response



    def close_positions(self, positions=None):

        # balance = self.get_positions()

        # print("balance = ", balance)

        if positions is None:
            positions = self.get_positions()

        print(Fore.RED + "CLOSING POSITIONS via MARKET orders")
        print("n")

        closing_orders = []

        for p in positions:
            if "q" not in p:

                units = positions[p][0]

                closing_direction = [-1 if units > 0 else 1][0]

                units = abs(units)


                print(Fore.WHITE + "ticker = ", p)
                print(Fore.WHITE + "units = ", units)
                print(Fore.WHITE + "closing_direction = ", closing_direction)
                print("\n")


                try:
                    co = self.set_order(px="market",
                                   direction=closing_direction,
                                   ticker=p,
                                   units=units)

                    closing_orders.append(co)

                except BinanceAPIException:
                    print("passing..")

        return closing_orders


if __name__ == "__main__":


    ticker = "XRPUSDT"

    # leverage = 40
    leverage = 20



    demo = False




    bc = Binance_controller(
                            demo=demo,
                            # API_KEY="aY880RCnTg1cg5PmSbxs9wHNgpdc0dgBVqPvaAiDJ1TYhFA4K1twTsMK7FhXpoVk",
                            # SECRET_KEY="fbMyxiRSrWk2wGEWgkkaSvSnpCedLyxUnsCZv8RXetQL8rtQJbM9z0HLRVJjnjxh",
                            source="binance_FUTURES",
                            # source="binance_SPOT",
                            leverage=leverage,
                            ticker=ticker
                            )


    x = bc.client.get_products()


    print("x = ", x["data"][0])



