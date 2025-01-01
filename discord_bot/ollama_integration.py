import asyncio
from ollama import chat

async def ollama_command(ctx, model='llama3.1:8b'):
    ''' Handles the Ollama API interaction.'''
    try:
        message = {'role': 'user', 
                   'content': ctx.message.content[7:]
        }
        placeholder_message = await ctx.send('Processing...')

        stream = chat(model=model, messages=[message], stream=True)

        buffer = ''
        full_response = ''
        chunk_count = 0

        for chunk in stream:
            buffer += chunk['message']['content']
            chunk_count += 1
            if chunk_count % 10 == 0:
                full_response += buffer
                buffer = ''
                await placeholder_message.edit(content=full_response)
            asyncio.sleep(0.1)
        
        full_response += buffer
        await placeholder_message.edit(content=full_response)



            

    except Exception as e:
        await ctx.send(f'Error: message not sent. Error message: {e}')