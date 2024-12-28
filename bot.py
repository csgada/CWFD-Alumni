import discord
from discord.ext import commands
from settings import Settings

# read token from external txt file
with open('/Users/carsongada/Stuff/Bot tokens/token.txt', 'r') as f:
    token = f.read()

# initialize bot and settings
intents = discord.Intents.default() # initialize intents (permissions)
intents.members = True # enable reading member list
intents.message_content = True # enable reading message content
bot = commands.Bot(command_prefix='$', intents=intents) # create a bot instance
settings = Settings() # create a settings object



### EVENTS
# event triggered when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# event triggered when a message is sent
@bot.event
async def on_message(message):
    # ignore messages by the bot itself
    if message.author == bot.user:
        return
    
    ### respond to specific messages
    # respond to 'hello'
    if message.content.lower() == 'hello':
        await message.channel.send('Hello!')

    # easter egg 1
    if message.content.lower() == 'whats the magic number?':
        await message.channel.send('SIR, THE MAGIC NUMBER IS: 757-220-7350, SIR!')
    
    # easter egg 2
    if message.content.lower() == 'what makes the grass grow?':
        await message.channel.send("BLOOD, BLOOD, BRIGHT RED BLOOD!")

    # easter egg 3
    if message.content.lower() == 'who likes to hear his name in a song?':
        await message.channel.send("LANCE, LANCE, LANCE!")

    # easter egg 4
    if message.content.lower() == 'shucky ducky':
        await message.channel.send("QUACK QUACK!")



### RUN THE BOT
bot.run(token, reconnect=True) # run the bot with the token