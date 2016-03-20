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
	await bot.say(aways)
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
async def set(ctx, stat: str):
	"""Allows a listener to set their status  <Set your status using \`?status A `\ or \`?status B \` >"""
	gtg = False; 
	status = 0
	check = []

	
	for r in ctx.message.author.roles:	
		if r.name == "Listener":
			gtg = True;
		if r.name == "ready":
			status = 1
		

	if gtg == True:
		if stat == "A":
			if status == 0:
				await bot.add_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles, name='ready'))
				print ("Gave " + ctx.message.author.name + " Ready")
				await bot.say(ctx.message.author.mention + " You are now Available. Woohoo!") 
				status = 1
			else:
				await bot.say("You're already Available")
		elif stat == "B":
			if status == 1: 
				await bot.remove_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles, name='ready'))
				print ("Removed " + ctx.message.author.name + " Ready role")
				await bot.say(ctx.message.author.mention + " You are now Busy. ") 
				status = 0
			else: 
				await bot.say("You're already UnAvailable")
		
		else: 
			await bot.say("That is not a valid role, please choose \"A(Available)/B(busy)\" ") 
	else: 
		await bot.say("This function works only for listeners")
		
				

botname = config.get("logins", "email")
botpass = config.get("logins", "pass")

bot.run(botname, botpass)
