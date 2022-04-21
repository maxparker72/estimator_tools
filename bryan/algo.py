'''
    General Comments: 
        Since each ticker requires its own code block for evaluation, I think it would be best to consolidate them into a data structure
        that can be loaded in via a json configuration file. Its easy to write a json file and ammend additional parameters. If you have
        different control structures for each ticker then we need to take a different approach. If you simply wish to write custom code
        for each ticker, then we can look into creating multiple python files. This is not hard but is not as concise as using a config
        file. It all depends on the flexibility you want to have and the intent you have with each of your equities. Give me some
        feedback on my comments and code and let me know if I am working on the right thing here. 

        In addition, I have not setup quant-connect myself so this will be challenging for me to test independently. I'm hoping it
        doesn't get that complicated and I can just simplify the python using knowledge of the language and what you are trying to 
        acheive. 

        Use Ctrl+F and search for "MP" to find all my comments. 
'''

# region imports
from AlgorithmImports import *

# endregion
from clr import AddReference
AddReference("System")
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Common")

# MP - other quant connect imports
from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *

# MP - python imports
import time
import json

# MP - I see this class is required to be implemented by Quantconnect
class NadionResistanceFlange(QCAlgorithm):

    def Initialize(self):
        # MP - Set time zone for this algorithm
        self.SetTimeZone("America/Los_Angeles")

        # MP - Instance variables for this algorithm
        self.tickets = [] # MP - Empty list
        self.second = -1 # MP - Default value
        trades = 0 # MP - Default value
        
        # MP - All tickers initialized are assumed to use the following parameters: Resolution second, Market USA, True, 2, False
        # MP - Ticker dictionary will use unique tickers as keys and parameter dictionaries as parameters. 
        with open('tickers.json', 'r') as file:
            # load json file as ticker dictionary instance variable.
            self.tkr_dic = json.load(file)

        # MP - Initialize each equity to the instance algorithm
        # MP - Add each equity object to a new equity object dicionary for referencing equity objects. 
        self.tkr_objs = {}
        for tkr in self.tkr_dic.keys():
            eq = self.AddEquity(tkr, Resolution.Second, Market.USA, True, 2, False)
            self.tkr_objs[tkr] = eq
            self.Debug(f"Equity added from json configuration file: {tkr}")

    def OnData(self, data):
        # MP - If time returned is equal to default of -1 return without continuing, otherwise set the time. 
        if self.second == self.Time.second:
            return
        else:
            self.second = self.Time.second

        # MP - Clarify intent of next three lines. 
        cash = self.Portfolio.Cash # MP TODO: variable not used. This looks like an inherited instance variable. 
        allCancelledOrders = self.Transactions.CancelOpenOrders() # MP - TODO: method called, if it returns something the variable is not used.  
        trades = 0 # MP - TODO: this variable is declared in the scope of OnData only and is not associated with the trades declared in initialize.

        # MP - I assume the algorithm is the same for each equity and uses pre-defined parameters, let me know if this is not the case. 
        for tkr in self.tkr_objs.keys():
            # MP - Note,  any parameters you wish to be unique can be stored in the json for a specific ticker and loaded in. 
            cprice = self.tkr_objs[tkr].Price
            cqty = self.Portfolio[tkr].Quantity
            strt = self.tkr_dic[tkr]['strt']
            step = self.tkr_dic[tkr]['step']
            buyp = strt
            sellp = strt + step * (2 - cqty)
            bgap = cprice / buyp 
            sgap = cprice / sellp 

            if cqty == 0 and buyp >= cprice:
                btik = self.MarketOrder(tkr, 1)

            if cqty >= 1 and sgap <= self.tkr_dic[tkr]['coef_01'] and sellp <= cprice:
                stik = self.LimitOrder(tkr,-1,sellp)
                trades += 1
            elif cqty >= 1 and sgap > self.tkr_dic[tkr]['coef_01']:
                stik = self.MarketOrder(tkr,-1)

            sleeptime = trades * 3

            if sleeptime > 15:
                sleeptime = 15

        time.sleep(sleeptime)
        allCancelledOrders = self.Transactions.CancelOpenOrders()
        time.sleep(sleeptime)