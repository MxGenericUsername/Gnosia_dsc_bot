from config import config
from enum import Enum
import random
import discord
import time

from discord.ext import tasks
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(intents=intents, command_prefix="!")
global curc

global players
class prof():
    def __init__(self,name):
        self.name = name

class player():
    def __init__(self, prof, id):

        self.name = prof.name
        self.role = 0
        self.prof = prof
        self.id = id
        self.votes = 0
        self.canvote = True
        self.validforvotes = True
        self.alive = True
        self.public_role = 0
        self.engi_scans = []
        self.engi_reveals = []
        self.doctor_scans = []
        self.doctor_reveals = []
        self.cold = False
        self.reqvotes = 0
        self.doctor_scanned = 0

players = []
a = []
i = 0


class role:
    def __init__(self, id, name, number, description, reqvotes):
        self.id = id
        self.canvote = True
        self.description = description
        self.name = name
        self.number = number
        self.totid = 0
        self.reqvotes = reqvotes



gnosia = []

roles = []
roles.append(role(0, "a Crewmate", 0, "You're just a normal crewmate, no special commands", 0))
roles.append(role(1, "an Engineer", 1, "special commands: !engireveal, !engiscan player_id gnosia/human (if faking, optional)", 1))
roles.append(role(2, "Guard Duty", 0, "!guardreveal", 0))
roles.append(role(3, "a Guardian Angel", 0, "special commands: !guard player_id", 1))
roles.append(role(4, "a Gnosia", 1, "special commands: every special command except for guard", 3))
roles.append(role(5, " an AC Follower", 0, "special commands: every special command except for guard and nighttime vote", 2))
roles.append(role(6, "A Bug", 1, "pecial commands: every special command except for guard and nighttime vote", 2))
roles.append(role(7, "A Doctor", 1, "special commands: !claim doctor, !docscan player_id gnosia/human (if faking, optional)", 1))

class phase(Enum):
    day = 0
    voting = 1
    night = 2
    freeze_all_vote = 3
    end = 4

class game_data():
    test = True
    role_amount = 0
    voting_time = 300

    curp = 2
    votes = 0
    players = 0
    gnosia = 0
    voting_phase = 0
    voted_out = []
    oldvictims = []
    info_channel = ""
    victimids = []
    engi_claimants = []
    doctor_claimants = []
    guard_duty_claimants = []
    last_msg = ""
    day = 0
    message = ""
    reqvotes = 0
    votesinprogress = 0
    warning = False
    freeze_all = 0
    vote_timer_start = 0
    bug_id = -1
    game = False
    protected_id = -1
    bug_squished = False
    guard_duty_ids = []
    gnosia_names = ""
    block = False
    engi_scans = 0
    doctor_scans = 0
    frozen_amount = 0



gd = game_data()
for role in roles:
    gd.role_amount += role.number


if(gd.test == True):
    while i < 6:
        a.append(prof(str(i+1)))
        players.append(player(a[i], i+1))
        i += 1


@tasks.loop(seconds=5.0)
async def voting_timer():
    global players
    global gd

    k = time.time() - gd.vote_timer_start
    print(k)
    if (gd.voting_time - time.time() + gd.vote_timer_start <= 60 and gd.warning != True):
        await gd.info_channel.send("https://tenor.com/view/zero-escape-zero-time-dilemma-zero-time-time-to-decide-decision-game-gif-17564467")
        await gd.info_channel.send("You have ~1 minute left")

        gd.warning = True
    if (k >= gd.voting_time):
        if (gd.curp == 0 and gd.block == False):
            gd.block = True
            await gd.info_channel.send("Voting time has ran out")
            await count_votes()
        elif (gd.curp == 2 and gd.block == False):
            gd.block = True
            await gd.info_channel.send("Nighttime ended")
            if (gd.day != 0):
                gd.block = True
                await count_votes()
            else:
                await progress_to_day()
        elif (gd.curp == 3):
            await count_votes()


