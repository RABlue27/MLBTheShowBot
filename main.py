import discord
import requests
import csv
from asyncio.events import TimerHandle
from asyncio.tasks import wait_for
from discord import user
from discord import channel 
class Investment:
    def __init__(self, id, invests) -> None:
        self.id = id
        self.invests = invests

    def print_investment(self):
        print(self.id, self.invests)

#TODO: Write to file to change command sign

f = open("secretstuff.txt", "r")
token = f.readline()
commandSign = f.readline()

print(commandSign)


client = discord.Client()
@client.event 
async def on_ready():
    print("Login success.")


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
        # user_investment.print()

        #TODO: Als error checking here
        print("entering for loop with iterations of ", int(count_to.content))

        #Theres gotta be a better way to do this, but async in a for loop doesnt seem to work


        count_to = int(count_to.content)
        await message.channel.send("Please make your first selection. ")
        card = await client.wait_for('message', check=check, timeout=120)
        card = card.content
        user_investment.invests.append(card)
        # print(user_investment)
        
        if (count_to >= 2):
            await message.channel.send("Please make your second selection. ")
            card = await client.wait_for('message', check=check, timeout=120)
            card = card.content
            user_investment.invests.append(card)
        if (count_to == 3):
            await message.channel.send("Please make your third selection. ")
            card = await client.wait_for('message', check=check, timeout=120)
            card = card.content
            user_investment.invests.append(card)

        await write_to_csv(user_investment)
        
# TODO: Finish code to read roster update      
# ? Does it have to be async? Does it matter?  
def roster_update():
    url = "http://mlb21.theshow.com/apis/roster_update.json?id=1"
    resp = requests.get(url)
    calc_score(resp)

# TODO: Go through the entire CSV to identify score. Give role to best player.
async def calc_score(resp):
    return 

client.run(token)
