import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import json
import os
import datetime
import traceback
#tijd = int(time.strftime("%M"))
#tijd1 = str(time.strftime("%c"))
#tijd1 = datetime.datetime.now().strftime("%c")
cp = '$'
bot = commands.Bot(command_prefix=cp)

print ('Bot is aan het laden...')
print ('.....')
print ('Het laden is bijna compleet!')
print ('Bij errors exit invoeren in console!')
print ('De command prefix die wordt gebruikt is ' + cp)
print ('...')
print ('...')
print ('We zijn er bijna!')
print ('Ter info! De bot is niet bedoeld als U-bot maar als Discord Bot')
print ('Versie 1.3')
print ('Nieuwe logo en naam')
@bot.event
async def on_ready():
    await bot.edit_profile(username="Aardappelen")
    await bot.change_presence(game=discord.Game(name='Use {}help | Aardappelen'.format(cp)))
    print('Bot is geladen als')
    print(bot.user.name)
    print(bot.user.id)

@bot.event
async def on_member_join(member):
	rollie8 = discord.utils.get(member.server.roles, name="Leden")
	rollie9 = discord.utils.get(member.server.roles, name="member")
	await bot.add_roles(member, rollie8, rollie9)
	


@bot.event
async def on_member_remove(member):
    server = member.server.get_channel("434708369496997912")
    fmt = ('{} left the server!' .format(member))
    await bot.send_message(server, fmt.format(member, member.server))
	
	
@bot.listen('on_member_join')
async def member_join_2(kakmens1):
    server = kakmens1.server.get_channel("434708369496997912")
    fmt = 'Welcome at the {1.name} Discord server, {0.mention}, read the rules and enjoy the server!'
    await bot.send_message(server, fmt.format(kakmens1, kakmens1.server))
	
	
@bot.command(pass_context = True)
@commands.has_permissions(kick_members = True)
async def kick(ctx, userName: discord.User):
	author = ctx.message.author
	server = author.server
	try:
		await bot.kick(userName)
		await bot.say("*** :white_check_mark:  The user {} has been kicked***" .format(userName))
		
	except discord.errors.Forbidden as error:
		await bot.say("Je mag jezelf geen pijn doen maatje!")
		
		
@bot.command(pass_context = True)
@commands.has_permissions(ban_members = True)
async def ban(ctx, userName: discord.User):
    """Ban a user"""
    await bot.ban(userName)
    await bot.say("*** :white_check_mark: The user {} had been banned***" .format(userName))


@bot.command(pass_context = True)
#@commands.has_permissions(manage_messages =  True)
async def purge(ctx, number):
	try:
		mgs = [] #Empty list to put all the messages in the log
		number = int(number) #Converting the amount of messages to delete to an integer
		async for x in bot.logs_from(ctx.message.channel, limit = number):
			mgs.append(x)
		await bot.delete_messages(mgs)
		await bot.say("** {} messages have been deleted:white_check_mark:**".format(number))
	except BaseException as error:
		traceback.print_exc()
		await bot.say("Er is iets fout gelopen, hier is de volledige error voor de Dev: `" + str(error) + "`")

@bot.command(pass_context = True)
@commands.has_permissions(manage_messages =  True)
async def massdelete(ctx, number):
	try:
		number = int(number) #Converting the amount of messages to delete to an integer
		counter = 0
		async for x in bot.logs_from(ctx.message.channel, limit = number):
			if counter < number:
				await bot.delete_message(x)
				counter += 1
				await asyncio.sleep(1.2) #1.2 second timer so the deleting process can be even
	except BaseException as error:
		traceback.print_exc()
		await bot.say("Er is iets fout gelopen, hier is de volledige error voor de Dev: `" + str(error) + "`")
			

@bot.command(name="8ball")
async def _ball():
     await bot.say(random.choice([":8ball: Without a doubt.", ":8ball: Yes definitely. ", ":8ball: Signs point to yes.", ":8ball: Outlook not so good.", ":8ball: Better not tell you now.", ":8ball: Don't count on it.", ":8ball: As I see it, Yes.", ":8ball: Never!"]))
	 
@bot.command(pass_context = True)
async def choose(ctx, choice1, choice2):
	try:
		await bot.say(random.choice([choice1, choice2]))
	except MissingRequiredArgument as error:
		traceback.print_exc()
		await bot.say("Gelieve 2 opties te geven zoals dit voorbeeld: $choose optie1 optie2, hier is de volledige error voor de Dev: `" + str(error) + "`")
	
@bot.command(pass_context = True)
@commands.has_permissions(mute_members =  True)
async def mute(ctx, member: discord.Member, time, *, reason):
    time  = int(time)
    role = discord.utils.get(member.server.roles, name='Muted')
    await bot.add_roles(member, role)
    channel = ctx.message.channel
    await bot.send_message(channel, "**:mute:| <@{}> You have been muted for:** {}\n**Reason:** {}\n**Admin/Mod:** <@{}>".format(member.id, time, reason, ctx.message.author.id))
    await asyncio.sleep("{}".format(time))
    role = discord.utils.get(member.server.roles, name='Muted')
    await bot.remove_roles(member, role)
	
@bot.command(pass_context =  True)
async def stinker(ctx, member: discord.Member):
	await bot.say("@{} is nu een stinkende aardappel zonder rechten! :potato:" .format(member))
	
@bot.command(pass_context = True)
async def unmute(ctx, member: discord.Member):
	role = discord.utils.get(member.server.roles, name='Muted')
	await bot.remove_roles(member, role)
	await bot.say("{} is unmuted!" .format(member))
		
@bot.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(name="{}'s info".format(ctx.message.server.name), description="Here's what I could find:", color=0x00ff00)
    embed.set_author(name="Server Info")
    embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.server.members))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def userinfo(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find:", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context = True)
async def say(ctx, *, bericht):
	await bot.say(bericht)
	
@bot.command(pass_context = True)
async def aardappel(ctx):
	member = ctx.message.author
	await bot.say("Hier een aardappel {} ! :potato:" .format(member))
	
@bot.command(pass_context = True)
async def fn(ctx, gebruikernaam):
	await bot.say("Deze functie is experimenteel!")
	await bot.say("Momentje alsjeblieft `API key ophalen....`")
	await asyncio.sleep(4)
	await bot.say("`Done!`")
	await bot.say("https://www.stormshield.one/pvp/stats/{}" .format(gebruikernaam))
	
@bot.command(pass_context = True)	
async def rhn(ctx):
	rollie8 = discord.utils.get(ctx.message.server.roles, name="bot")
	persoon = ctx.message.author 
	await bot.add_roles(persoon, rollie8)
	await bot.say("rhn done `No exception has occured`")
	print ("done")
	

	

bot.run(os.getenv('NDQyNDEwMDI5MTQ5MTkyMTky.Dit-HQ.cUB6QJs_H9z8_Zve6Mub2QF5ucA'))
