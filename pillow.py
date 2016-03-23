#Version: 0.2.1
#last edit by: iso, at 3:47 am CST March 23

import os
import time
import discord
from discord.ext import commands
import configparser

description = '''A bot to allow listeners and persons in need to better connect with one another.  

Written by: iso, Alienaura, and Punk''' 
bot = commands.Bot(command_prefix='?', description=description)
config = configparser.ConfigParser() 
config.read("config.ini")

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
	f = open('listeners.txt') 
	lines = f.read().splitlines() 
	for line in lines: 
		print (line) 
	f.close() 

@bot.command(pass_context=True)
async def scan(ctx): 
	"""This does nothing...Ignore it"""
	count = 0
	print (ctx.message.author.id)
	if ctx.message.author.id == '102110056148910080':
		outfile = open('listeners.txt', 'w+')
		for p in ctx.message.server.members: 
			if discord.utils.get(ctx.message.server.roles, name = 'Listener') in p.roles:
				outfile.write(p.id + '\n')
				count += 1
		outfile.close()
		print("Done scanning, added: " + str(count) + " listeners") 
		await bot.say("Scanned: " + str(count) + "! Use clockadd to insert more") 
	else: 
		await bot.say ("You cant use this, sorry")
		
@bot.command(pass_context=True)
async def clockadd(ctx, user : discord.Member): 
	"""Managers only command"""
	if discord.utils.get(ctx.message.server.roles, name = 'Listener Manager') in ctx.message.author.roles:
		found = False
		if discord.utils.get(ctx.message.server.roles, name = 'Listener') not in user.roles: 
			await bot.say("https://cdn.discordapp.com/attachments/157939461735448577/162098700213026817/11agbr.jpg") 
			await bot.say("Don't worry bro, I got it" ) 
			time.sleep(3)
			await bot.add_roles(user, discord.utils.get(ctx.message.server.roles, name= 'Listener'))
			await bot.say("Gave this user a listener tag and added them to the list if they werent already there") 
			
		with open('listeners.txt') as lfile: 
			found = False
			for line in lfile:
				if user.id in line: 
					print(user.name + " is already in list")
					await bot.say( user.mention + " is already clocked in")  
					found = True			
		if found == False: 
			lfile.close()
			with open ('listeners.txt', "a") as lfile: 
				print("Added: " + user.name + " to ready file!") 
				lfile.write(user.id + '\n') 
				lfile.close()  
	else: 
		print(ctx.message.author.name + " tried to use clockadd!")
		await bot.say("This command is for Listener Managers only")  

@bot.command(pass_context=True)
async def clockdel(ctx, user : discord.Member): 
	"""Managers only command"""
	if discord.utils.get(ctx.message.server.roles, name = 'Listener Manager') in ctx.message.author.roles: 
		fn = 'listeners.txt' 
		f = open(fn) 
		tmp = [] 
		found = False 
		for line in f: 
			if not user.id + '\n' in line: 
				tmp.append(line) 
			else: 
				found = True
		f.close() 
		f = open(fn, 'w') 
		f.writelines(tmp)
		f.close() 	
		
		if found == True:	
			await bot.say("User deleted successfully") 
			await bot.say("If they have the Listener role, it will be removed now too")
			await bot.remove_roles(user, discord.utils.get(ctx.message.server.roles, name= 'Listener'))
			await bot.remove_roles(user, discord.utils.get(ctx.message.server.roles, name= 'ready'))
		else: 
			await bot.say("That user was not found in the list, add them with clockadd or manually remove their tags") 

	else: 
		await bot.say("This command is for Listener Managers only") 
		print(ctx.message.author.name + " tried to use clockdel") 

