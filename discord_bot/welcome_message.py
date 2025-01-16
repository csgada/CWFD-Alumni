from role_automation import role_assignment, get_user_role, update_user_roles

STATUS_ROLES = {'🇦': 'Senior Corp,',
                '🇧': 'Heritage Alumni',
                '🇨': 'Recent Alumni'
                }

INSTRUMENT_ROLES = {'🪈': 'Fifer',
                    '🥁': 'Drummer',
                    '🔊': 'Bass Drummer'
                    }

async def send_welcome_message(discord, member):
    embed = discord.Embed(
        title = f'Welcome to the Colonial Williamsburg Fife and Drum Corps Discord Server, {member.name}!',
        description = f"""We're thrilled to have you here. Please select the reaction below that best matches your position to unlock access to the appropriate channels and roles. This will help us connect you with the right groups and discussions!
                        \nHow it works:
                        \n- Click on the emoji that corresponds to your status (see **Legend**).
                        \n- If you're unsure which role to select or need help, feel free to ask in the general chat or contact someone with the @:moyai: role.
                        \n
                        \nBefore diving in, please take a moment to review our server rules in #the-handbook. We can't wait for you to join the conversation!
                        \n
                        \n------------------------------------------
                        \n**Legend**:
                        \nStatus:
                        \n🇦 = I am currently in the Senior Corp
                        \n🇧 = I graduated/left the Corps before 2015
                        \n🇨 = I graduated/left the Corps after 2015
                        \n
                        \nInstrument:
                        \n🪈 = I am a fifer
                        \n🥁 = I am a drummer
                        \n🔊 = I am a bass drummer
                        \n------------------------------------------
                        \n
                        \nPlease note that you can only select one role from each category. To change your role, deselect your current role and select the new one.""",
        color=discord.Color.blue()
    )
    message = await member.send(embed=embed)

    for emoji in STATUS_ROLES.keys():
        await message.add_reaction(emoji)
    for emoji in INSTRUMENT_ROLES.keys():    
        await message.add_reaction(emoji)



async def handle_reaction(discord, guild, member, payload, add_role=True):
    emoji = payload.emoji.name
    
    if payload.emoji.name == "🇦":
        await role_assignment(discord, guild, member, 'Senior Corp', add_role)
    elif payload.emoji.name == "🇧":
        await role_assignment(discord, guild, member, 'Heritage Alumni', add_role)
    elif payload.emoji.name == "🇨":
        await role_assignment(discord, guild, member, 'Recent Alumni', add_role)

    if payload.emoji.name == "🪈":
        await role_assignment(discord, guild, member, 'Fifer', add_role)
    elif payload.emoji.name == "🥁":
        await role_assignment(discord, guild, member, 'Drummer', add_role)
    elif payload.emoji.name == "🔊":
        await role_assignment(discord, guild, member, 'Bass Drummer', add_role)