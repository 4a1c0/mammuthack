#!/usr/bin/env python
from game import Games
from game_engine import Game
# Work with Python 3.6
import discord
import os
import threading
import asyncio

from datetime import datetime

async def check_turn(client,timestamps, usersresponse):
    while True:
        await asyncio.sleep(5)
        # threading.Timer(5.0, check_turn, [client,timestamps, usersresponse]).start()
        for channel, time in timestamps.items(): 
            if datetime.timestamp(datetime.now()) - time  > 10 and datetime.timestamp(datetime.now()) - time  < 30:
                for user, val in usersresponse[channel].items():
                    if val == 0:
                        await client.get_user(user.id).send("Respon")
          




discord_hello_token = os.environ['DISCORD_HELLO_TOKEN']

games = Games()
users = {}
channelgame = {}
usersresponse = {}
timestamps = {}

client = discord.Client()

@client.event
async def on_message(message):

    # Do not want the bot to reply to itself
    if message.author == client.user:
        return
    
    if message.content.startswith('!test'):
        await message.channel.send(message.channel.type)

    if str(message.channel.type) == "text":

        if message.content.startswith('!help'):
            msg = '''   !join - 
    !start - 
    !help - this page
    !whisper -
    In DM:
        !stats
    '''
            await message.channel.send(msg)
        
        if message.content.startswith('!whisper'):
            #user=await client.get_user_info(message.author.id)
            await message.author.send("I'm a very tall midget")
        
    

        if message.content.startswith('!join'):
            current_channel = str(message.channel.guild) + str(message.channel.id)
            msg = 'User {0.author.mention} is included in the {1} game'.format(message, current_channel)
            if current_channel in games:
                if message.author in games[current_channel]:
                    msg = '{0.author.mention} is already in {1} game'.format(message, current_channel)
                else:
                    games.addUser(current_channel, message.author)
            else:
                games.addChannel(current_channel)
                games.addUser(current_channel, message.author)
            
            await message.channel.send(msg)

        if message.content.startswith('!users'):
            current_channel = str(message.channel.guild) + str(message.channel.id)
            msg = '''Joined users in game:
            '''
            if current_channel in games:
                for user in games[current_channel]:
                    msg += '''user {}
                    '''.format(user)
            else :
                msg = ''' No users in THE GAME'''
            await message.channel.send(msg)
        
        if message.content.startswith('!start'):
            current_channel = str(message.channel.guild) + str(message.channel.id)
            if current_channel in games:
                if len(games[current_channel]) < 1: #TODO 3
                    msg = '''Not enough people'''
                elif len(games[current_channel]) > 8: 
                    msg = '''Too much people'''
                else:
                    msg = '''The GAME starts'''
                    for user in games[current_channel]:
                        users[user.id] = current_channel
                        await client.get_user(user.id).send("Private DM")
            await message.channel.send(msg)
            await message.channel.send("Game ")
            timestamps[current_channel] = datetime.timestamp(datetime.now())
            for user in games[current_channel]:
                usersresponse[current_channel] = {user : 0 }
            await check_turn(client,timestamps, usersresponse)
            # channelgame[current_channel] = Game()

            # resp = channelgame[current_channel].Start()
            
    else:  # Private DM
        if message.content.startswith('!stats'):
            
            if message.author.id in users:
                msg = str(users[message.author.id]) + str(usersresponse[users[message.author.id]][message.author.id])
            else:
                msg = "No game has started "

            await message.author.send(msg)
        if message.content.startswith('!continue'):
            if message.author.id in users:
                usersresponse[users[message.author.id]][message.author.id]= 1

        if message.content.startswith('!leave'):
            if message.author.id in users:
                usersresponse[users[message.author.id]][message.author.id]= -1

        

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    client.loop.create_task(check_turn(client,timestamps, usersresponse))


client.run(discord_hello_token)