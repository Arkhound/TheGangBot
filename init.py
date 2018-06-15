# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import os
import discord
import sys
import aiohttp
import sqlite3 as sql
from bs4 import BeautifulSoup

TOKEN = os.getenv("GangBotToken")
 
client = discord.Client()
session = aiohttp.ClientSession()
conn = sql.connect('locations.db')
curs = conn.cursor()

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

    elif message.content.startswith('!add'):
        urls = message.content.split(' ')[1:]
        for url in urls:
            print('|' + url+  '|')
            await scrape(url, message.channel)
        return 

# Takes a url and a discord channel.  Tries to scrape for information to add to database and messages relevant
# channel. 
async def scrape(url, channel):
    try:
        resp = await session.get(url)
        html = await resp.text(encoding='utf-8')
        soup = BeautifulSoup(html, 'html.parser')
    except Exception as e:
        print('Failed to get and/or parse web page. ', e)
        return

    if url.startswith('https://www.yelp.com/biz'):
        try:
            # Find element by class attr, get first and only child element, strip lead and end whitespace.
            name = soup.find('h1', {'class' : 'biz-page-title'}).contents[0].strip()

            # Utility function that takes advantage of repetitive html to strip address from yelp.
            def from_attr(itemprop):
                return soup(itemprop=itemprop)[0].contents[0]
            street_address = from_attr('streetAddress')
            locality = from_attr('addressLocality')
            region = from_attr('addressRegion')
            zip_ = from_attr('postalCode')
        except NameError as e:
            print('Failed to extract from BeautifulSoup. ', e.__dict__, 'url: ', url)
            return
        try:
            # Use name and street address to check for uniqueness.
            curs.execute('SELECT * FROM restaurants WHERE name=? AND street_address=?', 
                         (name, street_address))
            res = curs.fetchall()
            if len(res) > 0:
                msg = name + ' already in database.'
                await client.send_message(channel, msg)
            elif len(res) == 0:
                curs.execute('INSERT INTO restaurants VALUES (?, ?, ?, ?, ?)', 
                             (name, street_address, locality, region, zip_))
                msg = name + ' added to database.'
                conn.commit()
                await client.send_message(channel, msg)
        except Exception as e:
            print('Failed to add to database. ', e)
            return

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='God'))
 
client.run(TOKEN)