@bot.command(pass_context=True)
async def list(ctx):
	"""Prints out the list of listeners"""
	readied = ''
	aways = ''	
	listeners = []
	rolen = "ready"
	l_count = 0
	on_count = 0
	ready = False
	
	for person in ctx.message.server.members: 
		
		for role in person.roles:
			if role.name == "Listener":
				listeners.append(person)
				l_count += 1
	for listener in listeners:
		ready = False
		if listener.status== discord.Status.online:
				
			for role in listener.roles:
				if role.name == "ready":
					on_count += 1
					ready = True	
			if ready == True: 
				readied += "**" + listener.name + " -- Available**"
			else: 
				readied += listener.name
					 
			readied += '\n'	
		elif listener.status == discord.Status.idle :
			aways +=  listener.name + " --Away/Idle\n"
	await bot.say("There are currently " + str(on_count) + "/" + str(l_count) + " listener(s) Available right now:")
	await bot.say("-------------------------------------------Online-------------------------------------------")	
	await bot.say(readied)
	await bot.say("--------------------------------------------Away--------------------------------------------")
	if aways: 
		await bot.say(aways)
	else: 
		await bot.say("Nobody is away") 
	await bot.say("If you require assistance, just type ?ineedhelp or if you would like to notify the active listeners type ?listeners")


@bot.command(pass_context=True)
async def listeners(ctx):
	"""Calls the listeners"""
	l1 = []
	output = ''
	count = 0
	for person in ctx.message.server.members: 
		for r in person.roles:
			if r.name == "Listener":
				l1.append(person)
	for listener in l1:
		if listener.status == discord.Status.online:
			for r in listener.roles:
				if r.name == "ready":
					count += 1
					output += listener.mention + " "
	if (count > 0): 
		await bot.say(output)
	else: 
		await bot.say("There are no listeners currently Available. You may still PM one, or wait for a member of lighthouse to help") 





@bot.command(pass_context=True)
async def status(ctx): 
	"""Displays your current availability"""
	mode = 0
	for r in ctx.message.author.roles:	
		if r.name == "Listener":
			gtg = True;
		if r.name == "ready":
			mode = 1
	if mode == 1:
		await bot.say("You are currently Available to help people") 
	else: 
		await bot.say("You are unAvailable to help at this time")


@bot.command(pass_context=True)
async def clockio(ctx):
	"""Lets listeners clock in and out"""
	gtg = False
	status = 0
	check = []
	legals = [line.rstrip('\n') for line in open('listeners.txt')]
	cin = []
	cout = []
	for p in ctx.message.server.members:
		if p.id in legals:
			check.append(p)
	for p in check:
		if discord.utils.get(ctx.message.server.roles, name = 'Listener') in p.roles:
			cin.append(p)
		else: 
			cout.append(p)
				
					
	if (ctx.message.author in check and ctx.message.author in cin):
		await bot.remove_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles, name='Listener'))
		print (ctx.message.author.mention + 'is now clocked out' ) 
		await bot.say(ctx.message.author.mention + ", you are now clocked out!") 
	elif (ctx.message.author in check and ctx.message.author in cout): 
		await bot.add_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles, name= 'Listener'))
		print (ctx.message.author.mention + "is now clocked in") 
		await bot.say(ctx.message.author.mention + ", you are now clocked in!") 
	else: 
		await bot.say("This command is for listeners only! If this is in error, contact kev or iso")

@bot.command(pass_context=True)
async def ready(ctx):
	"""Allows Listeners to set their availability"""
	if discord.utils.get(ctx.message.server.roles, name = 'Listener') in ctx.message.author.roles: 
		if discord.utils.get(ctx.message.server.roles, name = 'ready')  in ctx.message.author.roles: 
			await bot.remove_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles, name= 'ready')) 
			print(ctx.message.author.name + " is busy") 
			await bot.say(ctx.message.author.mention + ". You are now busy") 
		else: 
			await bot.add_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles, name= 'ready')) 
			print(ctx.message.author.name + " is ready") 
			await bot.say(ctx.message.author.mention + ". You are now ready! Woohoo!") 
	else: 
		print(ctx.message.author.name + " is not a listener") 
		await bot.say("This command is for listeners only") 




botname = config.get("logins", "email")
botpass = config.get("logins", "pass")

bot.run(botname, botpass)


