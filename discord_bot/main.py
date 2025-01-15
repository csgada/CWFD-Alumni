import discord
from discord.ext import commands
import os
import ollama_integration

from settings import Settings
from music_retrieval import music_request_retrieval
import role_automation
from welcome_message import send_welcome_message, handle_reaction_add

# read tokens from env
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# initialize bot and settings
intents = discord.Intents.default() # initialize intents (permissions)
intents.members = True # enable reading member list
intents.guilds = True # enable reading guild list
intents.message_content = True # enable reading message content
intents.reactions = True # enable reading reactions
bot = commands.Bot(command_prefix='!', intents=intents) # create a bot instance
settings = Settings() # create a settings object



### COMMANDS
@bot.command()
async def ollama(ctx):
    ''' Talk to the Ollama API. '''
    if settings.is_feature_enabled('ollama'):
        await ollama_integration.ollama_single_chat(ctx)
    else:
        await ctx.send('Ollama feature is disabled.')

@bot.command()
async def toggle_feature(ctx, feature_name):
    ''' Toggle a feature on or off. '''
    response = settings.toggle_feature(feature_name)
    await ctx.send(response)

@bot.command()
async def ping(ctx):
    ''' Check if the bot is functioning as intended. '''
    await ctx.send('Pong!')

@bot.command()
async def tune(ctx, instrument: str, *, tune_name: str):
    ''' Command to request a song. Can only be used in music-request channels. '''
    if settings.is_feature_enabled('music_requests'):
        if ctx.channel.name == 'music-requests':
            try:
                excel_path = './Master List.xlsx'

                file_path = music_request_retrieval(excel_path, tune_name, instrument)

                if not file_path:
                    await ctx.send(f"Sorry, I couldn't find a suitable file for {tune_name} with instrument {instrument}.")
                    return
                
                await ctx.send(f'Found it! Here is the sheet music for {tune_name}: ')
                await ctx.send(file=discord.File(file_path))

            except Exception as e:
                await ctx.send(f'Error: {e}')
    else:
        await ctx.send('Music requests are disabled.')



### EVENTS
# event triggered when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print(f'Starting sync...\n')
    for member in bot.get_all_members():
        await role_automation.add_alumni_role(discord, member, member.guild)
        await role_automation.apply_role_based_channel_access(discord, member.guild, member)
    print(f'Sync complete.')

# event triggered when a new member joins
@bot.event
async def on_member_join(member):
    await send_welcome_message(discord, member)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return  # Ignore bot reactions
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    await handle_reaction_add(discord, member, payload.emoji)

# event triggered when a message is sent
@bot.event
async def on_message(message):
    if settings.is_feature_enabled('easter_eggs'):
        # ignore messages by the bot itself
        if message.author == bot.user:
            return
        
        ### respond to specific messages
        # easter egg 1
        elif message.content.lower() == 'whats the magic number?':
            await message.channel.send('SIR, THE MAGIC NUMBER IS: 757-220-7350, SIR!')
        
        # easter egg 2
        elif message.content.lower() == 'what makes the grass grow?':
            await message.channel.send("BLOOD, BLOOD, BRIGHT RED BLOOD!")

        # easter egg 3
        elif message.content.lower() == 'who likes to hear his name in a song?':
            await message.channel.send("LANCE, LANCE, LANCE!")
            await message.channel.send('https://youtu.be/v6eAe8cID94?si=FPh337BCapEOOEZA')

        # easter egg 4
        elif message.content.lower() == 'shucky ducky':
            await message.channel.send("QUACK QUACK!")
    else:
        print('Easter eggs are disabled.')

    await bot.process_commands(message)


# event triggered when a member gets updated
@bot.event
async def on_member_update(before,after):
    if settings.is_feature_enabled('role_based_channel_access'):
        # # get the member's roles before and after the update
        # before_roles = [role.name for role in before.roles]
        # after_roles = [role.name for role in after.roles]

        await role_automation.add_alumni_role(discord, after, after.guild)
        await role_automation.apply_role_based_channel_access(discord, after.guild, after)



### RUN THE BOT
bot.run(DISCORD_TOKEN, reconnect=True) # run the bot with the token