from role_automation import role_assignment

async def send_welcome_message(discord, member):
    embed = discord.Embed(
        title = f'Welcome to the Fife and Drum Corps Discord Server, {member.name}!',
        description = f"""We're thrilled to have you here. Please select the reaction below that best matches your position to unlock access to the appropriate channels and roles. This will help us connect you with the right groups and discussions!
                    \n\nHow it works:
                      \n- Click on the emoji that corresponds to your role below.
                      \n- If you're unsure which role to select or need help, feel free to ask in the general chat or contact someone with the @:moyai: role.
                    \n\nBefore diving in, please take a moment to review our server rules in #the-handbook. We can't wait for you to join the conversation!
                    \n\n**Legend**:
                      \n🇦 = I am currently in the Senior Corp
                      \n🇧 = I graduated/left the Corps before 2015
                      \n🇨 = I graduated/left the Corps after 2015""",
                    color=discord.Color.blue()
    )
    message = await member.send(embed=embed)
    await message.add_reaction('🇦')
    await message.add_reaction('🇧')
    await message.add_reaction('🇨')



async def handle_reaction(discord, guild, member, payload, add_role=True):
    print(f'Handling reaction {payload.emoji.name} for {member.name}')
    if payload.emoji.name == "🇦":
        print(f'Adding Senior Corp role to {member.name}')
        await role_assignment(discord, guild, member, 'Senior Corp', add_role)
    elif payload.emoji.name == "🇧":
        print(f'Adding Heritage Alumni role to {member.name}')
        await role_assignment(discord, guild, member, 'Heritage Alumni', add_role)
    elif payload.emoji.name == "🇨":
        await role_assignment(discord, guild, member, 'Recent Alumni', add_role)