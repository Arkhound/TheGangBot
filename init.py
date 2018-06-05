# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import sys
 
TOKEN = os.getenv("GangBotToken")
 
client = discord.Client()
 
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
 
    if message.content.startswith('!bot'):
        roles = (str(x) for x in message.author.roles)
        if "Bot Maker" in roles:
            if message.content.endswith('kys'):
                msg = "RIP"
                await client.send_message(message.channel, msg)
                await client.logout()
                await client.close()
                sys.exit(0)
 
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='God'))
 
client.run(TOKEN)