async def start_the_game(chan):
    global players
    global gd
    n = 0
    i = 0
    if (gd.test == False):
        while i < len(chan.members):
            if (chan.members[i].bot == False):
                players.append(player(chan.members[i], n))
                await players[i].prof.send("you should recieve this message")

                print(type(players[0]))
                n += 1
            i += 1
    await gd.info_channel.send("counted the players")
    gd.players = len(players)
    print(players)

    if (gd.players >= gd.role_amount):
        i = 0
        while i < len(roles):
            while (n < roles[i].number):
                k = random.randint(0, len(players) - 1)
                if (players[k].role == 0):

                    if (i == 4):
                        gd.gnosia_names += str(players[k].name) + " \n "
                        gd.gnosia += 1
                    elif (i == 2):
                        gd.guard_duty_ids.append(k)
                    elif (i == 6):
                        gd.bug_id = k

                    players[k].role = i
                    print(players[k].role)
                    players[k].reqvotes = roles[i].reqvotes

                    n += 1

            i += 1
            n = 0
        i = 0

        print(len(players))
        print(i)
        if (gd.test == False):
            while i < len(players):
                await players[i].prof.send("good luck, you're {0} \n ".format(roles[players[i].role].name))
                await players[i].prof.send(str(roles[players[i].role].description))

                if (players[i].role == 4):
                    await players[i].prof.send("this game's gnosia are " + str(gd.gnosia_names))
                gd.last_msg += players[i].name + " id:" + str(i + 1) + "  \n"
                i += 1

            await gd.info_channel.send(gd.last_msg)
            gd.last_msg = ""
            i = 0

        else:

            while i < len(players):
                gd.last_msg += "id:" + str(i + 1) + "role:" + str(roles[players[i].role].name) + "  \n"

                i += 1
            await gd.info_channel.send(gd.last_msg)
        gd.last_msg = ""

        gd.game = True
        gd.curp = 2
        gd.reqvotes = gd.gnosia + 2
        i = 0

        await gd.info_channel.send("started the game. \n Check you dms to see what your role is \n We'll start with a nighttime round of engi scans to shake things up")
        gd.vote_timer_start = time.time()


    else:
        await gd.info_channel.send("Too few players for the amount of selected roles")
        gd.game = 0
        i = 0



async def progress_to_day():
    global players
    global gd
    gd.protected_id = -1
    gd.votes = 0
    gd.day += 1
    if (gd.bug_squished):
        players[gd.bug_id].alive = False

        gd.bug_squished = False
        gd.last_msg += ", " + players[gd.bug_id].name +"  "


    if(gd.last_msg != ""):
        await gd.info_channel.send(".\n Day {0} \n Last night {1} disappeared ".format(gd.day, gd.last_msg))
    else: await gd.info_channel.send(".\n Day {0} \n Last night noone disappeared ".format(gd.day))

    gd.reqvotes = 0
    gd.players = 0
    gd.last_msg = " "

    for player in players:
        player.votes = 0

        player.canvote = False
        if(1 << player.role & 114 != 0 and len(player.engi_scans) < gd.day):
            player.engi_scans.append(str(gd.day))
            player.engi_reveals.append("didn't scan")
        if(1< player.role & 240 != 0 and len(player.engi_reveals) < gd.day - 1):
            player.doctor_scans.append(" ")
            player.doctor_reveals.append("didn't scan")


        if (len(player.engi_scans) != 0 and player.public_role == 1):
            gd.last_msg = ""
            i = 0
            while (i < len(player.engi_scans)):

                gd.last_msg+="\n " + str(player.engi_scans[i]) + "   " + str(player.engi_reveals[i])
                i += 1
            await gd.info_channel.send("Engineer {0.name}'s scans: ".format(player) + gd.last_msg)
            gd.last_msg = ""
        elif (len(player.doctor_scans) != 0 and player.public_role == 7):
            gd.last_msg = ""
            i = 0

            while (i < len(player.doctor_scans)):
                gd.last_msg +="\n " + str(player.doctor_scans[i]) + "   " + str(player.doctor_reveals[i])
                i += 1

            await gd.info_channel.send(" Doctor {0.name}'s scans: ".format(player) + gd.last_msg)
            gd.last_msg = ""
        if (player.alive == True):
            gd.players += 1
            gd.reqvotes += 1
            player.validforvotes = True
            player.canvote = True

    i = 0
    while i < len(players):
        if (players[i].alive):
            gd.last_msg +=players[i].name + "'s " +  "id: " + str(i+1) + "  \n"

        i += 1
    await gd.info_channel.send(gd.last_msg)
    gd.last_msg = ""




    print("gd.gnosia")
    print(gd.gnosia)
    print("gd.platers")
    print(gd.players)

    if (gd.players - gd.gnosia <= gd.gnosia):
        gd.curp = 4
        if (gd.bug_id != -1):
            if (players[gd.bug_id].alive == True):
                await gd.info_channel.send("The bug wins! Congratulations to {0.name}.  The gnosia were: {1.gnosia_names}".format(players[gd.bug_id],gd))
            else:
                await gd.info_channel.send("The gnosia win! The gnosia were: {0.gnosia_names}, the bug was {1.name}".format(gd, players[gd.bug_id]))




        else:
            await gd.info_channel.send("The gnosia win! The gnosia were: {0.gnosia_names}".format(gd))


    gd.curp = 0
    gd.votes = 0
    gd.vote_timer_start = time.time()
    gd.voting_time = 300
    gd.block = False
    gd.warning = False
    gd.last_msg = ""





