user_role_storage = 'user_role_storage.json'

role_channel_mapping = {
    'alumni-fifers': ('Alumni', 'Fifer'),
    'alumni-drummers': ('Alumni', 'Drummer'),
    'alumni-bassdrums': ('Alumni', 'Bass Drummer'),
    'srcorp-fifers': ('Senior Corp', 'Fifer'),
    'srcorp-drummers': ('Senior Corp', 'Drummer'),
    'srcorp-bassdrums': ('Senior Corp', 'Bass Drummer'),
}



### Alumni Role Automation Functions
async def check_roles(member, required_roles):
    user_roles = [role.name for role in member.roles]
    return all(role in user_roles for role in required_roles)

async def apply_role_based_channel_access(discord, guild, member):
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

async def add_alumni_role(discord, member, guild):
    alumni_role = discord.utils.get(guild.roles, name='Alumni')
    if (discord.utils.get(member.roles, name='Recent Alumni')) or (discord.utils.get(guild.roles, name='Heritage Alumni')):
        await member.add_roles(alumni_role)
        # print(f'Added Alumni role to {member.name}')
    else:
        await member.remove_roles(alumni_role)



### Reaction Role Functions
async def remove_reaction_role(discord, member, role_name):
    role = discord.utils.get(member.guild.roles, name=role_name)
    if role in member.roles:
        await member.remove_roles(role)

async def add_reaction_role(discord, member, role_name):
    role = discord.utils.get(member.guild.roles, name=role_name)
    if role not in member.roles:
        await member.add_roles(role)

