import discord
from discord.ext import commands
from .utils.chat_formatting import *
from random import randint
from random import choice as randchoice
import datetime
import time
import aiohttp
import asyncio

settings = {"POLL_DURATION" : 60}

class General:
    """General commands."""

    def __init__(self, bot):
        self.bot = bot
        self.stopwatches = {}
        self.ball = ["Hell yes","Eh, sure","Sure why not","Yes!!!","Yes","Yeah","Probably",
                     "I'm just a lowly bot, I wouldn't know","Hey why don't you ask thisisnotabot","Beats me",
                     "Nah","No","No!!!","Are you serious? No way","Um...how about no","Eh probably not","Nooooooo"]
        self.userlist = ["deadname","peyrin","painty-can","beans","bias","Esteban De La Sexface","BMC","boxelder","Dark Homer","DoctorMcGann","Dobbie","Egg","hops","hamm","hutz","inmate","insomnia","justin","kaos","kupomog","LTTR","Matty","moose","OldSchoolerMicRuler","Nicky","paddlin","parklife","RobynS","Ryan","handsome","Shaunbadia","sir hops","SmilingPolitely","The Great Remin","scully apologist","tormented","Torrens","Tromboon","Telso","jay","Judge Fudge","comeau","AlphaOmega","c l o n e","SVT","Yossarian"]
        self.poll_sessions = []

    @commands.command(hidden=True)
    async def ping(self):
        """Pong."""
        await self.bot.say("Pong.")

    @commands.command(hidden=True)
    async def pong(self):
        """Ping."""
        await self.bot.say("Ping.")

    @commands.command()
    async def choose(self, *choices):
        """Chooses between multiple choices.

        To denote multiple choices, you should use double quotes.
        """
        choices = [escape_mass_mentions(choice) for choice in choices]
        if len(choices) < 2:
            await self.bot.say('Not enough choices to pick from.')
        else:
            await self.bot.say(randchoice(choices))

    @commands.command(pass_context=True)
    async def roll(self, ctx, number : int = 100):
        """Rolls random number (between 1 and user choice)

        Defaults to 100.
        """
        author = ctx.message.author
        if number > 1:
            n = randint(1, number)
            await self.bot.say("{} :game_die: {} :game_die:".format(author.mention, n))
        else:
            await self.bot.say("{} Maybe higher than 1? ;P".format(author.mention))

    @commands.command(pass_context=True)
    async def flip(self, ctx, user : discord.Member=None):
        """Flips a coin... or a user.

        Defaults to coin.
        """
        if user != None:
            msg = ""
            if user.id == self.bot.user.id:
                user = ctx.message.author
                msg = "Nice try. You think this is funny? How about *this* instead:\n\n"
            char = "abcdefghijklmnopqrstuvwxyz"
            tran = "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz"
            table = str.maketrans(char, tran)
            name = user.display_name.translate(table)
            char = char.upper()
            tran = "∀qƆpƎℲפHIſʞ˥WNOԀQᴚS┴∩ΛMX⅄Z"
            table = str.maketrans(char, tran)
            name = name.translate(table)
            await self.bot.say(msg + "(╯°□°）╯︵ " + name[::-1])
        else:
            await self.bot.say("*flips a coin and... " + randchoice(["HEADS!*", "TAILS!*"]))

    @commands.command(pass_context=True)
    async def rps(self, ctx, choice : str):
        """Play rock paper scissors"""
        author = ctx.message.author
        rpsbot = {"rock" : ":moyai:",
           "paper": ":page_facing_up:",
           "scissors":":scissors:"}
        choice = choice.lower()
        if choice in rpsbot.keys():
            botchoice = randchoice(list(rpsbot.keys()))
            msgs = {
                "win": " You win {}!".format(author.mention),
                "square": " We're square {}!".format(author.mention),
                "lose": " You lose {}!".format(author.mention)
            }
            if choice == botchoice:
                await self.bot.say(rpsbot[botchoice] + msgs["square"])
            elif choice == "rock" and botchoice == "paper":
                await self.bot.say(rpsbot[botchoice] + msgs["lose"])
            elif choice == "rock" and botchoice == "scissors":
                await self.bot.say(rpsbot[botchoice] + msgs["win"])
            elif choice == "paper" and botchoice == "rock":
                await self.bot.say(rpsbot[botchoice] + msgs["win"])
            elif choice == "paper" and botchoice == "scissors":
                await self.bot.say(rpsbot[botchoice] + msgs["lose"])
            elif choice == "scissors" and botchoice == "rock":
                await self.bot.say(rpsbot[botchoice] + msgs["lose"])
            elif choice == "scissors" and botchoice == "paper":
                await self.bot.say(rpsbot[botchoice] + msgs["win"])
        else:
            await self.bot.say("Choose rock, paper or scissors.")

    @commands.command(name="8", aliases=["8ball"])
    async def _8ball(self, *, question : str):
        """Ask 8 ball a question
        """
        await self.bot.say(randchoice(self.ball))

    @commands.command()
    async def whodunit(self):
        """Who did it??????????????????
        """
        await self.bot.say("It was " + randchoice(self.userlist) + "!!!!")

    @commands.command(name="fahrenheit")
    async def fahrenheit(self, *, temp : int):
        """Converts Fahrenheit temperature to Celsius
        """
        newtemp = (temp-32)*5.0/9.0
        if newtemp < 0:
            await self.bot.say(str(temp) + " degrees Fahrenheit is " + str(newtemp)[:5] + " degrees Celsius.")
        else:
            await self.bot.say(str(temp) + " degrees Fahrenheit is " + str(newtemp)[:4] + " degrees Celsius.")            

    @commands.command(name="celsius")
    async def celsius(self, *, temp : int):
        """Converts Celsius temperature to Fahrenheit
        """
        newtemp = (temp * 9.0/5.0) + 32
        await self.bot.say(str(temp) + " degrees Celsius is " + str(newtemp) + " degrees Fahrenheit.")

    @commands.command(aliases=["sw"], pass_context=True)
    async def stopwatch(self, ctx):
        """Starts/stops stopwatch"""
        author = ctx.message.author
        if not author.id in self.stopwatches:
            self.stopwatches[author.id] = int(time.perf_counter())
            await self.bot.say(author.mention + " Stopwatch started!")
        else:
            tmp = abs(self.stopwatches[author.id] - int(time.perf_counter()))
            tmp = str(datetime.timedelta(seconds=tmp))
            await self.bot.say(author.mention + " Stopwatch stopped! Time: **" + tmp + "**")
            self.stopwatches.pop(author.id, None)

    @commands.command()
    async def lmgtfy(self, *, search_terms : str):
        """Creates a lmgtfy link"""
        search_terms = escape_mass_mentions(search_terms.replace(" ", "+"))
        await self.bot.say("http://lmgtfy.com/?q={}".format(search_terms))

    @commands.command(no_pm=True, hidden=True)
    async def hug(self, user : discord.Member, intensity : int=1):
        """Because everyone likes hugs

        Up to 10 intensity levels."""
        name = user.name
        if intensity <= 0:
            msg = "(っ˘̩╭╮˘̩)っ *" + name + "*"
        elif intensity <= 3:
            msg = "(っ´▽｀)っ *" + name + "*"
        elif intensity <= 6:
            msg = "╰(*´︶`*)╯ *" + name + "*"
        elif intensity <= 9:
            msg = "(つ≧▽≦)つ *" + name + "*"
        elif intensity <= 12:
            msg = "(づ￣ ³￣)づ*" + name + "*⊂(´・ω・｀⊂)"
        elif intensity >= 15:
            msg = "(づ♡ 3♡)づ*" + name + "*⊂('^▽^´⊂)"
        await self.bot.say(msg)

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    async def sue(self, ctx, user : discord.Member):
        """Take a user to court."""
        if user.id == self.bot.user.id:
                user = ctx.message.author
                await self.bot.say("Nice try. You think this is funny? How about let's sue {}, huh?".format(user.mention))
        else:
            await self.bot.say("{} has been sued".format(user.mention))

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    async def slap(self, ctx, user : discord.Member):
        """Slaps a user."""
        if user.id == self.bot.user.id:
                user = ctx.message.author
                await self.bot.say("Nice try. You think this is funny? *POW!* *slaps {}*".format(user.mention))
        else:
            await self.bot.say("*POW!* {} has been slapped".format(user.mention))

    @commands.command(pass_context=True, no_pm=True)
    async def userinfo(self, ctx, user: discord.Member=None):
        """Shows users's informations"""
        author = ctx.message.author
        server = ctx.message.server

        if not user:
            user = author

        roles = [x.name for x in user.roles if x.name != "@everyone"]

        joined_at = self.fetch_joined_at(user, server)
        since_created = (ctx.message.timestamp - user.created_at).days
        since_joined = (ctx.message.timestamp - joined_at).days
        user_joined = joined_at.strftime("%d %b %Y %H:%M")
        user_created = user.created_at.strftime("%d %b %Y %H:%M")

        created_on = "{}\n({} days ago)".format(user_created, since_created)
        joined_on = "{}\n({} days ago)".format(user_joined, since_joined)

        game = "Chilling in {} status".format(user.status)

        if user.game is None:
            pass
        elif user.game.url is None:
            game = "Playing {}".format(user.game)
        else:
            game = "Streaming: [{}]({})".format(user.game, user.game.url)

        if roles:
            roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                       if x.name != "@everyone"].index)
            roles = ", ".join(roles)
        else:
            roles = "None"

        data = discord.Embed(description=game, colour=user.colour)
        data.add_field(name="Joined Discord on", value=created_on)
        data.add_field(name="Joined this server on", value=joined_on)
        data.add_field(name="Roles", value=roles, inline=False)
        data.set_footer(text="User ID: " + user.id)

        if user.avatar_url:
            name = str(user)
            name = " ~ ".join((name, user.nick)) if user.nick else name
            data.set_author(name=name, url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
        else:
            data.set_author(name=user.name)

        try:
            await self.bot.say(embed=data)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def serverinfo(self, ctx):
        """Shows server's informations"""
        server = ctx.message.server
        online = len([m.status for m in server.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len(server.channels) - text_channels
        passed = (ctx.message.timestamp - server.created_at).days
        created_at = ("Since {}. That's over {} days ago!"
                      "".format(server.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        colour = ''.join([randchoice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        data = discord.Embed(
            description=created_at,
            colour=discord.Colour(value=colour))
        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Users", value="{}/{}".format(online, total_users))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Roles", value=len(server.roles))
        data.add_field(name="Owner", value=str(server.owner))
        data.set_footer(text="Server ID: " + server.id)

        if server.icon_url:
            data.set_author(name=server.name, url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        else:
            data.set_author(name=server.name)

        try:
            await self.bot.say(embed=data)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command()
    async def urban(self, *, search_terms : str, definition_number : int=1):
        """Urban Dictionary search

        Definition number must be between 1 and 10"""
        # definition_number is just there to show up in the help
        # all this mess is to avoid forcing double quotes on the user
        #search_terms = search_terms.split(" ")
        #try:
            #if len(search_terms) > 1:
                #pos = int(search_terms[-1]) - 1
                #search_terms = search_terms[:-1]
            #else:
                #pos = 0
            #if pos not in range(0, 11): # API only provides the
                #pos = 0                 # top 10 definitions
        #except ValueError:
            #pos = 0
        #search_terms = "+".join(search_terms)
        #url = "http://api.urbandictionary.com/v0/define?term=" + search_terms
        #try:
            #async with aiohttp.get(url) as r:
                #result = await r.json()
            #if result["list"]:
                #definition = result['list'][pos]['definition']
                #example = result['list'][pos]['example']
                #defs = len(result['list'])
                #msg = ("**Definition #{} out of {}:\n**{}\n\n"
                       #"**Example:\n**{}".format(pos+1, defs, definition,
                                                 #example))
                #msg = pagify(msg, ["\n"])
                #for page in msg:
                    #await self.bot.say(page)
            #else:
                #await self.bot.say("Your search terms gave no results.")
        #except IndexError:
            #await self.bot.say("There is no definition #{}".format(pos+1))
        #except:
            #await self.bot.say("Error.")
        await self.bot.say("How about...let's not.")

    @commands.command(pass_context=True, no_pm=True)
    async def poll(self, ctx, *text):
        """Starts/stops a poll

        Usage example:
        poll Is this a poll?;Yes;No;Maybe
        poll stop"""
        message = ctx.message
        if len(text) == 1:
            if text[0].lower() == "stop":
                await self.endpoll(message)
                return
        if not self.getPollByChannel(message):
            check = " ".join(text).lower()
            if "@everyone" in check or "@here" in check:
                await self.bot.say("Nice try.")
                return
            p = NewPoll(message, self)
            if p.valid:
                self.poll_sessions.append(p)
                await p.start()
            else:
                await self.bot.say("poll question;option1;option2 (...)")
        else:
            await self.bot.say("A poll is already ongoing in this channel.")

    async def endpoll(self, message):       
        if self.getPollByChannel(message):
            p = self.getPollByChannel(message)
            if p.author == message.author.id: #or isMemberAdmin(message)
                await self.getPollByChannel(message).endPoll()
            else:
                await self.bot.say("Only the author can stop the poll.")
        else:
            await self.bot.say("There's no poll ongoing in this channel.")

    def getPollByChannel(self, message):
        for poll in self.poll_sessions:
            if poll.channel == message.channel:
                return poll
        return False

    async def check_poll_votes(self, message):
        if message.author.id != self.bot.user.id:
            if self.getPollByChannel(message):
                    self.getPollByChannel(message).checkAnswer(message)

    def fetch_joined_at(self, user, server):
        """Just a special case for someone special :^)"""
        if user.id == "96130341705637888" and server.id == "133049272517001216":
            return datetime.datetime(2016, 1, 10, 6, 8, 4, 443000)
        else:
            return user.joined_at

class NewPoll():
    def __init__(self, message, main):
        self.channel = message.channel
        self.author = message.author.id
        self.client = main.bot
        self.poll_sessions = main.poll_sessions
        msg = message.content[6:]
        msg = msg.split(";")
        if len(msg) < 2: # Needs at least one question and 2 choices
            self.valid = False
            return None
        else:
            self.valid = True
        self.already_voted = []
        self.question = msg[0]
        msg.remove(self.question)
        self.answers = {}
        i = 1
        for answer in msg: # {id : {answer, votes}}
            self.answers[i] = {"ANSWER" : answer, "VOTES" : 0}
            i += 1

    async def start(self):
        msg = "**POLL STARTED!**\n\n{}\n\n".format(self.question)
        for id, data in self.answers.items():
            msg += "{}. *{}*\n".format(id, data["ANSWER"])
        msg += "\nType the number to vote!"
        await self.client.send_message(self.channel, msg)
        await asyncio.sleep(settings["POLL_DURATION"])
        if self.valid:
            await self.endPoll()

    async def endPoll(self):
        self.valid = False
        msg = "**POLL ENDED!**\n\n{}\n\n".format(self.question)
        for data in self.answers.values():
            msg += "*{}* - {} votes\n".format(data["ANSWER"], str(data["VOTES"]))
        await self.client.send_message(self.channel, msg)
        self.poll_sessions.remove(self)

    def checkAnswer(self, message):
        try:
            i = int(message.content)
            if i in self.answers.keys():
                if message.author.id not in self.already_voted:
                    data = self.answers[i]
                    data["VOTES"] += 1
                    self.answers[i] = data
                    self.already_voted.append(message.author.id)
        except ValueError:
            pass

def setup(bot):
    n = General(bot)
    bot.add_listener(n.check_poll_votes, "on_message")
    bot.add_cog(n)