async def progress_to_night():
    global players
    global gd

    gd.reqvotes = 0
    gd.gnosia = 0
    gd.protected_id = -1
    gd.players = 0

    await gd.info_channel.send(".\n Night {0}".format(gd.day))
    for player in players:
        player.votes = 0
        player.canvote = False
        if (player.alive == True):
            gd.players+=1
            gd.reqvotes += roles[player.role].reqvotes
            if (1 << player.role & 250 != 0):
                player.canvote = True
                print("player {0.name} can vote".format(player))
                if (player.role == 4):
                    player.validforvotes = False
                    gd.gnosia +=1
                if(1<<player.role & 240 !=0):
                    if(player.doctor_scanned == gd.frozen_amount):
                        gd.reqvotes -=1
                        if(player.role == 7):
                            player.canvote = False

    if (gd.players - gd.gnosia <= gd.gnosia):
        gd.curp = 4
        if (gd.bug_id != -1):
            if (players[gd.bug_id].alive == True):
                await gd.info_channel.send("The bug wins! Congratulations to {0.name}.  The gnosia were: {1.gnosia_names}".format(players[gd.bug_id],gd))
            else:
                await gd.info_channel.send("The gnosia win! The gnosia were: {0.gnosia_names}, the bug was {1.name}".format(gd, players[gd.bug_id]))
        else:
            await gd.info_channel.send("The gnosia win! The gnosia were: {0.gnosia_names}".format(gd))
    elif(gd.gnosia == 0):
        if (gd.bug_id != -1):
            if (players[gd.bug_id].alive == True):
                await gd.info_channel.send("The bug wins! Congratulations to {0.name}.  The gnosia were: {1.gnosia_names}".format(players[gd.bug_id],gd))
                gd.game = False
            else:
                await gd.info_channel.send("The humans win! The gnosia were: {0.gnosia_names}, the bug was {1.name}".format(gd, players[gd.bug_id]))
                gd.game = False
        else:
            await gd.info_channel.send("The humans win! The gnosia were: {0.gnosia_names}".format(gd))
            gd.game = False





    if gd.game:
        i = 0
        while i < len(players):
            if (players[i].alive):
                gd.last_msg += players[i].name + "'s " + "id: " + str(i+1) + "  \n"

            i += 1
        await gd.info_channel.send(gd.last_msg)
        gd.last_msg = ""
    gd.curp = 2
    gd.votes = 0
    gd.voting_time = 300
    gd.vote_timer_start = time.time()
    gd.block = False
    gd.warning = False




