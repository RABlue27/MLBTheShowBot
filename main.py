import discord
import requests
import csv
from asyncio.events import TimerHandle
from asyncio.tasks import wait_for
from discord import user
from discord import channel 
from discord.ext import commands
import json
class Investment:
    def __init__(self, id, invests):
        self.id = id
        self.invests = invests

    def print_investment(self):
        print(self.id, self.invests)

class Player:
    def __init__(self, name, change):
        self.name = name
        self.change = change
        
    def print(self):
        print("Name:", self.name, " Attribute change: ", self.change)

#TODO: Write to file to change command sign

with open("secretstuff.txt", "r") as f:
    token = f.readline()
    commandSign = f.readline()


bot = commands.Bot(command_prefix=commandSign)
client = discord.Client()
@client.event 
async def on_ready():
    print("Login success.")
    await lastupdate()
    

async def write_to_csv(investment):
    with open("investmentsheet.csv", 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        l = []
        l.append(investment.id)
        l.append(investment.invests)
        csvwriter.writerow(l)

# Check to make sure user ID isn't in the CSV
async def check_for_id(id):
    with open("investmentsheet.csv", "rt") as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            for field in row:
                if int(field) == int(id):
                    return True
    return False


# TODO: allow abortion, typo fixing
# Main juice of the program
@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    if message.content.startswith(commandSign + "lastupdate"):
        await lastupdate()
        return

    def check(m):
        return m.author == message.author and m.channel == message.channel

    if message.content.startswith(commandSign + "invest"):

        if (await check_for_id(message.author.id)):
            await message.channel.send("You've already made your weekly prediction, sorry!")
            return

        await message.channel.send('Welcome to the investing bot!')
        await message.channel.send("Tell me how many players would you like to invest in? 1, 2 or 3?")
        count_to = await client.wait_for('message',check=check , timeout=120)

        #TODO: Error checking here

        while int(count_to.content) < 0 or int(count_to.content) > 3:
            await message.channel.send("Please follow simple instructions in the future.")
            await message.channel.send("Select either 1, 2, or 3 players to invest in.")
            count_to = await client.wait_for('message',check=check , timeout=120)

        await message.channel.send("You will be investing in " + count_to.content + " players.")
        user_investment = Investment(message.author.id, []) #create out investment object

        #TODO: Also error checking here
        print("entering for loop with iterations of ", int(count_to.content))

        count_to = int(count_to.content)
        for i in range(count_to):
            await message.channel.send("Please make your selection selection. ")
            card = await client.wait_for('message', check=check, timeout=120)
            card = card.content
            user_investment.invests.append(card)
        
        await write_to_csv(user_investment)
        
# TODO: Finish code to read roster update        
def roster_update():
    url = "http://mlb21.theshow.com/apis/roster_update.json?id=1"
    print("Request from: ", url)
    rq = requests.get(url)
    rq = rq.json()    
    rq = rq['attribute_changes']    # keys = ["name", "current_rank", "old_rank"]
    important_keys = []
    for i in rq:
        important_keys.append(i["name"])
        important_keys.append(i["current_rank"])
        important_keys.append(i["old_rank"])
    return beutify_update(important_keys)


# Lastupdate calls roster update
# Roster update calls beutify update
# Beutify update calls finds biggest gainers with a simple list 
# Of Player objects. Player objects have a name and a attribute change.
async def lastupdate():
    update = roster_update() #This should be a dictionary with name, new and old rank. 
    await find_biggest_gainers(update)

# TODO: Someone please make this functon work
async def find_biggest_gainers(update):
    winners = {}
    return winners

def beutify_update(update):
    player_list = [] #List of Player objects
    for i in range(0, len(update), 3):
        player = Player(update[i], update[i+1] - update[i+2])
        player_list.append(player)
    return player_list


client.run(token)
