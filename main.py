import discord 

<<<<<<< HEAD
# Not gonna commit my token.
f = open("secretstuff", "r")
token = f.read()


client = discord.Client()
@client.event 
async def on_ready():
    print("Login success.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(token)