async def vote_resolution(victims):
    global players
    global gd

    gd.last_msg = ""


    gd.last_msg = ""
    if (len(victims) == 1):
        if(gd.curp != 3):
            if(gd.protected_id != victims[0]):

                print("got to the freezing part")
            if (gd.curp == 0):

                players[victims[0]].alive = False
                players[victims[0]].cold = True
                gd.frozen_amount+=1
                await gd.info_channel.send("The crew decided to freeze {0.name}".format(players[victims[0]]))
                await progress_to_night()

            elif (gd.curp == 2):
                if(players[victims[0]].role !=6):
                    gd.last_msg += players[victims[0]].name
                    players[victims[0]].alive = False
                await progress_to_day()
        elif(gd.curp == 3):
            if(gd.freeze_all > 0):
                for victim in gd.oldvictims:
                    players[victim].alive = False
                    players[victim].cold = True
                    gd.frozen_amount += 1
                    gd.last_msg += players[victim].name
                await gd.info_channel.send("Vote successful, the crew decided to freeze all of the suspects")
            else:
                await gd.info_channel.send("Vote successful, the crew decided not to freeze all of the suspects")
            await progress_to_night()
            return 0
        return 0


    elif(players[victims[0]].votes == 0):
        await gd.info_channel.send("Vote unsuccessful, nobody voted")
        if(gd.curp == 0):
            await progress_to_night()
        else:
            await progress_to_day()

    else:
        if (gd.curp == 0 ):

            if(victims != gd.oldvictims):
                gd.last_msg += "Vote unsuccesful \n Players passing to the next round of voting are: \n"
                gd.votes = 0
                a = players[victims[0]].votes
                for player in players:
                    if(player.alive):
                        player.canvote = True
                        player.validforvotes = False
                        if (player.votes == a):
                            player.validforvotes = True
                            gd.last_msg += player.name + " id: " + str(player.id +1) + " \n "
                        player.votes = 0

                gd.oldvictims = victims

                await gd.info_channel.send(gd.last_msg)
                gd.last_msg = ""
                gd.vote_timer_start = time.time()
                gd.voting_time = 120
            else:
                gd.curp = 3
                for player in players:
                    if(player.alive == True):
                        player.canvote = True
                        print("player can vote")
                        if (victims.__contains__(player.id)):
                            player.canvote = False
                gd.reqvotes-=len(victims)
                await gd.info_channel.send("The crew couldn't reach an agreement on who to send to cold sleep so now you're deciding between freezing everyone, or noone \n Dm me !vote 1 if you want to freeze everyone who's tied or !vote 2 if you don't want to freeze anyone")
                gd.votes = 0
                gd.vote_timer_start = time.time()
                gd.voting_time = 120
        elif (gd.curp == 2):
            k = random.randint(0, len(victims) - 1)
            if(victims[k] != gd.protected_id):
                players[victims[k]].alive = False
                gd.last_msg+= " " + players[victims[k]].name + " "
            await progress_to_day()


async def count_votes():
    global players
    global gd
    k = 0
    i = 1
    gd.last_msg = " "
    print("last msg =" + gd.last_msg)
    victims = [0]
    if(gd.curp != -3):

        if(gd.curp == 0):
            gd.last_msg += "Voting results \n" + str(players[0].name) + " " + str(players[0].votes) + " votes \n"
        while (i < len(players)):
            print(victims)
            print(players[i].votes)
            print(victims[0])
            gd.last_msg += players[i].name + " " + str(players[i].votes) + "votes \n"
            if (players[i].votes > players[victims[0]].votes):
                victims = [i]
            elif (players[i].votes == players[victims[0]].votes):
                victims.append(i)
            i += 1
        await  gd.info_channel.send(gd.last_msg)
        gd.last_msg = ""
    else:
        victims = [gd.freeze_all]

    await vote_resolution(victims)




@bot.event
async def on_ready():
    print("logged in as {0.user} ".format(bot))



@bot.command()
async def vote(ctx, *args):
    global players
    global gd
    if (gd.game == True):
        print("aaaa")
        x = -1
        i = 0
        k = len(players)
        if (gd.test == False):
            while (x == -1 and i < k):
                if (ctx.author.id == players[i].prof.id):
                    x = i
                i += 1
        else:
            x = int(args[1]) - 1


        print("voooote")
        print(x)
        print(ctx.author.id)

        if (x != -1 and players[x].canvote == True):
            votenum = int(args[0]) -1
            print(players[votenum].name)
            if (gd.curp == 0):
                if (players[votenum].validforvotes == True):
                    players[votenum].votes += 1

                    gd.votes += 1
                    players[x].canvote = False
                    print("votes " + str(gd.votes))
                    print("reqvotes" + str(gd.reqvotes))

                    await ctx.channel.send("you voted for {0}".format(players[votenum].name))
                    if (gd.votes == gd.reqvotes):
                        await count_votes()
                    return 0
            elif (gd.curp == 2 and gd.day != 0):

                if (players[votenum].validforvotes == True and players[votenum].alive == True):
                    players[votenum].votes += 1

                    gd.votes+=1
                    await ctx.channel.send("you voted for {0}".format(players[votenum].name))
                    players[x].canvote = False
                    print("votes " + str(gd.votes))
                    print("reqvotes" + str(gd.reqvotes))
                    if (gd.votes == gd.reqvotes):
                        await count_votes()
                else:
                    await ctx.channel.send("sorry, but you cannot vote for that player")
            elif (gd.curp == 3):

                if(votenum == 1):
                    gd.freeze_all += 1
                    players[x].canvote = False
                    await ctx.channel.send("You decided to freeze everyone")
                elif (votenum == 2):
                    gd.freeze_all -= 1
                    players[x].canvote = False
                    await ctx.channel.send("You decided not to freeze everyone")
                gd.votes +=1
                print("votes " + str(gd.votes))
                print("reqvotes" + str(gd.reqvotes))
                if(gd.votes == gd.reqvotes):
                    await count_votes()


