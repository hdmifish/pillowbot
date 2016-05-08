
#!/usr/local/bin/python3.5
#filename=fluffedpillow.py
#Version: 0.3.0
#last edit by: iso, at 10:03 am CST April 4

import discord
import asyncio
from datetime import datetime
import time

client = discord.Client() #obvious
compref = '?' #command prefix for discord public chat. PM's do not require it
owner = 'your id' #Gives full admin rights to bot regardless of roll, to this user. Me.
def load():

        with open('/pillow/listeners.txt') as f:
                lines = f.read().splitlines()
                print(lines)
        return lines

def say(message, words, log = False):
        #yield from client.send_typing(message.channel)
        yield from client.send_message(message.channel, str(words))
        stamp = timestamp()

        #I kinda wanted to remove this too. It really isnt useful.
        if (log):
                print(stamp +  'Said: ' + str(words))
        return

def timestamp():
        return (str(datetime.now()) + '|=> ')

@client.async_event
def on_ready():
        print ('Pillow is connected!')
        print ('My name is: ' + client.user.name)
        print ('and My ID is: ' + client.user.id + '.')
        print ('I report to: [' + owner+ '].')
        print ('And my command prefix is: \"' + compref + '\".')
        print('Startup complete')

@client.async_event
def on_message(message):
        if message.author == client.user:
                return

        if message.content.startswith(compref):
                func = message.content.lstrip(compref)

                if (func == 'test'):
                                lcount = 0
                                ucount = 0
                                lines = load()
                                for mem in message.server.members:
                                        ucount += 1
                                        if mem.id in lines:
                                                        ltcount += 1
                                yield from say(message, 'There are currently: ' + str(lcount) + ' Listeners out of: ' + str(ucount) + ' users.\nHope you liked my test message!')
                                return

                if func.startswith('clockadd'):
                        lines = load()
                        if discord.utils.get(message.server.roles, name = 'Listener Manager') not in message.author.roles:
                                yield from say(message, 'This command is for Listener Managers only')
                                return
                        userid = func.lstrip('clockadd <@')
                        userid = userid.rstrip('>')
                        user = discord.utils.get(message.server.members, id=userid)
                        if user is None:
                                yield from say(message, 'This user doesn\'t exist')
                                return

                        if discord.utils.get(message.server.roles, name = 'Listener') not in user.roles:
                                yield from say(message, 'https://cdn.discordapp.com/attachments/157939461735448577/162098700213026817/11agbr.jpg')
                                yield from say(message, "Don't worry bro, I got it" )
                                time.sleep(3)
                                yield from client.add_roles(user, discord.utils.get(message.server.roles, name= 'Listener'))
                                yield from say(message, "Gave this user a listener tag and added them to the list if they werent already there")
                                if user.id not in lines:
                                        with open('/pillow/listeners.txt', 'a') as f:
                                                f.write(user.id + '\n')
                                        print('Wrote ' + user.name +' - id to the list')
                        else:
                                yield from say(message, 'That person is already a listener. I attempted to add them to the magical list anyway')
                                if user.id not in lines:
                                        with open('/pillow/listeners.txt', 'a') as f:
                                                f.write(user.id + '\n')
                                        print('Wrote ' + user.name +' - id to the list')
                        return

                if func.startswith('clockdel'):
                        lines = load()
                        if discord.utils.get(message.server.roles, name = 'Listener Manager') not in message.author.roles:
                                yield from say(message, 'This command is for Listener Managers only')
                                return
                        userid = func.lstrip('clockdel <@')
                        userid = userid.rstrip('>')
                        user = discord.utils.get(message.server.members, id=userid)
                        if user is None:
                                yield from say(message, 'This user doesn\'t exist')
                                return
                        if discord.utils.get(message.server.roles, name = 'Listener') in user.roles:
                                yield from client.remove_roles(user, discord.utils.get(message.server.roles, name= 'Listener'))
                                yield from client.remove_roles(user, discord.utils.get(message.server.roles, name= 'ready'))
                                yield from say(message, "Removing listener's tag and deleting them from the magic list")
                                for line in lines:
                                        if user.id == line:
                                                lines.remove(line)
                                print ('writing: ' + str(lines) + '\nTo file')
                                with open('/pillow/listeners.txt', 'w') as f:
                                        for line in lines:
                                                f.write(line + '\n')


                        else:

                                yield from say(message, "Pretty sure that person isnt a listener. Or if they are, they are clocked out. So i'll just delete them from the list")
                                if user.id in lines:
                                        lines.remove(user.id)
                                        with open('/pillow/listeners.txt', 'w') as f:
                                                f.writelines(lines)
                        return

                if (func == 'list'):

                        lines = load()
                        readied = ""
                        msg = ""
                        l_count = 0
                        on_count = 0
                        for item in lines:
                                user = discord.utils.get(message.server.members, id = item)

                                if (user.status == discord.Status.online) and (discord.utils.get(message.server.roles, name = 'Listener') in user.roles):
                                        l_count += 1
                                        if (discord.utils.get(message.server.roles, name='ready') in user.roles):
                                                readied += 'READY---> ' + user.name + ' <----READY\n'
                                                on_count += 1
                                        else:
                                                readied += user.name + '\n'

                        msg += "There are currently " + str(on_count) + " of " + str(l_count) + " online listeners actively available right now: \n\n" + '```\n' + "Online-------------------------------------------" + '\n' + readied +  '\n' + "```\n\n" + "If you need immediate help and no listeners are online pm an admin or listener manager. \n\n Listeners on the list are online and willing to help, readied listeners are just priority.\nAlso, if you would like to tag all available listeners, do `>tbro ready`"
                        yield from say(message, msg)
                        return

                if (func == 'ready'):
                        if discord.utils.get(message.server.roles, name = 'Listener') in message.author.roles:
                                if discord.utils.get(message.server.roles, name = 'ready')  in message.author.roles:
                                        yield from client.remove_roles(message.author, discord.utils.get(message.server.roles, name= 'ready'))
                                        print(message.author.name + " is busy")
                                        yield from say(message, message.author.mention + ". You are now busy (hopefully helping someone)")
                                else:
                                        yield from client.add_roles(message.author, discord.utils.get(message.server.roles, name= 'ready'))
                                        print(message.author.name + " is ready")
                                        yield from say(message, message.author.mention + ". You are now ready to help people! Woohoo!")
                        else:
                                print(message.author.name + " is not a listener")
                                yield from say(message, "This command is for listeners only")
                        return

                if (func == 'clockio'):
                        lines = load()
                        if (message.author.id in lines) and (discord.utils.get(message.server.roles, name= 'Listener') in message.author.roles):
                                yield from client.remove_roles(message.author, discord.utils.get(message.server.roles, name='Listener'))
                                time.sleep(1)
                                if discord.utils.get(message.server.roles, name= 'ready') in message.author.roles:
                                        yield from client.remove_roles(message.author, discord.utils.get(message.server.roles, name= 'ready'))
                                print (message.author.name + 'is now clocked out' )
                                time.sleep(1)
                                yield from say(message, message.author.mention + ", you are now clocked out!")
                                return

                        elif (message.author.id in lines) and (discord.utils.get(message.server.roles, name= 'Listener') not in message.author.roles):
                                yield from client.add_roles(message.author, discord.utils.get(message.server.roles, name= 'Listener'))
                                time.sleep(1)
                                print (message.author.name + "is now clocked in")
                                yield from say(message, message.author.mention + ", you are now clocked in! Be sure to use `?ready` too if you arent helping anyone currently")
                                return

                        else:
                                yield from say("This command is for listeners only! If this is in error, contact <@102110056148910080>")
                                return


                if (func == 'status'):
                        lines = load()
                        if message.author.id in lines:
                                if (discord.utils.get(message.server.roles, name= 'ready') in message.author.roles ) and (discord.utils.get(message.server.roles, name= 'Listener') in message.author.roles):
                                        yield from say(message, "You are marked as `Ready Listener` to help people. Do `?ready` if you are helping someone to prevent getting overwhelmed")

                                elif (discord.utils.get(message.server.roles, name='Listener') in message.author.roles):
                                        yield from say(message, "You are marked as `Listener` If you are clocked in and not helping somone and have the time to monitor intt, do `?ready` please.")

                                else:
                                        yield from say(message, "You are clocked out, do `?clockio`")
                        else:
                                yield from say(message, "This command is for listeners only. If you are a listener, please clock in first.")
                        return

                if (func == 'about'):
                        yield from say(message, '```\n[Pillow v1.3  AKA Listenerbot]\n\nA Discord bot created for Patch Gaming as a tool to help persons in need\nbetter receive help from the listeners.\nIt also allows listeners to better manage their\navailability.```\n\nIf you are interested in becoming a listener. PM <@96461620976300032> , <@102110056148910080> , <@92374814211203072> , <@108309693369196544> , or <@95385476541718528>')

client.run('your token here') 
#Ok not that you really need to run pillowbot, at all. Like its for one server, fuck off. This is more for alien and me
