import discord
from discord.ext import commands
import os
import sys

class RestartBot:

    def __init__(self, bot):
        self.bot = bot
        #Reserved for further ... stuff

    """Commands section"""
    @commands.command(no_pm=True)
    async def restart(self, *text):
        os.system("sleep 1 && python red.py")
        sys.exit(0)

    @commands.command(no_pm=True)
    async def sync(self, *text):
        os.system("git pull")
        os.system("pip3 install --upgrade git+https://github.com/Rapptz/discord.py@async")

def setup(bot):
    bot.add_cog(RestartBot(bot))
