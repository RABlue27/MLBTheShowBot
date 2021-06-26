from asyncio.events import TimerHandle
from asyncio.tasks import wait_for
import discord
from discord import user
from discord import channel 

class Investment:
    def __init__(self, id, invests) -> None:
        self.id = id
        self.invests = invests

    def print_investment(self):
        print(self.id, self.invests)

#TODO: Write to file to change command sign

f = open("secretstuff", "r")
token = f.readline()
commandSign = f.readline()

print(commandSign)
investments = [] #array of investments 
print(investments)

client = discord.Client()
@client.event 
async def on_ready():
    print("Login success.")


#TODO: allow abortion, also check user ID to make sure they arent making multiple investments
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    def check(m):
        return m.author == message.author and m.channel == message.channel

    if message.content.startswith(commandSign + "invest"):
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

        print("Exited the loop")

        investments.append(user_investment)
        return

    # Test command 
    if message.content.startswith(commandSign + "print"):
        investments[0].print_investment()



client.run(token)
