user_role_storage = 'user_role_storage.json'

async def send_welcome_message(discord, member):
    embed = discord.Embed(
        title = f'Welcome to the Fife and Drum Corps Discord Server, {member.name}!',
        description = f"We're thrilled to have you here. Please select the reaction below that best matches your position to unlock access to the appropriate channels and roles. This will help us connect you with the right groups and discussions!
                    \n\nHow it works:
                      \n- Click on the emoji that corresponds to your role below.
                      \n- If you're unsure which role to select or need help, feel free to ask in the general chat or contact <@1085413425406021632>.
                    \n\nBefore diving in, please take a moment to review our server rules in <#1316222693988634624>. We can't wait for you to join the conversation!
                    \n\n**Legend**:
                      \n:regional_indicator_a: = I am currently in the Senior Corp
                      \n:regional_indicator_b: = I graduated/left the Corps before 2015
                      \n:regional_indicator_c: = I graduated/left the Corps after 2015",
                    color=discord.Color.blue()
    )
    message = await member.send(embed=embed)
    await message.add_reaction(':regional_indicator_a:')
    await message.add_reaction(':regional_indicator_b:')
    await message.add_reaction(':regional_indicator_c:')

    with open(reaction_message_ids, 'a') as file:
        file.write(f'{message.id};{member.id}\n')