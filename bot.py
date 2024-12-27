import discord
from settings import Settings

with open('/Users/carsongada/Stuff/Bot tokens/token.txt', 'r') as f:
    token = f.read()

# set up intents (permissions for the bots)
intents = discord.Intents.default()
intents.message_content = True # enable reading message content

# create a client instance
client = discord.Client(intents=intents)



### EVENT
# event triggered when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# event triggered when a message is sent
@client.event
async def on_message(message):
    # ignore messages by the bot itself
    if message.author == client.user:
        return
    
    ### respond to specific messages
    # respond to 'hello'
    if message.content.lower() == '$hello':
        await message.channel.send('Hello!')

    # easter egg 1
    if message.content.lower() == "$what's the magic number?":
        await message.channel.send("SIR, THE MAGIC NUMBER IS 757-220-7350, SIR!")
    
    # easter egg 2
    if message.content.lower() == '$what makes the grass grow?':
        await message.channel.send("BLOOD, BLOOD, BRIGHT RED BLOOD!")

    # easter egg 3
    if message.content.lower() == '$who likes to hear his name in a song?':
        await message.channel.send("LANCE, LANCE, LANCE!")

    # easter egg 2
    if message.content.lower() == '$shucky ducky':
        await message.channel.send("QUACK QUACK!")



### RUN THE BOT
# run the bot with the token
client.run(token, reconnect=True)