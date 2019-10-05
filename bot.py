#!/usr/bin/env python
from game import Games
# Work with Python 3.6
import discord
import os

discord_hello_token = os.environ['DISCORD_HELLO_TOKEN']

games = Games()

client = discord.Client()

@client.event
async def on_message(message):

    # Do not want the bot to reply to itself
    if message.author == client.user:
        return

    # Not sure if this opens up some exploits. Feels unsafe.
    if message.content.startswith('!echo'):
        await message.channel.send(message.content)

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('!help'):
        msg = '''
!echo - repeat what was typed
!hello - replies with 'hello <username>'
!help - this page
!whisper
'''
        await message.channel.send(msg)
    
    if message.content.startswith('!whisper'):
        #user=await client.get_user_info(message.author.id)
        await message.author.send("I'm a very tall midget")
    
    if message.content.startswith('!join'):
        current_channel = str(message.channel.guild) + str(message.channel.id)
        if current_channel in games:
            games.addUser(current_channel, message.author)
        else:
            games.addChannel(current_channel)
            games.addUser(current_channel, message.author)
        msg = 'User {0.author.mention} is included in the {1} game'.format(message, current_channel)
        await message.channel.send(msg)

    if message.content.startswith('!users'):
        current_channel = str(message.channel.guild) + str(message.channel.id)
        msg = '''Joined users in game:
        '''
        if current_channel in games:
            for user in games[current_channel]:
                msg += '''user 
                '''.format(user)
        else :
            msg = ''' No users in THE GAME'''
        await message.channel.send(msg)
    
    if message.content.startswith('!start'):
        
        

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(discord_hello_token)