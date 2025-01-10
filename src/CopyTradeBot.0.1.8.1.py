import time
import PySimpleGUI as sg
from Binance_controller import Binance_controller
from colorama import init,Fore
init(convert=True)
import json
import sys
import os

class CopyTradeBot:

    def __init__(self,
                 listening_step_ms=1000,
                 ):

        self.FUTURES_TICKERS = ["1000SHIB",
                                "1000XEC",
                                "1INCH",
                                "AAVE",
                                "ADA",
                                "AKRO",
                                "ALICE",
                                "ALPHA",
                                "APE","AR","ATA","ATOM","AUDIO","AVAX","AXS","BAKE","BAL","BAND","BAT","BCH","BEL","BLZ","BNB","BTCDOM","BTCST","BTC","BTS","C98","CELO","CELR","CHR","CNY","COMP","COTI","CRV","CTK","CVC","DASH","DEFI","DENT","DGB","DODO","DOGE","DOT","DYDX","EGLD","ENJ","EOS","ETC","ETH","FIL","FLM","FTM","GALA","GRT","GTC","HBAR","HNT","HOT","ICP","ICX","IOST","IOTA","IOTX","KAVA","KNS","KSM","LINA","LINK","LIT","LRC","LTC","MANA","MASK","MATIC","MTR","MTL","NEAR","NEO","NKN","OCEAN","OGN","OMG","ONE","ONT","QTUM","RAY","REEF","REN","RLC","RSR","RUNE","RVN","SC","SFP","SKL","SNX","SOL","SRM","STMX","STORJ","SUSHI","SXP","THETA","TLM","TOMO","TRB","TRX","UNFI","UNI","VET","WAVES","XEM","XLM","XMR","XRP","XTZ","YFI","ZEC","ZEN","ZIL","ZRX"]

        self.ticker = "BTC"

        self.source = "binance_FUTURES"

        self.QUOTE_ASSET = "USDT"

        self.leverage = 20

        self.listening_step_ms = listening_step_ms

        self.current_time = time.time()

        self.mode = "MANUAL"




        layout = [
                 [sg.Text(text="MAIN.API:")],
                 [sg.InputText(key="MAIN.API")],
                 [sg.Text(text="MAIN.SECRET:")],
                 [sg.InputText(key="MAIN.SECRET")],
                 [sg.Text(text="...")],
                 [sg.Text(text="copy1.API:")],
                 [sg.InputText(key="copy1.API")],
                 [sg.Text(text="copy1.SECRET:")],
                 [sg.InputText(key="copy1.SECRET")],
                 [sg.Text(text="copy2.API:")],
                 [sg.InputText(key="copy2.API")],
                 [sg.Text(text="copy2.SECRET:")],
                 [sg.InputText(key="copy2.SECRET")],
                 [sg.Text(text="copy3.API:")],
                 [sg.InputText(key="copy3.API")],
                 [sg.Text(text="copy3.SECRET:")],
                 [sg.InputText(key="copy3.SECRET")],
                 [sg.Text(text="copy4.API:")],
                 [sg.InputText(key="copy4.API")],
                 [sg.Text(text="copy4.SECRET:")],
                 [sg.InputText(key="copy4.SECRET")],
                 [sg.Text(text="copy5.API:")],
                 [sg.InputText(key="copy5.API")],
                 [sg.Text(text="copy5.SECRET:")],
                 [sg.InputText(key="copy5.SECRET")],
                 [sg.Button(button_text="START")],
                 [sg.Button(button_text="LOAD keys.json + START")],
                 ]


        self.window = sg.Window("Copy-Trade by Kirill P.", layout,
                                background_color="gray")




        def get_file_path(initial_file_path: str) -> str:

            base_path = os.path.dirname(os.path.abspath(__file__))

            if getattr(sys, 'frozen', False):
                base_path = os.path.dirname(sys.executable)

            return os.path.join(base_path, initial_file_path)


        self.event, self.values = self.window.Read()


        self.ctb_API_KEYS = {}

        self.ctb_API_KEYS["copy"] = []


        if self.event == "START":

            self.ctb_API_KEYS["main_API"] = self.values["MAIN.API"]

            self.ctb_API_KEYS["main_SECRET"] = self.values["MAIN.SECRET"]

            if self.values["copy1.API"] != "":

                self.ctb_API_KEYS["copy"].append({"API": self.values["copy1.API"],
                                                  "SECRET": self.values["copy1.SECRET"],
                                                  "label": "copy1"})

            if self.values["copy2.API"] != "":
                self.ctb_API_KEYS["copy"].append({"API": self.values["copy2.API"],
                                                  "SECRET": self.values["copy2.SECRET"],
                                                  "label": "copy2"})

            if self.values["copy3.API"] != "":
                self.ctb_API_KEYS["copy"].append({"API": self.values["copy3.API"],
                                                  "SECRET": self.values["copy3.SECRET"],
                                                  "label": "copy3"})

            if self.values["copy4.API"] != "":
                self.ctb_API_KEYS["copy"].append({"API": self.values["copy4.API"],
                                                  "SECRET": self.values["copy4.SECRET"],
                                                  "label": "copy4"})

            if self.values["copy5.API"] != "":
                self.ctb_API_KEYS["copy"].append({"API": self.values["copy5.API"],
                                                  "SECRET": self.values["copy5.SECRET"],
                                                  "label": "copy5"})


        elif self.event == "LOAD keys.json + START":
            # with open("C:/ctb_API_KEYS.json", "r") as read_file:
            with open(get_file_path("keys.json"), "r") as read_file:
                self.ctb_API_KEYS = json.load(read_file)
            pass

        self.window.close()

        while True:

            try:

                self.bc_main = Binance_controller(ticker=self.ticker + self.QUOTE_ASSET,
                                                  demo=False,
                                                  source=self.source,
                                                  leverage=self.leverage,
                                                  API_KEY=self.ctb_API_KEYS["main_API"],
                                                  SECRET_KEY=self.ctb_API_KEYS["main_SECRET"])
                break
            except Exception as e:
                print(f"{e}")
                time.sleep(7)


        positions = self.bc_main.get_positions()

        self.current_balance = self.bc_main.get_balance(positions=positions,
                                                        quote_asset=self.QUOTE_ASSET)




        self.bc_copy = []



        self.copy_balances = []

        for ak_sk in self.ctb_API_KEYS["copy"]:

            bc_c = Binance_controller(ticker=self.ticker + self.QUOTE_ASSET,
                                      demo=False,
                                      source=self.source,
                                      leverage=self.leverage,
                                      API_KEY=ak_sk["API"],
                                      SECRET_KEY=ak_sk["SECRET"])

            self.bc_copy.append(bc_c)

            positions = bc_c.get_positions()

            copy_balance = bc_c.get_balance(positions=positions,
                                            quote_asset=self.QUOTE_ASSET)

            self.copy_balances.append(copy_balance)

        print(Fore.WHITE + "compy accounts detected: ", len(self.bc_copy))

        self.ignore_orders_oids = []

    def init_interface(self):

        layout = [
                 [sg.Combo(['USD-M FUTURES', "SPOT"], default_value="USD-M FUTURES", auto_size_text=True,size=20, key="source")],
                 [sg.Combo(self.FUTURES_TICKERS, default_value=self.ticker, auto_size_text=True,key="ticker")],
                 [sg.Button("LISTENING OFF", button_color="gray", key="LISTENING")],
                 # [sg.Checkbox("LISTENING", default=False, key="LISTENING")],
                 [sg.Button("CLOSE TICKER POSITIONS", button_color="purple"),
                  sg.Button("CANCEL TICKER ORDERS", button_color="purple")],
                 [sg.Button("CLOSE ALL POSITIONS", button_color="purple")],
                 [sg.Text(f"Avbl: {self.current_balance} USDT", key="balance")],
                 [sg.Text(f"copy_balances: {self.copy_balances} USDT", key="copy_balances")],
                 # [sg.Button("Limit/Market"), sg.Button("Stop Limit")],
                 [sg.Text("Limit Price")],
                 [sg.InputText(key="px")],
                 [sg.Text("Size %:")],
                 [sg.InputText(key="position_volume_percent")],
                 [sg.Text("Take Profit")],
                 [sg.InputText(key="TAKE_PROFIT")],
                 [sg.Text("Stop Loss")],
                 [sg.InputText(key="STOP_LOSS")],
                 # [sg.Checkbox('Reduce-Only', default=False)],
                 [sg.Button("Buy/Long", button_color="green"),sg.Button("Sell/Short", button_color="red")],
                 ]


        self.window = sg.Window("Copy-Trade", layout,
                                background_color="gray")


        listening_loop_start_time = time.time()


        print("self.bc_copy before starting the While loop = ", self.bc_copy)

        while True:


            self.event, self.values = self.window.Read(timeout=1000)

            print(Fore.WHITE + "self.values = ", self.values)

            if self.values["ticker"] != self.ticker:# and self.values["ticker"] in self.FUTURES_TICKERS:

                if self.values["ticker"] in self.FUTURES_TICKERS:

                    self.bc_main = Binance_controller(ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                      demo=False,
                                                      source=self.values["source"],
                                                      leverage=self.leverage,
                                                      API_KEY=self.ctb_API_KEYS["main_API"],
                                                      SECRET_KEY=self.ctb_API_KEYS["main_SECRET"])

                    positions = self.bc_main.get_positions()

                    self.current_balance = self.bc_main.get_balance(positions=positions,
                                                                    quote_asset=self.QUOTE_ASSET)

                    self.bc_copy = []

                    self.copy_balances = []


                    try:
                        self.window["balance"].update(self.current_balance)
                    except Exception:

                        pass


                    for ak_sk in self.ctb_API_KEYS["copy"]:

                        bc_c = Binance_controller(ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                  demo=False,
                                                  source=self.values["source"],
                                                  leverage=self.leverage,
                                                  API_KEY=ak_sk["API"],
                                                  SECRET_KEY=ak_sk["SECRET"])

                        self.bc_copy.append(bc_c)

                        positions = bc_c.get_positions()

                        copy_balance = bc_c.get_balance(positions=positions,
                                                        quote_asset=self.QUOTE_ASSET)

                        self.copy_balances.append(copy_balance)

                    self.ticker = self.values["ticker"]
                else:
                    print(Fore.YELLOW + "ticker not listed...")

            print(Fore.WHITE + "self.bc_main.source = ", self.bc_main.source)
            print(Fore.WHITE + "self.values['source'] = ", self.values["source"])

            if self.values["source"] == 'USD-M FUTURES' and self.bc_main.source == "binance_SPOT":



                self.bc_main = Binance_controller(ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                  demo=False,
                                                  source="binance_FUTURES",
                                                  leverage=self.leverage,
                                                  API_KEY=self.ctb_API_KEYS["main_API"],
                                                  SECRET_KEY=self.ctb_API_KEYS["main_SECRET"])

                positions = self.bc_main.get_positions()

                self.current_balance = self.bc_main.get_balance(positions=positions,
                                                                quote_asset=self.QUOTE_ASSET)

                self.bc_copy = []

                self.copy_balances = []

                self.window["balance"].update(self.current_balance)

                # self.bc_main.source = 'USD-M FUTURES'

                for ak_sk in self.ctb_API_KEYS["copy"]:

                    bc_c = Binance_controller(ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                              demo=False,
                                              source="binance_FUTURES",
                                              leverage=self.leverage,
                                              API_KEY=ak_sk["API"],
                                              SECRET_KEY=ak_sk["SECRET"])

                    self.bc_copy.append(bc_c)

                    positions = bc_c.get_positions()

                    copy_balance = bc_c.get_balance(positions=positions,
                                                    quote_asset=self.QUOTE_ASSET)

                    self.copy_balances.append(copy_balance)

            if self.values["source"] == 'SPOT' and self.bc_main.source == "binance_FUTURES":

                self.bc_main = Binance_controller(ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                  demo=False,
                                                  source="binance_SPOT",
                                                  leverage=self.leverage,
                                                  API_KEY=self.ctb_API_KEYS["main_API"],
                                                  SECRET_KEY=self.ctb_API_KEYS["main_SECRET"])

                positions = self.bc_main.get_positions()

                self.current_balance = self.bc_main.get_balance(positions=positions,
                                                                quote_asset=self.QUOTE_ASSET)

                self.window["balance"].update(self.current_balance)

                self.bc_copy = []

                self.copy_balances = []

                # self.bc_main.source = 'USD-M SPOT'

                for ak_sk in self.ctb_API_KEYS["copy"]:
                    bc_c = Binance_controller(ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                              demo=False,
                                              source="binance_SPOT",
                                              leverage=self.leverage,
                                              API_KEY=ak_sk["API"],
                                              SECRET_KEY=ak_sk["SECRET"])

                    self.bc_copy.append(bc_c)

                    positions = bc_c.get_positions()

                    copy_balance = bc_c.get_balance(positions=positions,
                                                    quote_asset=self.QUOTE_ASSET)

                    self.copy_balances.append(copy_balance)

            # print(Fore.WHITE + "self.values beggining = ", self.values)

            if self.event in (None, 'Exit'):
                break

            self.current_time = time.time()

            if self.event in ["CLOSE TICKER POSITIONS",
                              "CANCEL TICKER ORDERS",
                              "CLOSE TICKER POSITIONS",
                              "CLOSE ALL POSITIONS"]:

                self.positions_orders_closing(event=self.event,
                                              ticker_with_quote_asset=self.values["ticker"] + self.QUOTE_ASSET)

                self.new_archived_orders = self.bc_main.get_current_orders(ticker=listening_ticker + self.QUOTE_ASSET,
                                                                           status="all")

                self.archived_orders = self.new_archived_orders



            if self.event in ["Sell/Short","Buy/Long"]:

                self.values['px'] = self.values['px'].replace(',', ".")

                print(Fore.WHITE + "self.values['position_volume_percent'] = ", self.values["position_volume_percent"])
                print(Fore.WHITE + "self.current_balance = ", self.current_balance)
                print(Fore.WHITE + "float(self.values['px'] = ", float(self.values['px']))

                if self.values["source"] == "SPOT":


                    self.leverage = 1


                try:
                    self.units = ((float(self.values["position_volume_percent"]) * 0.01 * self.current_balance) * self.leverage) / float(self.values["px"])
                except ValueError:
                    print(Fore.WHITE + "Something wrong with units...")
                    self.window.close()

                    layout = [
                        [sg.Combo(['USD-M FUTURES', "SPOT"], default_value="USD-M FUTURES", auto_size_text=True,
                                  size=20, key="source")],
                        [sg.Combo(self.FUTURES_TICKERS, default_value=self.values["ticker"], auto_size_text=True,
                                  key="ticker")],
                        [sg.Button("LISTENING OFF", button_color="gray", key="LISTENING")],
                        [sg.Button("CLOSE TICKER POSITIONS", button_color="purple"),
                         sg.Button("CANCEL TICKER ORDERS", button_color="purple")],
                        [sg.Button("CLOSE ALL POSITIONS", button_color="purple")],
                        [sg.Text(f"Avbl: {self.current_balance} USDT",key="balance")],
                        [sg.Text(f"copy_balances: {self.copy_balances} USDT", key="copy_balances")],
                        [sg.Text("Limit Price")],
                        [sg.InputText(key="px")],
                        [sg.Text("Size %:")],
                        [sg.InputText(key="position_volume_percent")],
                        [sg.Text("Take Profit")],
                        [sg.InputText(key="TAKE_PROFIT")],
                        [sg.Text("Stop Loss")],
                        [sg.InputText(key="STOP_LOSS")],
                        [sg.Button("Buy/Long", button_color="green"), sg.Button("Sell/Short", button_color="red")],
                        [sg.Text("Invalid position_volume_percent")]
                    ]

                    self.window = sg.Window("Copy-Trade",
                                            layout,
                                            background_color="gray")




                try:

                    if self.event == "Sell/Short":

                        if self.values["px"] != '':

                            """
                            Limit Order
                            """

                            self.bc_main.set_order(px=float(self.values["px"]),direction=-1,
                                                 ticker=self.values["ticker"]+"USDT",
                                                 units=self.units)



                            if self.values["TAKE_PROFIT"] != '':
                                self.bc_main.set_order(px=float(self.values["TAKE_PROFIT"]), direction=1,
                                             ticker=self.values["ticker"] + "USDT",
                                             units=self.units)


                            if self.values["STOP_LOSS"] != '':
                                self.bc_main.set_order(px=float(self.values["STOP_LOSS"]), direction=1,
                                                       order_type=["STOP_MARKET" if "FUTURES" in self.values["source"] else "STOP_LOSS"][0],
                                                       ticker=self.values["ticker"] + "USDT",
                                                       units=self.units)


                            print(Fore.WHITE + "self.bc_copy before self.bc_copy loop = ", self.bc_copy)

                            for bcc in self.bc_copy:

                                print(Fore.WHITE + "entered the self.bc_copy loop...")

                                """
                                open Limit orders price is "price"
                                Limits done
                                """
                                target_copy_balance = self.copy_balances[self.bc_copy.index(bcc)]

                                print(Fore.WHITE + "target_copy_balance = ", target_copy_balance)

                                copy_units = ((float(self.values["position_volume_percent"]) * 0.01 * target_copy_balance) * self.leverage) / float(self.values["px"])

                                print(Fore.WHITE + "copy_units = ", copy_units)

                                orderId, ClientOrderId, order_sent = bcc.set_order(px=float(self.values["px"]),
                                                                                   direction=-1,
                                                                                   ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                                                   units=copy_units)

                                if self.values["TAKE_PROFIT"] != '':

                                    """
                                    open Limit orders price is "price"
                                    Limits done
                                    """
                                    target_copy_balance = self.copy_balances[self.bc_copy.index(bcc)]

                                    print(Fore.WHITE + "target_copy_balance = ", target_copy_balance)

                                    copy_units = ((float(self.values["position_volume_percent"]) * 0.01 * target_copy_balance) * self.leverage) / float(self.values["px"])

                                    print(Fore.WHITE + "copy_units = ", copy_units)

                                    orderId, ClientOrderId, order_sent = bcc.set_order(px=float(self.values["TAKE_PROFIT"]),
                                                                                       direction=1,
                                                                                       ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                                                       units=copy_units)


                                if self.values["STOP_LOSS"] != '':

                                    """
                                    open Limit orders price is "price"
                                    Limits done
                                    """
                                    target_copy_balance = self.copy_balances[self.bc_copy.index(bcc)]

                                    print(Fore.WHITE + "target_copy_balance = ", target_copy_balance)

                                    copy_units = ((float(self.values["position_volume_percent"]) * 0.01 * target_copy_balance) * self.leverage) / float(self.values["px"])

                                    print(Fore.WHITE + "copy_units = ", copy_units)

                                    orderId, ClientOrderId, order_sent = bcc.set_order(px=float(self.values["STOP_LOSS"]),
                                                                                       order_type=["STOP_MARKET" if "FUTURES" in self.values["source"] else "STOP_LOSS"][0],
                                                                                       direction=1,
                                                                                       ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                                                       units=copy_units)

                        else:

                            """
                            Market Order
                            """

                            self.bc_main.set_order(px="market", direction=-1,
                                         ticker=self.values["ticker"] + "USDT",
                                         units=self.units)



                            if self.values["TAKE_PROFIT"] != '':
                                self.bc_main.set_order(px=float(self.values["TAKE_PROFIT"]), direction=1,
                                             ticker=self.values["ticker"] + "USDT",
                                             units=self.units)


                            if self.values["STOP_LOSS"] != '':
                                self.bc_main.set_order(px=float(self.values["STOP_LOSS"]), direction=1,
                                                       order_type=["STOP_MARKET" if "FUTURES" in self.values["source"] else "STOP_LOSS"][0],
                                                       ticker=self.values["ticker"] + "USDT",
                                                       units=self.units)



                            for bcc in self.bc_copy:
                                """
                                open Limit orders price is "price"
                                Limits done
                                """
                                target_copy_balance = self.copy_balances[self.bc_copy.index(bcc)]

                                print(Fore.WHITE + "target_copy_balance = ", target_copy_balance)

                                copy_units = ((float(self.values["position_volume_percent"]) * 0.01 * target_copy_balance) * self.leverage) / float(self.values["px"])

                                print(Fore.WHITE + "copy_units = ", copy_units)


                                orderId, ClientOrderId, order_sent = bcc.set_order(px=float(self.values["px"]),
                                                                                   direction=-1,
                                                                                   ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                                                   units=copy_units)






                                if self.values["TAKE_PROFIT"] != '':

                                    """
                                    open Limit orders price is "price"
                                    Limits done
                                    """
                                    target_copy_balance = self.copy_balances[self.bc_copy.index(bcc)]

                                    print(Fore.WHITE + "target_copy_balance = ", target_copy_balance)

                                    copy_units = ((float(self.values["position_volume_percent"]) * 0.01 * target_copy_balance) * self.leverage) / float(self.values["px"])

                                    print(Fore.WHITE + "copy_units = ", copy_units)

                                    orderId, ClientOrderId, order_sent = bcc.set_order(px=float(self.values["TAKE_PROFIT"]),
                                                                                       direction=1,
                                                                                       ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                                                       units=copy_units)


                                if self.values["STOP_LOSS"] != '':

                                    """
                                    open Limit orders price is "price"
                                    Limits done
                                    """
                                    target_copy_balance = self.copy_balances[self.bc_copy.index(bcc)]

                                    print(Fore.WHITE + "target_copy_balance = ", target_copy_balance)

                                    copy_units = ((float(self.values["position_volume_percent"]) * 0.01 * target_copy_balance) * self.leverage) / float(self.values["px"])

                                    print(Fore.WHITE + "copy_units = ", copy_units)

                                    orderId, ClientOrderId, order_sent = bcc.set_order(px=float(self.values["STOP_LOSS"]),
                                                                                       order_type=["STOP_MARKET" if "FUTURES" in self.values["source"] else "STOP_LOSS"][0],
                                                                                       direction=1,
                                                                                       ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                                                       units=copy_units)



                    if self.event == "Buy/Long":

                        if self.values["px"] != '':

                            """
                            Limit Order
                            """

                            self.bc_main.set_order(px=float(self.values["px"]),direction=1,
                                                   ticker=self.values["ticker"]+self.QUOTE_ASSET,
                                                   units=self.units)

                            if self.values["TAKE_PROFIT"] != '':
                                self.bc_main.set_order(px=float(self.values["TAKE_PROFIT"]), direction=-1,
                                             ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                             units=self.units)

                            if self.values["STOP_LOSS"] != '':
                                self.bc_main.set_order(px=float(self.values["STOP_LOSS"]), direction=-1,
                                                       order_type=["STOP_MARKET" if "FUTURES" in self.values["source"] else "STOP_LOSS"][0],
                                                       ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                       units=self.units)



                            for bcc in self.bc_copy:



                                """
                                open Limit orders price is "price"
                                Limits done
                                """
                                target_copy_balance = self.copy_balances[self.bc_copy.index(bcc)]

                                print(Fore.WHITE + "target_copy_balance = ", target_copy_balance)

                                copy_units = ((float(self.values["position_volume_percent"]) * 0.01 * target_copy_balance) * self.leverage) / float(self.values["px"])

                                print(Fore.WHITE + "copy_units = ", copy_units)

                                orderId, ClientOrderId, order_sent = bcc.set_order(px=float(self.values["px"]),
                                                                                   direction=1,
                                                                                   ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                                                   units=copy_units)

                                if self.values["TAKE_PROFIT"] != '':

                                    """
                                    open Limit orders price is "price"
                                    Limits done
                                    """

                                    target_copy_balance = self.copy_balances[self.bc_copy.index(bcc)]

                                    print(Fore.WHITE + "target_copy_balance = ", target_copy_balance)

                                    copy_units = ((float(self.values["position_volume_percent"]) * 0.01 * target_copy_balance) * self.leverage) / float(self.values["px"])

                                    print(Fore.WHITE + "copy_units = ", copy_units)

                                    orderId, ClientOrderId, order_sent = bcc.set_order(px=float(self.values["TAKE_PROFIT"]),
                                                                                       direction=-1,
                                                                                       ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                                                       units=copy_units)

                                if self.values["STOP_LOSS"] != '':

                                    """
                                    open Limit orders price is "price"
                                    Limits done
                                    """
                                    target_copy_balance = self.copy_balances[self.bc_copy.index(bcc)]

                                    print(Fore.WHITE + "target_copy_balance = ", target_copy_balance)

                                    copy_units = ((float(self.values["position_volume_percent"]) * 0.01 * target_copy_balance) * self.leverage) / float(self.values["px"])

                                    print(Fore.WHITE + "copy_units = ", copy_units)

                                    orderId, ClientOrderId, order_sent = bcc.set_order(px=float(self.values["STOP_LOSS"]),
                                                                                       order_type=["STOP_MARKET" if "FUTURES" in self.values["source"] else "STOP_LOSS"][0],
                                                                                       direction=-1,
                                                                                       ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                                                       units=copy_units)


                        else:

                            """
                            Market Order
                            """

                            self.bc_main.set_order(px="market",
                                                   direction=1,
                                                   ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                   units=self.units)


                            if self.values["TAKE_PROFIT"] != '':
                                self.bc_main.set_order(px=float(self.values["TAKE_PROFIT"]),
                                                       direction=-1,
                                                       ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                       units=self.units)




                            if self.values["STOP_LOSS"] != '':
                                self.bc_main.set_order(px=float(self.values["STOP_LOSS"]),
                                                       order_type=["STOP_MARKET" if "FUTURES" in self.values["source"] else "STOP_LOSS"][0],
                                                       direction=-1,
                                                       ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                       units=self.units)




                            for bcc in self.bc_copy:
                                """
                                open Limit orders price is "price"
                                Limits done
                                """
                                target_copy_balance = self.copy_balances[self.bc_copy.index(bcc)]

                                print(Fore.WHITE + "target_copy_balance = ", target_copy_balance)

                                copy_units = ((float(self.values["position_volume_percent"]) * 0.01 * target_copy_balance) * self.leverage) / float(self.values["px"])

                                print(Fore.WHITE + "copy_units = ", copy_units)

                                orderId, ClientOrderId, order_sent = bcc.set_order(px="market",
                                                                                   direction=1,
                                                                                   ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                                                   units=copy_units)

                                if self.values["TAKE_PROFIT"] != '':

                                    """
                                    open Limit orders price is "price"
                                    Limits done
                                    """
                                    target_copy_balance = self.copy_balances[self.bc_copy.index(bcc)]

                                    print("target_copy_balance = ", target_copy_balance)

                                    copy_units = ((float(self.values["position_volume_percent"]) * 0.01 * target_copy_balance) * self.leverage) / float(self.values["px"])

                                    print("copy_units = ", copy_units)

                                    orderId, ClientOrderId, order_sent = bcc.set_order(px=float(self.values["TAKE_PROFIT"]),
                                                                                       direction=-1,
                                                                                       ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                                                       units=copy_units)


                                if self.values["STOP_LOSS"] != '':

                                    """
                                    open Limit orders price is "price"
                                    Limits done
                                    """
                                    target_copy_balance = self.copy_balances[self.bc_copy.index(bcc)]

                                    print("target_copy_balance = ", target_copy_balance)

                                    copy_units = ((float(self.values["position_volume_percent"]) * 0.01 * target_copy_balance) * self.leverage) / float(self.values["px"])

                                    print("copy_units = ", copy_units)

                                    orderId, ClientOrderId, order_sent = bcc.set_order(px=float(self.values["STOP_LOSS"]),
                                                                                       order_type=["STOP_MARKET" if "FUTURES" in self.values["source"] else "STOP_LOSS"][0],
                                                                                       direction=-1,
                                                                                       ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                                                       units=copy_units)



                except Exception as e:


                    print(f"{e}")


                    self.window.close()


                    layout = [
                        [sg.Combo(['USD-M FUTURES', "SPOT"], default_value="USD-M FUTURES", auto_size_text=True,
                                  size=20, key="source")],
                        [sg.Combo(self.FUTURES_TICKERS, default_value=self.values["ticker"], auto_size_text=True,
                                  key="ticker")],
                        [sg.Button("LISTENING OFF", button_color="gray", key="LISTENING")],
                        [sg.Button("CLOSE TICKER POSITIONS", button_color="purple"),
                         sg.Button("CANCEL TICKER ORDERS", button_color="purple")],
                        [sg.Button("CLOSE ALL POSITIONS", button_color="purple")],
                        [sg.Text(f"Avbl: {self.current_balance} USDT")],
                        [sg.Text(f"copy_balances: {self.copy_balances} USDT", key="copy_balances")],
                        [sg.Text("Limit Price")],
                        [sg.InputText(key="px")],
                        [sg.Text("Size %:")],
                        [sg.InputText(key="position_volume_percent")],
                        [sg.Text("Take Profit")],
                        [sg.InputText(key="TAKE_PROFIT")],
                        [sg.Text("Stop Loss")],
                        [sg.InputText(key="STOP_LOSS")],
                        [sg.Button("Buy/Long", button_color="green"), sg.Button("Sell/Short", button_color="red")],
                        [sg.Text(e)]
                    ]

                    print(e)

                    self.window = sg.Window("Copy-Trade",
                                            layout,
                                            background_color="gray")



                time.sleep(1)


            if self.event == "LISTENING":

                self.window.close()

                listening_ticker = self.values["ticker"]

                layout = [
                        [sg.Text(self.values["source"], key="source")],
                          [sg.Text(listening_ticker,key="ticker")],
                          [sg.Button("LISTENING ON", button_color="green", key="LISTENING")],
                          [sg.Button("CLOSE TICKER POSITIONS", button_color="purple"),
                           sg.Button("CANCEL TICKER ORDERS", button_color="purple")],
                          [sg.Button("CLOSE ALL POSITIONS", button_color="purple")],
                          [sg.Text(f"Avbl: {self.current_balance} USDT", key="balance")],
                    [sg.Text(f"copy_balances: {self.copy_balances} USDT", key="copy_balances")]
                          ]

                self.window = sg.Window("Copy-Trade",
                                        layout,
                                        background_color="gray",finalize=True)


                self.bc_main = Binance_controller(ticker=listening_ticker + self.QUOTE_ASSET,
                                                  demo=False,
                                                  source=self.source,
                                                  leverage=self.leverage,
                                                  API_KEY=self.ctb_API_KEYS["main_API"],
                                                  SECRET_KEY=self.ctb_API_KEYS["main_SECRET"])

                positions = self.bc_main.get_positions()

                self.current_balance = self.bc_main.get_balance(positions=positions,
                                                                quote_asset=self.QUOTE_ASSET)

                # self.values["balance"] = self.current_balance
                self.window["balance"].update(self.current_balance)

                self.bc_copy = []

                self.copy_balances = []

                self.archived_orders = self.bc_main.get_current_orders(ticker=self.values["ticker"] + self.QUOTE_ASSET,
                                                                  status="all")

                for ak_sk in self.ctb_API_KEYS["copy"]:

                    bc_c = Binance_controller(ticker=listening_ticker + self.QUOTE_ASSET,
                                              demo=False,
                                              source=self.source,
                                              leverage=self.leverage,
                                              API_KEY=ak_sk["API"],
                                              SECRET_KEY=ak_sk["SECRET"])

                    self.bc_copy.append(bc_c)

                    positions = bc_c.get_positions()

                    copy_balance = bc_c.get_balance(positions=positions,
                                                    quote_asset=self.QUOTE_ASSET)

                    self.copy_balances.append(copy_balance)

                listening_loop = 0

                while True:

                    self.event, self.values = self.window.Read(timeout=1000)


                    self.new_archived_orders = self.bc_main.get_current_orders(ticker=listening_ticker + self.QUOTE_ASSET, status="all")



                    if self.event in ["CLOSE TICKER POSITIONS", "CANCEL TICKER ORDERS", "CLOSE TICKER POSITIONS", "CLOSE ALL POSITIONS"]:
                        self.positions_orders_closing(event=self.event,
                                                      ticker_with_quote_asset=listening_ticker + self.QUOTE_ASSET)

                        self.new_archived_orders = self.bc_main.get_current_orders(ticker=listening_ticker + self.QUOTE_ASSET, status="all")

                        self.archived_orders = self.new_archived_orders




                    print(Fore.WHITE + "self.values inside listening loop = ", self.values)


                    print(Fore.WHITE + "update... ", listening_loop_start_time - self.current_time)

                    open_orders = self.bc_main.get_current_orders(ticker=listening_ticker + self.QUOTE_ASSET,
                                                                  status="open")


                    print(Fore.WHITE + "open_orders = ", open_orders)

                    print("\n")
                    print("\n")

                    open_orders_oids = []

                    for o in open_orders:
                        oid = o["orderId"]
                        open_orders_oids.append(oid)

                    if open_orders != []:

                        print(Fore.WHITE + "open_orders != []")

                        for o in open_orders:

                            if o["orderId"] not in self.ignore_orders_oids:

                                if listening_loop > 0:

                                    print(Fore.WHITE + "o = ", o)
                                    print(Fore.WHITE + "self.current_balance = ", self.current_balance)
                                    print(Fore.WHITE + "float(o['price']) = ", float(o['price']))
                                    print(Fore.WHITE + "float(o['origQty']) = ", float(o['origQty']))
                                    print(Fore.WHITE + "self.leverage = ", self.leverage)

                                    position_volume_percent_restored = float(o["price"]) * float(o["origQty"]) / float(0.01 * self.current_balance * self.leverage)

                                    print(Fore.WHITE + "position_volume_percent_restored = ", position_volume_percent_restored)

                                    for bcc in self.bc_copy:

                                        """
                                        open Limit orders price is "price"
                                        Limits done
                                        """

                                        target_copy_balance = self.copy_balances[self.bc_copy.index(bcc)]

                                        # print(Fore.WHITE + "target_copy_balance = ", target_copy_balance)

                                        target_copy_used_balance = position_volume_percent_restored*0.01*target_copy_balance

                                        # print(Fore.WHITE + "target_copy_used_balance = ", target_copy_used_balance)

                                        copy_units = target_copy_used_balance / (float(o["price"])/self.leverage)

                                        print(Fore.WHITE + "copy_units = ", copy_units)


                                        if o["type"] in ["STOP", "STOP_LOSS_LIMIT"]:

                                            bcc.set_stop_limit_order(ticker=listening_ticker + self.QUOTE_ASSET,
                                                                    px=o["price"],
                                                                    stop_price=o["stopPrice"],
                                                                    units=copy_units,
                                                                    direction=[1 if o["side"] == "BUY" else -1][0])

                                        else:
                                            orderId, ClientOrderId, order_sent = bcc.set_order(px=o["price"],
                                                                                               direction=[1 if o["side"] == "BUY" else -1][0],
                                                                                               ticker=listening_ticker + self.QUOTE_ASSET,
                                                                                               units=copy_units)



                                else:
                                    self.ignore_orders_oids.append(o["orderId"])


                                self.ignore_orders_oids.append(o["orderId"])


                    if self.new_archived_orders != self.archived_orders:

                        print(Fore.YELLOW + "new_archived_orders != self.archived_orders")

                        print(Fore.LIGHTWHITE_EX + "new_archived_orders = ", self.new_archived_orders)
                        print(Fore.WHITE + "archived_orders = ", self.archived_orders)

                        for o in self.new_archived_orders:

                            if (o not in self.archived_orders) and (o["orderId"] not in open_orders_oids) and (o["status"] == "FILLED") and (o["orderId"] not in self.ignore_orders_oids):

                                if listening_loop > 0:

                                    print(Fore.LIGHTYELLOW_EX + "o is not in orders! = ", o)
                                    print(Fore.WHITE + "dublicating it to other accounts...")

                                    position_volume_percent_restored = (float(o["avgPrice"]) * float(o["origQty"])) / float(
                                        self.current_balance * self.leverage * 0.01)

                                    print(Fore.WHITE + "position_volume_percent_restored = ", position_volume_percent_restored)

                                    for bcc in self.bc_copy:
                                        px = [o["price"] if o["type"] != "MARKET" else o["avgPrice"]][0]

                                        copy_units = ((float(position_volume_percent_restored) * 0.01 * self.copy_balances[
                                            self.bc_copy.index(bcc)]) * self.leverage) / float(px)

                                        if o["type"] == "MARKET":
                                            px = "market"

                                        """
                                        filled orders have "avgPrice" for px
                                        """

                                        print(Fore.WHITE + "copy_units = ", copy_units)




                                        if o["type"] in ["STOP", "STOP_LOSS_LIMIT"]:

                                            bcc.set_stop_limit_order(ticker=listening_ticker + self.QUOTE_ASSET,
                                                                    px=o["price"],
                                                                    stop_price=o["stopPrice"],
                                                                    units=copy_units,
                                                                    direction=[1 if o["side"] == "BUY" else -1][0])

                                        else:
                                            orderId, ClientOrderId, order_sent = bcc.set_order(px=px,
                                                                                               direction=[1 if o["side"] == "BUY" else -1][0],
                                                                                               ticker=listening_ticker + self.QUOTE_ASSET,
                                                                                               units=copy_units
                                                                                               )



                                    self.ignore_orders_oids.append(o["orderId"])

                                else:
                                    self.ignore_orders_oids.append(o["orderId"])



                    if self.event == "LISTENING":

                        self.window.close()

                        layout = [
                            [sg.Combo(['USD-M FUTURES', "SPOT"], default_value="USD-M FUTURES", auto_size_text=True,
                                      size=20, key="source")],
                            [sg.Combo(self.FUTURES_TICKERS, default_value=listening_ticker, auto_size_text=True, key="ticker")],
                            [sg.Button("LISTENING OFF", button_color="gray", key="LISTENING")],
                            # [sg.Checkbox("LISTENING", default=False, key="LISTENING")],
                            [sg.Button("CLOSE TICKER POSITIONS", button_color="purple"),
                             sg.Button("CANCEL TICKER ORDERS", button_color="purple")],
                            [sg.Button("CLOSE ALL POSITIONS", button_color="purple")],
                            [sg.Text(f"Avbl: {self.current_balance} USDT", key="balance")],
                            [sg.Text(f"copy_balances: {self.copy_balances} USDT", key="copy_balances")],
                            # [sg.Button("Limit/Market"), sg.Button("Stop Limit")],
                            [sg.Text("Limit Price")],
                            [sg.InputText(key="px")],
                            [sg.Text("Size %:")],
                            [sg.InputText(key="position_volume_percent")],
                            [sg.Text("Take Profit")],
                            [sg.InputText(key="TAKE_PROFIT")],
                            [sg.Text("Stop Loss")],
                            [sg.InputText(key="STOP_LOSS")],
                            # [sg.Checkbox('Reduce-Only', default=False)],
                            [sg.Button("Buy/Long", button_color="green"), sg.Button("Sell/Short", button_color="red")],
                        ]

                        self.window = sg.Window("Copy-Trade",
                                                layout,
                                                background_color="gray")



                        break


                    # self.ticker = self.values["ticker"]

                    listening_loop += 1


    def positions_orders_closing(self,event,ticker_with_quote_asset):

        orders_sent = []

        if event == "CLOSE TICKER POSITIONS":

            positions = self.bc_main.get_positions()

            positions_temp = self.bc_main.get_positions()

            for t in positions_temp:
                if t != ticker_with_quote_asset:
                    positions.pop(t)

            print(Fore.YELLOW + "positions to be closed = ", positions)

            orders_sent = self.bc_main.close_positions(positions)

            for bcc in self.bc_copy:

                copy_positions = bcc.get_positions()

                copy_positions_temp = bcc.get_positions()


                for t in copy_positions_temp:


                    if t != ticker_with_quote_asset:

                        print(Fore.YELLOW + f"t {t} != ticker_with_quote_asset...")

                        copy_positions.pop(t)

                print(Fore.YELLOW + "copy_positions to be closed = ", copy_positions)

                bcc.close_positions(copy_positions)


        if event == "CANCEL TICKER ORDERS":

            open_ticker_orders = self.bc_main.get_current_orders(ticker=ticker_with_quote_asset,
                                                                 status="open")

            print(Fore.YELLOW + "open_ticker_orders to be canceled = ", open_ticker_orders)

            for o in open_ticker_orders:

                orders_sent = self.bc_main.cancel_order(ticker=ticker_with_quote_asset,
                                          orderId=o["orderId"],
                                          ClientOrderId=o["clientOrderId"])



            for bcc in self.bc_copy:

                copy_open_ticker_orders = bcc.get_current_orders(ticker=ticker_with_quote_asset,
                                                                 status="open")

                print(Fore.YELLOW + "copy_open_ticker_orders to be canceled = ", copy_open_ticker_orders)


                for o in copy_open_ticker_orders:
                    bcc.cancel_order(ticker=ticker_with_quote_asset,
                                     orderId=o["orderId"],
                                     ClientOrderId=o["clientOrderId"])



        if event == "CLOSE ALL POSITIONS":

            positions = self.bc_main.get_positions()

            print(Fore.YELLOW + "positions to be closed = ", positions)

            orders_sent = self.bc_main.close_positions(positions)

            for bcc in self.bc_copy:

                copy_positions = bcc.get_positions()

                print(Fore.YELLOW + "copy_positions to be closed = ", copy_positions)

                bcc.close_positions(copy_positions)

        return orders_sent


    def long_function_wrapper(self,work_id, window):
        print("RUNNING THREAD")
        time.sleep(5)
        window.write_event_value('-THREAD DONE-', work_id)
        return


def get_file_path(initial_file_path: str) -> str:
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, initial_file_path)

    return initial_file_path







if __name__ == "__main__":

    ctb = CopyTradeBot()

    ctb.init_interface()

































