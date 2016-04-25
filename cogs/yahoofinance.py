import discord
from discord.ext import commands
from random import randint
import aiohttp
import random
import urllib.parse

class YahooFinance:
    """Image related commands."""

    URL = "https://query.yahooapis.com/v1/public/yql?q=%s&env=http%%3A%%2F%%2Fdatatables.org%%2Falltables.env&format=json"
    QUERY = """select * from yahoo.finance.quotes where symbol in ("%s")"""

    def __init__(self, bot):
        self.bot = bot
        #Reserved for further ... stuff

    def __build_url(self, symbols):
        """ 
            Simple URL builder
        """
        derp = ",".join(symbols)
        query = self.QUERY % derp
        query = urllib.parse.quote_plus(query)
        return self.URL % query

    def __get_quote_list(self, *text):
        pass
       

    """Commands section"""
    @commands.command(no_pm=True)
    async def quote(self, *text):
        """
            This will give back a small quote for a given stock symbol
        """
        response = "[ %s | %s | %s ]"
        result = None
        async with aiohttp.get(self.__build_url(text)) as r:
            result = await r.json()

        quotes = []
        count = int(result["query"]["count"])
        if count > 1:
            quotes = result["query"]["results"]["quote"]
        else:
            quotes.append(result["query"]["results"]["quote"])

        for quote in quotes:
            exchange = quote["StockExchange"]
            if exchange is None:
                await self.bot.say("Invalid stock symbol '%s'" % text)
                return
            pchange = quote["PercentChange"]
            if pchange[0] == "+":
                pchange = ":arrow_up: " + pchange
            else:
                pchange = ":arrow_down: " + pchange
            name = quote["Name"]
            last_trade = quote["LastTradePriceOnly"]
            symbol = quote["Symbol"]
            await self.bot.say(response % (symbol,pchange,last_trade))

        
    @commands.command(no_pm=True)
    async def summary(self, *text):
        """
            This will give back a larger summary of data for a specific quote
        """
        response = "Name: %s\nPercent Change: %s\nLast Trade Price: $%s\nAsk: $%s\nBid: $%s\nDay's low: $%s\nDay's high: $%s\nPrevious close: $%s\nOpen: $%s\n50-day SMA: $%s\n200-day SMA: $%s\nStock exchange: %s\nDividend yield: %s%%\nExpected dividend pay date: %s\n"
        result = None
        async with aiohttp.get(self.__build_url(text)) as r:
            result = await r.json()

        quotes = []
        count = int(result["query"]["count"])
        if count > 1:
            quotes = result["query"]["results"]["quote"]
        else:
            quotes.append(result["query"]["results"]["quote"])

        for quote in quotes:
            exchange = quote["StockExchange"]
            if exchange is None:
                await self.bot.say("Invalid stock symbol '%s'" % text)
                return
            pchange = quote["PercentChange"]
            if pchange[0] == "+":
                pchange = ":arrow_up: " + pchange
            else:
                pchange = ":arrow_down: " + pchange
            name = quote["Name"]
            ask = quote["Ask"]
            bid = quote["Bid"]
            daylow = quote["DaysLow"]
            dayhigh = quote["DaysHigh"]
            prevclose = quote["PreviousClose"]
            open = quote["Open"]
            fdsma = quote["FiftydayMovingAverage"]
            thdsma = quote["TwoHundreddayMovingAverage"]
            dyield = quote["DividendYield"]
            ddate = quote["ExDividendDate"]
            last_trade = quote["LastTradePriceOnly"]
            await self.bot.say(response % (name,pchange,last_trade,ask,bid,daylow,dayhigh,prevclose,open,fdsma,thdsma,exchange,dyield,ddate))

def setup(bot):
    bot.add_cog(YahooFinance(bot))