@bot.command()
async def engiscan(ctx, *args):
    global players
    global gd
    if (gd.game == True and gd.curp == 2 or gd.curp == 3):
        x = -1
        i = 0
        k = len(players)
        if (gd.test == False):
            while (x == -1 and i < k):
                if (ctx.author.id == players[i].prof.id):
                    x = i
                i += 1
        else:
            x = int(args[2])-1
        if (x != -1):
            print(players[x].role & 114)
            print(len(players[x].engi_scans))
            print(gd.day)
            if (1 << players[x].role & 114 != 0 and len(players[x].engi_scans) <= gd.day and players[x].alive):

                votenum = int(args[0])-1
                print("votenum")
                print(votenum)

                if (len(args) == 1):
                    role_discovered = " "

                else:
                    role_discovered = args[1]
                if (players[votenum].alive == True):
                    if (players[x].role == 1):
                        if (players[votenum].role == 4):
                            players[x].engi_reveals.append(" gnosia")
                        else:
                            players[x].engi_reveals.append(" human")
                            if (players[votenum].role == 6):
                                gd.bug_squished = True

                    else:

                        if (role_discovered == "gnosia"):
                            players[x].engi_reveals.append(" gnosia")

                        else:
                            players[x].engi_reveals.append(" human")
                    players[x].engi_scans.append(votenum + 1)

                    gd.votes += 1
                    print("votes " + str(gd.votes))
                    print("reqvotes" + str(gd.reqvotes))
                    await ctx.channel.send("Thank you for scanning {0.name} and revealing them to be {1}".format(players[votenum], players[x].engi_reveals[gd.day]))
                    if (gd.votes == gd.reqvotes):
                        if(gd.day != 0):
                            await count_votes()
                        else:
                            await progress_to_day()
                else:
                    await ctx.channel.send("Sorry, but that person's frozen, so scanning them is the doctor's job. Ask them to do it")





@bot.command()
async def docscan(ctx, *args):
    global players
    global gd
    if (gd.game == True and gd.curp == 2):
        x = -1
        i = 0
        k = len(players)
        if (gd.test == False):
            while (x == -1 and i < k):
                if (ctx.author.id == players[i].prof.id):
                    x = i
                i += 1
        else:
            x = int(args[2])-1
        if (x != -1):
            print(players[x].role & 240)
            print(len(players[x].doctor_scans))
            print(gd.day)

            if (1 << players[x].role & 240 != 0 and len(players[x].doctor_scans) < gd.day and players[x].alive and players[x].doctor_scanned < gd.frozen_amount):
                if (len(args) == 1):
                    role_discovered = " "

                else:
                    role_discovered = args[1]
                votenum = int(args[0])-1
                if (players[votenum].alive == False):
                    if (players[votenum].cold == True):
                        if (players[x].role == 7):
                            if (players[votenum].role == 4):
                                players[x].doctor_reveals.append(" gnosia")
                            else:
                                players[x].doctor_reveals.append(" human")
                        else:

                            if (role_discovered == "gnosia"):
                                players[x].doctor_reveals.append(" gnosia")

                            else:
                                players[x].doctor_reveals.append(" human")
                        players[x].doctor_scans.append(votenum + 1)


                        await ctx.channel.send("Thank you for scanning {0.name} and revealing them to be {1}".format(players[votenum],players[x].doctor_reveals[gd.day-1]))
                        players[x].doctor_scanned += 1
                        gd.votes +=1
                        print("votes " + str(gd.votes))
                        print("reqvotes" + str(gd.reqvotes))
                        if (gd.votes == gd.reqvotes):
                            await count_votes()


                    else:
                        await ctx.channel.send("Unfortunately this player has disappeared. I'd like to let you scan them but... I don't exactly know where they are")
                else:
                    await ctx.channel.send("Vivisections are terribly messy. Please pick someone who isn't still around, ok?")






