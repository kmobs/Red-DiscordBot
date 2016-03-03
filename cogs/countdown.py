import discord
from discord.ext import commands
from .utils import checks
import os
import time
import datetime
import asyncio

class Countdown:
    """Countdown

    Countdown for Vive"""

    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def Countdown(self):
        """Countdown until Vive release"""

        vivedate = datetime.datetime(2016, 4, 5)    
        now = datetime.datetime.now()
        delta_time = vivedate - now

        return await self.bot.say(delta_time)

def setup(bot):
    n = Countdown(bot)
    bot.add_cog(n)
