import discord
from discord.ext import commands
from .utils.dataIO import fileIO
import os

class Here:
    """Here

    Mention users by category"""

    def __init__(self, bot):
        self.bot = bot
        self.notifications = fileIO("data/here/here.json", "load")

    @commands.group(name="here", pass_context=True)
    async def _here(self, ctx):
        """Here notifications"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_here.command(pass_context=True, no_pm=True)
    async def register(self, ctx, game):
        """Register for a notification category"""
        user = ctx.message.author
        done = False

        for i, s in enumerate(self.notifications):
            if s["KEYWORD"] == game:
                if user.id in s["USERS"]:
                    if len(s["USERS"]) == 1:
                        self.notifications.remove(s)
                        await self.bot.say("User removed from " + game)
                        done = True
                    else:
                        self.notifications[i]["USERS"].remove(user.id)
                        await self.bot.say("User removed from " + game)
                        done = True
                else:
                    self.notifications[i]["USERS"].append(user.id)
                    await self.bot.say("User added to " + game)
                    done = True
        if not done:
            self.notifications.append(
                {"KEYWORD": game, "USERS": [user.id]})
            await self.bot.say("User added to " + game)
        fileIO("data/here/here.json", "save", self.notifications)

    @_here.command(pass_context=True, no_pm=True)
    async def lets(self, ctx, game):
        """Call all people in that group"""

        names = ""
        gname =  "It's time for " + game + " "
        for i, s in enumerate(self.notifications):
            if s["KEYWORD"] == game:
                names = ', '.join(map(lambda i: '<@{}>'.format(i), self.notifications[i]["USERS"]))
                await self.bot.say(gname + names)

    @_here.command(pass_context=True)
    async def lists(self, ctx):
        """Show existing lists"""

        lists = ""
        for i, s in enumerate(self.notifications):
            lists = lists + s["KEYWORD"] + "     "
        await self.bot.say("Existing lists are ```" + lists + "```")


def check_folders():
    if not os.path.exists("data/here"):
        print("Creating data/here folder...")
        os.makedirs("data/here")

def check_files():
    f = "data/here/here.json"
    if not fileIO(f, "check"):
        print("Creating empty here.json...")
        fileIO(f, "save", [])

def setup(bot):
    check_folders()
    check_files()
    n = Here(bot)
    bot.add_cog(n)
