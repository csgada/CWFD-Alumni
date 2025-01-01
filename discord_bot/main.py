import discord
from discord.ext import commands
import os
import ollama_integration
from settings import Settings

# read tokens from env
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# initialize bot and settings
intents = discord.Intents.default() # initialize intents (permissions)
intents.members = True # enable reading member list
intents.guilds = True # enable reading guild list
intents.message_content = True # enable reading message content
bot = commands.Bot(command_prefix='!', intents=intents) # create a bot instance
settings = Settings() # create a settings object

role_channel_mapping = {
    'alumni-fifers': ('Alumni', 'Fifer'),
    'alumni-drummers': ('Alumni', 'Drummer'),
    'alumni-bassdrums': ('Alumni', 'Bass Drummer'),
    'srcorp-fifers': ('Senior Corp', 'Fifer'),
    'srcorp-drummers': ('Senior Corp', 'Drummer'),
    'srcorp-bassdrums': ('Senior Corp', 'Bass Drummer'),
}

### FUNCTIONS
async def check_roles(member, required_roles):
    user_roles = [role.name for role in member.roles]
    # print(f'\nUser roles: {user_roles}')
    return all(role in user_roles for role in required_roles)

async def apply_role_based_channel_access(guild, member, role_channel_mapping):
    for channel_name, required_roles in role_channel_mapping.items():
        channel = discord.utils.get(guild.channels, name=channel_name)
        if not channel:
            print(f'Channel {channel_name} not found')
            continue

        if await check_roles(member, required_roles):
            await channel.set_permissions(member, view_channel=True)
            # print(f'Added {member.name} to {channel_name}')
        else:
            await channel.set_permissions(member, overwrite=None)
            # print(f'Removed {member.name} from {channel_name}')

async def add_alumni_role(member, guild):
    alumni_role = discord.utils.get(guild.roles, name='Alumni')
    if (discord.utils.get(member.roles, name='Recent Alumni')) or (discord.utils.get(guild.roles, name='Heritage Alumni')):
        await member.add_roles(alumni_role)
        # print(f'Added Alumni role to {member.name}')
    else:
        await member.remove_roles(alumni_role)
    
async def sync_on_ready():
    print(f'Starting sync...\n')
    for member in bot.get_all_members():
        await add_alumni_role(member, member.guild)
        await apply_role_based_channel_access(member.guild, member, role_channel_mapping)
    print(f'Sync complete.')



### COMMANDS
@bot.command()
async def ollama(ctx):
    ''' Talk to the Ollama API. '''
    if settings.is_feature_enabled('ollama'):
        await ollama_integration.ollama_command(ctx)
    else:
        await ctx.send('Ollama feature is disabled.')

@bot.command()
async def toggle_feature(ctx, feature_name):
    ''' Toggle a feature on or off. '''
    response = settings.toggle_feature(feature_name)
    await ctx.send(response)

@bot.command()
async def ping(ctx, feature_name):
    ''' Check if the bot is online. '''
    await ctx.send('Pong!')



### EVENTS
# event triggered when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await sync_on_ready()

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

        await add_alumni_role(after, after.guild)
        await apply_role_based_channel_access(after.guild, after, role_channel_mapping)



### RUN THE BOT
bot.run(DISCORD_TOKEN, reconnect=True) # run the bot with the token