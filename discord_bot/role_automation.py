import json



### JSON Helper Functions
user_role_storage = 'discord_bot/user_role_storage.json'

def load_roles():
    try:
        with open(user_role_storage, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    
def save_roles(user_roles):
    with open(user_role_storage, 'w') as file:
        json.dump(user_roles, file)

def get_user_role(user_id):
    user_roles = load_roles()
    return user_roles.get(str(user_id), [])

def update_user_roles(user_id, roles):
    user_roles = load_roles()
    if roles:
        user_roles[str(user_id)] = roles
    else:
        user_roles.pop(str(user_id), None)
    save_roles(user_roles)



### Role Assignment Functions
async def role_assignment(discord, guild, member, role_name, add_role=True):
    current_roles = get_user_role(member.id)

    if add_role:
        if role_name not in current_roles:
            await member.add_roles(discord.utils.get(guild.roles, name=role_name))
            current_roles.append(role_name)
        else:
            return # Role is already assigned. Will eventually add this to log.
    else:
        if role_name in current_roles:
            await member.remove_roles(discord.utils.get(guild.roles, name=role_name))
            current_roles.remove(role_name)
        else:
            return # Role is not assigned. Will eventually add this to log.
        
    
    update_user_roles(member.id, current_roles)



### Role Channel Mapping Functions
role_channel_mapping = {
    'alumni-fifers': ('Alumni', 'Fifer'),
    'alumni-drummers': ('Alumni', 'Drummer'),
    'alumni-bassdrums': ('Alumni', 'Bass Drummer'),
    'srcorp-fifers': ('Senior Corp', 'Fifer'),
    'srcorp-drummers': ('Senior Corp', 'Drummer'),
    'srcorp-bassdrums': ('Senior Corp', 'Bass Drummer'),
}

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



### Alumni Role Automation Functions
async def assign_alumni_role(discord, guild, member):
    if (discord.utils.get(member.roles, name='Recent Alumni')) or (discord.utils.get(member.roles, name='Heritage Alumni')):
        await role_assignment(discord, guild, member, 'Alumni', add_role=True)
    else:
        await role_assignment(discord, guild, member, 'Alumni', add_role=False)