@bot.command()
async def protect(ctx, *args):
    global players
    global gd
    if (gd.game == True and gd.curp == 2 and gd.day != 0):
        x = -1
        i = 0
        k = len(players)
        if (gd.test == False):
            while (x == -1 and i < k):
                if (ctx.author.id == players[i].prof.id):
                    x = i
                i += 1
        else:
            x = int(args[1])-1
        if (x != -1):
            if(x != int(args[0])):
                if (players[x].role == 3 and players[x].canvote == True):
                    await ctx.channel.send("You decided to protect {0.name}".format(players[int(args[0])-1]))
                    gd.protected_id = int(args[0])-1
                    gd.votes += 1
                    print("votes " + str(gd.votes))
                    print("reqvotes" + str(gd.reqvotes))
                    players[x].canvote = False
                    if (gd.votes == gd.reqvotes):
                        await count_votes()
            else:
                await ctx.channel.send("Sorry, but you can't protect yourself")



@bot.command()
async def engireveal(ctx, *args):
    if (gd.game == True and gd.curp == 0):
        x = -1
        i = 0
        k = len(players)
        if (gd.test == False):
            while (x == -1 and i < k):
                if (ctx.author.id == players[i].prof.id):
                    x = i
                i += 1
        else:
            x = int(args[0])-1
        if( x != -1):
            if (1 << players[x].role & 114 != 0 and players[x].public_role == 0):
                last_msg = " "
                print("engi scans" + str(len(players[x].engi_scans)))
                print("engi reveals" + str(len(players[x].engi_reveals)))
                await  gd.info_channel.send(str(players[x].name) + " has revealed themselves to be an engineer, here are their reports")
                i = 0
                players[x].public_role = 1
                while (i < len(players[x].engi_scans)):
                    last_msg += str(players[x].engi_scans[i]) + ":" + str(players[x].engi_reveals[i]) + " \n "


                    i += 1
                if(last_msg!=" "):
                    await gd.info_channel.send(last_msg)
                gd.last_msg = ""






@bot.command()
async def docreveal(ctx,*args):
    if (gd.game == True and gd.curp == 0):
        x = -1
        i = 0
        k = len(players)
        if (gd.test == False):
            while (x == -1 and i < k):
                if (ctx.author.id == players[i].prof.id):
                    x = i
                i += 1
        else:
            x = int(args[0])-1
        if( x != -1):
            if(1 << players[x].role & 240 != 0 and players[x].public_role == 0):
                await  gd.info_channel.send(str(players[x].name) + " has revealed themselves to be a doctor, here are their reports")
                i = 0
                players[x].public_role = 7
                last_msg = " "
                print("doc scans" + str(len(players[x].doctor_scans)))
                print("doc reveals" + str(len(players[x].doctor_reveals)))
                while (i < len(players[x].doctor_scans)):
                    last_msg += str(players[x].doctor_scans[i]) + " : " + str(players[x].doctor_reveals[i]) + " \n "

                    i += 1
                if(last_msg!= " "):
                     await gd.info_channel.send(last_msg)




@bot.command()
async def start(ctx):
    if (gd.game == False and ctx.author.id == config['host_id'] and str(type(ctx.channel))) != "<class 'discord.channel.DMChannel'>":
        gd.info_channel = ctx.channel
        chan = ""
        if(gd.test == False):
            chan = ctx.author.voice.channel

        await start_the_game(chan)
        gd.voting_time = 180
        voting_timer.start()


async def guardreveal():
    if (gd.game == True and gd.curp == 0):
        x = -1
        i = 0
        k = len(players)
        if (gd.test == False):
            while (x == -1 and i < k):
                if (ctx.author.id == players[i].prof.id):
                    x = i
                i += 1
        else:
            x = int(args[0])-1

        if(players[x].role==2 and players[x].public_role!=2):
            await gd.info_channel.send("{0.name}  has announced {1.name} and {2.name}  were on guard duty".format(players[x],gd.guard_duty_ids[0],gd.guard_duty_ids[1]))
