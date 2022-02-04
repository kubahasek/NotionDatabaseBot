import asyncio
from discord import SlashOption
import nextcord
from nextcord import client
from nextcord import message
from nextcord.colour import Color
from nextcord.ext import tasks, commands
from nextcord.ext.commands import CommandNotFound
from nextcord.ext.commands.core import check
from nextcord.ui import view
from nextcord.ui.view import View
import requests
import datetime
import pytz
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import utils.notion as nt
import utils.info as info
import utils.utilities as utils
import logging
from nextcord import Interaction, Member
import cogs.Lobby as Lobby

logging.basicConfig(format='%(asctime)s-%(levelname)s:%(message)s', level=logging.INFO)


class TierDropdown(nextcord.ui.Select):
  def __init__(self):
    options = [
      nextcord.SelectOption(label="Tier 1",description="F1 - Tier 1" ,value="F1 - Tier 1"),
      nextcord.SelectOption(label="Tier 2",description="F1 - Tier 2" ,value="F1 - Tier 2"),
      nextcord.SelectOption(label="Tier 3",description="F1 - Tier 3" ,value="F1 - Tier 3"),
      # nextcord.SelectOption(label="Tier 4",description="F1 - Tier 4" ,value="F1 - Tier 4"),
      # nextcord.SelectOption(label="Tier 5",description="F1 - Tier 5" ,value="F1 - Tier 5"),
      # nextcord.SelectOption(label="Tier M",description="F1 - Tier M" ,value="F1 - Tier M"),
      # nextcord.SelectOption(label="Tier NA",description="F1 - Tier NA" ,value="F1 - Tier NA"),
      # nextcord.SelectOption(label="F2 - Tier 1",description="F2 - Tier 1" ,value="F2 - Tier 1"),
      # nextcord.SelectOption(label="F2 - Tier 2",description="F2 - Tier 2" ,value="F2 - Tier 2"),
    ]
    super().__init__(placeholder="Select your tier...", min_values=1, max_values=1, options=options)

  async def callback(self, interaction: nextcord.Interaction):
    self.tierSelected = self.values[0]
class DropdownTierView(nextcord.ui.View):
  def __init__(self):
    super().__init__()
    self.dropdown = TierDropdown()
    self.add_item(self.dropdown)

  @nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.green, row=1)
  async def confirm(self,button: nextcord.ui.Button, interaction: nextcord.Interaction):
    self.tierSelected = self.dropdown.tierSelected
    self.stop()

class SuggestionMenu(nextcord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  
  async def handle_click(self, button, interaction):
    if(str(button.custom_id) == "Yes"):
      self.anonymous = True
      self.stop()
    elif(str(button.custom_id) == "No"):
      self.anonymous = False
      self.stop()

  @nextcord.ui.button(label="Yes", style=nextcord.ButtonStyle.primary, custom_id="Yes")
  async def yesClicked(self, button, interaction):
    await self.handle_click(button, interaction)
  
  @nextcord.ui.button(label="No", style=nextcord.ButtonStyle.primary, custom_id="No")
  async def noClicked(self, button, interaction):
    await self.handle_click(button, interaction)


class CalendarMenu(nextcord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  
  async def handle_click(self, button, interaction):
    if(str(button.custom_id) == "F1"):
      self.tierSelected = "F1"
      self.stop()
    elif(str(button.custom_id) == "Nations_League"):
      self.tierSelected = "Nations League"
      self.stop()

  @nextcord.ui.button(label="F1", style=nextcord.ButtonStyle.primary, custom_id="F1")
  async def tier1ButtonClicked(self, button, interaction):
    await self.handle_click(button, interaction)
  
  # @nextcord.ui.button(label="Nations League", style=nextcord.ButtonStyle.primary, custom_id="Nations_League")
  # async def tier2ButtonClicked(self, button, interaction):
  #   await self.handle_click(button, interaction)

class reportMenu(nextcord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  async def handle_click(self, button, interaction):
    user = interaction.user
    channel = interaction.channel
    if(interaction.channel_id == info.get_channelID(interaction.guild_id, "incidentReportChannel")):
      bst = pytz.timezone("Europe/London")
      todayInc = datetime.datetime.now(tz=bst).isoformat()
      def check(m):
        return m.author == user and m.guild is None 

      def checkRaw(u):
        return u.user_id == user.id and u.guild_id is None
      
      await interaction.response.send_message(f"Please follow the bot to your DMs to report your incident {user.mention}", ephemeral=True)

      try:
          await user.send("What is your gamertag?")
          gamertagOfUserInc = await bot.wait_for("message", check=check, timeout=180.0)
          gamertagOfUserInc = gamertagOfUserInc.content
          await user.send("Please describe your incident.")
          descriptionInc = await bot.wait_for("message", check=check, timeout=180.0)
          descriptionInc = descriptionInc.content

          view = DropdownTierView()
          await user.send("Select in which tier did the incident occur", view=view)
          await view.wait()
          if(view.tierSelected == "F1 - Tier 1"):
            tierOfIncidentInc = view.tierSelected
            await user.send(f"You selected {tierOfIncidentInc}")
          elif(view.tierSelected == "F1 - Tier 2"):
            tierOfIncidentInc = view.tierSelected
            await user.send(f"You selected {tierOfIncidentInc}")
          elif(view.tierSelected == "F1 - Tier 3"):
            tierOfIncidentInc = view.tierSelected
            await user.send(f"You selected {tierOfIncidentInc}")
          elif(view.tierSelected == "F1 - Tier 4"):
            tierOfIncidentInc = view.tierSelected
            await user.send(f"You selected {tierOfIncidentInc}")
          elif(view.tierSelected == "F1 - Tier 5"):
            tierOfIncidentInc = view.tierSelected
            await user.send(f"You selected {tierOfIncidentInc}")
          elif(view.tierSelected == "F1 - Tier M"):
            tierOfIncidentInc = view.tierSelected
            await user.send(f"You selected {tierOfIncidentInc}")
          elif(view.tierSelected == "F1 - Tier NA"):
            tierOfIncidentInc = view.tierSelected
            await user.send(f"You selected {tierOfIncidentInc}")
          elif(view.tierSelected == "F2 - Tier 1"):
            tierOfIncidentInc = view.tierSelected
            await user.send(f"You selected {tierOfIncidentInc}")
          elif(view.tierSelected == "F2 - Tier 2"):
            tierOfIncidentInc = view.tierSelected
            await user.send(f"You selected {tierOfIncidentInc}")
          
          await user.send("Please provide video evidence (Only reply with links to gamerdvr or other services)")
          evidenceInc = await bot.wait_for("message", check=check, timeout=180.0)
          evidenceInc = evidenceInc.content
          await user.send("What lap did this incident/penalty occur on?")
          lapOfIncidentInc = await bot.wait_for("message", check=check, timeout=180.0)
          lapOfIncidentInc = lapOfIncidentInc.content
          await user.send("What is the gamertag(s) of the driver(s) involved? (For penalties, reply with N/A)")
          gamertagOfInvolevedDriverInc = await bot.wait_for("message", check=check, timeout=180.0)
          gamertagOfInvolevedDriverInc = gamertagOfInvolevedDriverInc.content
          response = nt.submitAnIncident(gamertagOfUserInc, lapOfIncidentInc, descriptionInc, tierOfIncidentInc, evidenceInc, gamertagOfInvolevedDriverInc, todayInc)
          logEmbed = nextcord.Embed(title="⚠️New Ticket has been reported!⚠️")
          logEmbed.add_field(name="Tier", value=tierOfIncidentInc, inline=False)
          logEmbed.add_field(name="Drivers involved", value=f"{gamertagOfUserInc} vs {gamertagOfInvolevedDriverInc}", inline=False)
          channel = bot.get_channel(info.get_channelID(interaction.guild_id, "incidentLogChannel"))
          await channel.send(embed = logEmbed)
          await user.send(response)
      except asyncio.TimeoutError:
          await user.send("Unfortunately you took too long to reply (Limit is three minutes per message). Please start a new incident if you want to proceed.")
      except Exception as e:
        print("incident report:")
        print(e)
      


    if(interaction.channel.id == info.get_channelID(interaction.guild_id, "appealReportChannel")):
      bst = pytz.timezone("Europe/London")
      todayApp = datetime.datetime.now(tz=bst).isoformat()
      def check(m):
        return m.author == user and m.guild is None 
        
      await interaction.response.send_message(f"Please follow the bot to your DMs to submit your appeal {user.mention}", ephemeral=True)
      try:
          await user.send("What is the case number you want to appeal (use ;gettickets in the bot channel in the server if you need to get it)")
          caseNumberApp = await bot.wait_for("message", check=check, timeout=180.0)
          caseNumberApp = caseNumberApp.content
          await user.send("What is your gamertag?")
          gamertagOfUserApp = await bot.wait_for("message", check=check, timeout=180.0)
          gamertagOfUserApp = gamertagOfUserApp.content
          await user.send("Please state the reason for you appeal.")
          reasonApp = await bot.wait_for("message", check=check, timeout=180.0)
          reasonApp = reasonApp.content
          await user.send("State any additional information to support your appeal (if you don't have any, reply with N/A)")
          additionalInfoApp = await bot.wait_for("message", check=check, timeout=180.0)
          additionalInfoApp = additionalInfoApp.content
          await user.send("Please provide addition video evidence to support your appeal (Only reply with links to gamerdvr or other services)")
          evidenceApp = await bot.wait_for("message", check=check, timeout=180.0)
          evidenceApp = evidenceApp.content
          await user.send("What is the gamertag(s) of the driver(s) involved? (For penalties, reply with N/A)")
          gamertagOfInvolevedDriverApp = await bot.wait_for("message", check=check, timeout=180.0)
          gamertagOfInvolevedDriverApp = gamertagOfInvolevedDriverApp.content
          response = nt.submitAppeal(caseNumberApp, evidenceApp, gamertagOfUserApp, gamertagOfInvolevedDriverApp, reasonApp, additionalInfoApp, todayApp)
          logEmbed = nextcord.Embed(title="⚠️New Appeal has been submitted!⚠️")
          logEmbed.add_field(name="Case Number", value=caseNumberApp, inline=False)
          logEmbed.add_field(name="Drivers involved", value=f"{gamertagOfUserApp} vs {gamertagOfInvolevedDriverApp}", inline=False)
          channel = bot.get_channel(info.get_channelID(interaction.guild_id, "incidentLogChannel"))
          await channel.send(embed = logEmbed)
          await user.send(response)
      except asyncio.TimeoutError:
          await user.send("Unfortunately you took too long to reply (Limit is a three minutes per message). Please start a new incident if you want to proceed.")
      except Exception as e:
        print("Appeal:")
        print(e)
      


    if(interaction.channel.id == info.get_channelID(interaction.guild_id, "suggestionSubmitChannel")):
      def check(m):
        return m.author == user and m.guild is None 
      try:      
        await interaction.response.send_message(f"Please follow the bot to your DMs! {user.mention}", ephemeral=True)
        await user.send("Please type your suggestion here, the admins will have a look at it as soon as possible. Thank you, Admins of F1ABEEZ")
        suggestion = await bot.wait_for("message", check=check, timeout=300.0)
        suggestion = suggestion.content
        view = SuggestionMenu()
        await user.send("Do you wish to stay anonymous?", view=view)
        await view.wait()
      except asyncio.TimeoutError:
        await user.send("Unfortunately you took too long. The limit is 5 minutes per message")
      except Exception as e:
        print("suggestion:")
        print(e)

      suggestionLogEmbed = nextcord.Embed(title="🚨A new suggestion has been submitted🚨")
      if(view.anonymous == False):
        suggestionLogEmbed.add_field(name="**Submitted by:**", value=user.display_name, inline=False)
      suggestionLogEmbed.add_field(name="**Suggestion**", value=suggestion, inline=False)
      channel = bot.get_channel(info.get_channelID(interaction.guild_id, "suggestionLogChannel"))
      await channel.send(embed = suggestionLogEmbed)
      await user.send("Your suggestion has been submitted to the admins!")

  @nextcord.ui.button(label="", emoji="📨", style=nextcord.ButtonStyle.primary, custom_id="id")
  async def reportButtonClicked(self, button, interaction):
    await self.handle_click(button, interaction)


def GetHelpCommand():
    embed = nextcord.Embed(title="Help", color=info.color)
    embed.add_field(name=";standings", value="This command gives you a menu to select the tier of which you want to see standings and then it returns them in the channel.", inline=False)
    embed.add_field(name=";calendar", value="This command gives you a selection of the F1 or Nations League calendar and then sends it in the channel.", inline=False)
    embed.add_field(name=";gettickets <gamertag>", value="This command is useful when you don’t know the number of your ticket. The command lists all tickets you’ve been involved (whether you reported it or someone else reported you) and gives you the number of the ticket and the direct link to the website.", inline=False)
    embed.add_field(name=";getappeals <gamertag>", value="This command gets you a list of appeals you've been involeved in (whether you appealed or someone appealed against you) and gives you the number of the appeal, a direct link to the website and the status of the appeal.")
    embed.add_field(name=";ticketdetail <number of ticket>", value="This command gets you the details of ticket you provide. It lists the status, penalty that was awarded and who was involved.", inline=False)
    embed.add_field(name=";incidentreport", value="This command allows you to submit an incident from nextcord. Please read the messages carefully and reply correctly.", inline=False)
    embed.add_field(name=";submitappeal", value="This command allows you to submit an appeal to a decision that has been made by the stewards. Please use ;gettickets before you start submitting it to make sure you know the case number of the incident you want to appeal", inline=False)
    return embed

def getStaffHelpCommand():
  embed = nextcord.Embed(title="Staff Help", color=info.color)
  embed.add_field(name=";lobbytier<tierNumber>", value="Sends the lobby is open message. Enter the tier number instead of <tierNumber>. Options: [1,2,3,4,5,M,NA]", inline=False)
  embed.add_field(name=";readytier<tierNumber>", value="Sends the ready up instruction. Enter the tier number instead of <tierNumber>. Options: [1,2,3,4,5,M,NA]", inline=False)
  embed.add_field(name=";racetier<tierNumber>", value="Sends the race ready up instruction. Enter the tier number instead of <tierNumber>. Options: [1,2,3,4,5,M,NA]", inline=False)
  embed.add_field(name=";lobbyf2tier<tierNumber>", value="Sends the lobby is open message. Enter the tier number instead of <tierNumber>. Options: [1,2]")
  embed.add_field(name=";readyf2tier<tierNumber>", value="Sends the ready up instruction. Enter the tier number instead of <tierNumber>. Options: [1,2]")
  embed.add_field(name=";racef2tier<tierNumber>", value="Sends the race ready up instruction. Enter the tier number instead of <tierNumber>. Options: [1,2]")
  embed.add_field(name=";stewardsdecision <roundNumber>", value="Send the links to respective tier race reports. Enter round number instead of <roundNumber>", inline=False)
  embed.add_field(name=";academymessage", value="Send the academy info message", inline=False)
  embed.add_field(name=";warn <user> <reason>", value="(ADMIN ONLY) - allows to warn a user, sending the warning into the proper channel to keep track.")
  embed.add_field(name=";ban <user> <reason>", value="(ADMIN ONLY) - allows to ban a user, and automatically sends it into the ban channel.", inline=False)
  embed.add_field(name=";racereport <roundNumber>", value="Send the links to respective tier race reports. Enter round number instead of <roundNumber>", inline=False)
  embed.add_field(name=";channelname", value="Provide the channel name separated by - (e.g. this-is-a-channel) and the bot will return the name in the special font", inline=False)
  return embed

def dotdMessageFun(str):
  tier = str[0]
  driver1 = str[1]
  driver1PosChange = str[2]
  driver2 = str[3]
  driver2PosChange = str[4]
  driver3 = str[5]
  driver3PosChange = str[6]
  driver4 = str[7]
  driver4PosChange = str[8]
  driver5 = str[9]
  driver5PosChange = str[10]
  if(tier == "Tier 1"):
    return(f"<@&{info.tier1Role}>\n\n**Tier 1 Driver of The Day poll:**\n\n1️⃣ - {driver1} - {driver1PosChange}\n2️⃣ - {driver2} - {driver2PosChange}\n3️⃣ - {driver3} - {driver3PosChange}\n4️⃣ - {driver4} - {driver4PosChange}\n5️⃣ - {driver5} - {driver5PosChange}")
  elif(tier == "Tier 2"):
    return(f"<@&{info.tier2Role}>\n\n**Tier 2 Driver of The Day poll:**\n\n1️⃣ - {driver1} - {driver1PosChange}\n2️⃣ - {driver2} - {driver2PosChange}\n3️⃣ - {driver3} - {driver3PosChange}\n4️⃣ - {driver4} - {driver4PosChange}\n5️⃣ - {driver5} - {driver5PosChange}")
  elif(tier == "Tier 3"):
    return(f"<@&{info.tier3Role}>\n\n**Tier 3 Driver of The Day poll:**\n\n1️⃣ - {driver1} - {driver1PosChange}\n2️⃣ - {driver2} - {driver2PosChange}\n3️⃣ - {driver3} - {driver3PosChange}\n4️⃣ - {driver4} - {driver4PosChange}\n5️⃣ - {driver5} - {driver5PosChange}")
  elif(tier == "Tier 4"):
    return(f"<@&{info.tierMRole}>\n\n**Tier 4 Driver of The Day poll:**\n\n1️⃣ - {driver1} - {driver1PosChange}\n2️⃣ - {driver2} - {driver2PosChange}\n3️⃣ - {driver3} - {driver3PosChange}\n4️⃣ - {driver4} - {driver4PosChange}\n5️⃣ - {driver5} - {driver5PosChange}")
  elif(tier == "NL"):
    return(f"<@&{info.nationsLeagueRole}>\n\n**Tier 4 Driver of The Day poll:**\n\n1️⃣ - {driver1} - {driver1PosChange}\n2️⃣ - {driver2} - {driver2PosChange}\n3️⃣ - {driver3} - {driver3PosChange}\n4️⃣ - {driver4} - {driver4PosChange}\n5️⃣ - {driver5} - {driver5PosChange}")
  
def dotdWinnerMsg(tier, driver):
  if(tier == "Tier 1"):
    return(f"<@&{info.tier1Role}>\n\n**Tier 1 Driver of The Day:**\n\n{driver}\n\nCongratulations!")
  elif(tier == "Tier 2"):
    return(f"<@&{info.tier2Role}>\n\n**Tier 2 Driver of The Day:**\n\n{driver}\n\nCongratulations!")
  elif(tier == "Tier 3"):
    return(f"<@&{info.tier3Role}>\n\n**Tier 3 Driver of The Day:**\n\n{driver}\n\nCongratulations!")
  elif(tier == "Tier 4"):
    return(f"<@&{info.tierMRole}>\n\n**Tier 2 Driver of The Day:**\n\n{driver}\n\nCongratulations!")
  elif(tier == "NL"):
    return(f"<@&{info.nationsLeagueRole}>\n\n**Tier 2 Driver of The Day:**\n\n{driver}\n\nCongratulations!")


intents = nextcord.Intents.default()
intents.reactions = True
intents.members = True
bot = commands.Bot(command_prefix=";", help_command=None, intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    logging.info("We have logged in as {0.user}".format(bot))
    bot.add_view(reportMenu())
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="F1ABEEZ Server 🚀"))

@bot.slash_command(name="help", description="Shows the help menu", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
async def HelpCommand(interaction: Interaction):
    await interaction.send(embed = GetHelpCommand())

@bot.slash_command(name="staffhelp", description="Shows the staff help menu", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
async def StaffHelpCommand(interaction: Interaction):
  await interaction.response.defer()
  if(utils.check_roles(interaction.user.roles, ["Staff"])):
    await interaction.send(embed = getStaffHelpCommand())
  else:
    await interaction.send("You do not have permission to use this command!")

@bot.slash_command(name="gettickets", description="Gets the tickets for the gamertag", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
async def GetTickets(interaction: Interaction, gamertag: str = SlashOption(name="gamertag", description="The gamertag to get the tickets for", required=True)):
    await interaction.response.defer()
    await interaction.send(embed=nt.queryTickets(gamertag))

@bot.slash_command(name="getprofile", description="Gets profile info from the database", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
async def GetProfile(interaction: Interaction, gamertag: str = SlashOption(name="gamertag", description="The gamertag to get the tickets for", required=True)):
    await interaction.response.defer()
    await interaction.send(embed=nt.getProfileInfo(gamertag))    

@bot.slash_command(name="getappeals", description="Gets the appeals for the gamertag", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
async def GetAppeals(interaction: Interaction, gamertag: str = SlashOption(name="gamertag", description="The gamertag to get the tickets for", required=True)):
  await interaction.response.defer()
  await interaction.send(embed = nt.queryAppeals(gamertag))

@bot.slash_command(name="ticketdetail", description="Gets the details for the ticket", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
async def TicketDetail(interaction: Interaction, ticketID: str = SlashOption(name="ticketid", description="The ticket ID to get the details for", required=True)):
    await interaction.response.defer()
    await interaction.send(embed = nt.TicketDetailQuery(ticketID))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("Command not found")
    logging.error(error)

@bot.slash_command(name="warn", description="Warns a user", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
@commands.has_any_role("Admin")
async def warn(interaction: Interaction, user: Member = SlashOption(name="user", description="The user to warn", required=True), reason: str = SlashOption(name="reason", description="The reason for the warning", required=True)):

  await interaction.response.defer()
  member = await interaction.guild.fetch_member(user.id)

  embed = nextcord.Embed(title="A Warning has been issued", color=info.color)
  embed.add_field(name="User", value=member.name, inline=False)
  embed.add_field(name="Reason", value=reason, inline=False)
  channel = bot.get_channel(info.get_channelID(interaction.guild.id, "warningChannel"))
  await channel.send(embed = embed)
  await interaction.send(embed = embed)   

@bot.command(name="ban")
@commands.has_any_role("Admin")
async def ban(ctx, user=None, *, reason=None):
  if(user is None):
    await ctx.send("You didn't mention the user")
    return
  if(reason is None):
    await ctx.send("You didn't provide a reason")
    return

  try: 
    member = ctx.message.mentions[0]
    membername = ctx.message.mentions[0].name
  except IndexError:
    print(user)
    member = await ctx.guild.fetch_member(int(user))
    print(member)
    membername = member.name
  except Exception as e:
    print("ban:")
    print(e)

  embed = nextcord.Embed(title="A Ban has been issued", color=info.color)
  embed.add_field(name="User", value=membername, inline=False)
  embed.add_field(name="Reason", value=reason, inline=False)
  channel = bot.get_channel(info.get_channelID(ctx.guild.id, "banChannel"))
  await channel.send(embed = embed)
  await member.ban(reason = reason)
  await ctx.send(embed = embed)   
    
@bot.event
async def on_member_join(member):
  serverID = member.guild.id
  if(member.guild.id == int(info.f1abeezID)):
    role = nextcord.utils.get(member.guild.roles, name="Academy Driver")
    await member.add_roles(role)
  elif(member.guild.id == int(info.f2abeezID)):
    role = nextcord.utils.get(member.guild.roles, name="Member")
    await member.add_roles(role)
  channel = bot.get_channel(info.get_channelID(serverID, "welcomeChannel"))
  if(type(channel) != type(None)):
    if(member.guild.id == int(info.f1abeezID)):
      await channel.send(f"**Welcome {member.mention}**\n\nPlease use this chat if you have any questions and someone will be on hand.\n\nAll the information you need is on <#865379267977412618>")
    elif(member.guild.id == int(info.f2abeezID)):
      await channel.send(f"Welcome to F2ABEEZ!{member.mention}\n\nYour dedicated F2 racing discord community. Please read <#937998062842957824> to get equated with our brand and information then, head over to <#937997355737833482> to get a seat in the next race that suits your pace!")
  else:
    logging.error("welcomeChannel not found")

@bot.event
async def on_member_remove(member):
  memberName = member.name
  channel = bot.get_channel(info.get_channelID(member.guild.id, "leavingChannel"))
  if(type(channel) != type(None)):
    await channel.send(f"**{memberName}** has left the server.")
  else:
    logging.error("leavingChannel not found", exc_info=True)

@bot.command(name="incidentchannel")
@commands.has_any_role("Admin", "Moderator")
async def incidentChannel(ctx):
  await ctx.message.delete()
  embed = nextcord.Embed(title="Report an incident",description="React to this message to report an incident by clicking the 📨 button", color=info.color)
  await ctx.send(embed=embed, view=reportMenu())
  # msg = await ctx.send(embed = embed)
  # await msg.add_reaction("📨")

@bot.command(name="appealchannel")
@commands.has_any_role("Admin", "Moderator")
async def appealChannel(ctx):
  await ctx.message.delete()
  embed = nextcord.Embed(title="Submit an appeal",description="React to this message to submit an appeal by clicking the 📨 button", color=info.color)
  await ctx.send(embed=embed, view=reportMenu())

@bot.command(name="suggestionchannel")
@commands.has_any_role("Admin", "Moderator")
async def suggestionChannel(ctx):
  await ctx.message.delete()
  embed = nextcord.Embed(title="Submit a suggestion",description="React to this message to submit a suggestion by clicking the 📨 button", color=info.color)
  await ctx.send(embed=embed, view=reportMenu())

@bot.command(name="calendar")
async def getCalendar(ctx):
  await ctx.message.delete()
  view = CalendarMenu()
  selectMSG = await ctx.send("For which tier do you want to see standings?", view=view)
  await view.wait()
  if(info.f1abeezID == ctx.guild.id):
    msg = await ctx.send("Getting the F1 calendar...")
    try:
      await selectMSG.delete()
      r = requests.get("https://api.figma.com/v1/images/8mL0mwOKyIUcoLG3goL7wk/?ids=2%3A138&format=png", headers={"X-Figma-Token": info.figmaToken})
      r = r.json()
      if(r):
        await msg.delete()
      img = r["images"]["2:138"]
      embed1 = nextcord.Embed(color=info.color) 
      embed1.set_image(url=img) 
      await ctx.send(embed=embed1)
    except Exception as e:
      await ctx.send(f"There was an error getting the calendar, please report this issue to the admins.")
      print("calendar:")
      print(e)
  elif(info.f2abeezID == ctx.guild.id):
    msg = await ctx.send("Getting the F2 calendar...")
    try:
      await selectMSG.delete()
      r = requests.get("https://api.figma.com/v1/images/8mL0mwOKyIUcoLG3goL7wk/?ids=15%3A2&format=png", headers={"X-Figma-Token": info.figmaToken})
      r = r.json()
      if(r):
        await msg.delete()
      img = r["images"]["15:2"] ## TODO: change this to F2 calendar
      print(img)
      embed2 = nextcord.Embed(color=info.color) 
      embed2.set_image(url=img) 
      await ctx.send(embed=embed2)
    except Exception as e:
      await ctx.send(f"There was an error getting the calendar, please report this issue to the admins.")
      print("calendar:")
      print(e)


@bot.command(name="standings")
async def getStandings(ctx):
  await ctx.message.delete()
  view = DropdownTierView()
  selectMSG = await ctx.send("For which tier do you want to see standings?", view=view)
  await view.wait()
  try:
    if(view.tierSelected == "F1 - Tier 1"):
      await selectMSG.delete()
      msg = await ctx.send("Getting Tier 1 Standings")
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=2%3A16&format=png", headers={"X-Figma-Token": info.figmaToken})
      if(r):
        await msg.delete()
      r = r.json()
      url = r["images"]["2:16"]
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
    elif(view.tierSelected == "F1 - Tier 2"):
      await selectMSG.delete()
      msg = await ctx.send("Getting Tier 2 Standings...")
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=4%3A446&format=png", headers={"X-Figma-Token": info.figmaToken})
      if(r):
        await msg.delete()
      r = r.json()
      url = r["images"]["4:446"]
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
    elif(view.tierSelected == "F1 - Tier 3"):
      await selectMSG.delete()
      msg = await ctx.send("Getting Tier 3 Standings...")
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=4%3A265&format=png", headers={"X-Figma-Token": info.figmaToken})
      if(r):
        await msg.delete()
      r = r.json()
      url = r["images"]["4:265"]
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
    elif(view.tierSelected == "F1 - Tier 4"):
      await selectMSG.delete()
      msg = await ctx.send("Getting Tier 4 Standings...")
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=4%3A351&format=png", headers={"X-Figma-Token": info.figmaToken})
      if(r):
        await msg.delete()
      r = r.json()
      url = r["images"]["4:351"] ## TODO: Change this to the correct image
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
    elif(view.tierSelected == "F1 - Tier 5"):
      await selectMSG.delete()
      msg = await ctx.send("Getting Tier 5 Standings")
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=2%3A16&format=png", headers={"X-Figma-Token": info.figmaToken})
      if(r):
        await msg.delete()
      r = r.json()
      url = r["images"]["2:16"] ## TODO: Change this to the correct image
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
    elif(view.tierSelected == "F1 - Tier M"):
      await selectMSG.delete()
      msg = await ctx.send("Getting Tier M Standings")
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=2%3A16&format=png", headers={"X-Figma-Token": info.figmaToken})
      if(r):
        await msg.delete()
      r = r.json()
      url = r["images"]["2:16"] ## TODO: Change this to the correct image
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
    elif(view.tierSelected == "F1 - Tier NA"):
      await selectMSG.delete()
      msg = await ctx.send("Getting Tier NA Standings")
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=2%3A16&format=png", headers={"X-Figma-Token": info.figmaToken})
      if(r):
        await msg.delete()
      r = r.json()
      url = r["images"]["2:16"] ## TODO: Change this to the correct image
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
    elif(view.tierSelected == "F2 - Tier 1"):
      await selectMSG.delete()
      msg = await ctx.send("Getting F2 - Tier 1 Standings")
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=2%3A16&format=png", headers={"X-Figma-Token": info.figmaToken})
      if(r):
        await msg.delete()
      r = r.json()
      url = r["images"]["2:16"] ## TODO: Change this to the correct image
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
    elif(view.tierSelected == "F2 - Tier 2"):
      await selectMSG.delete()
      msg = await ctx.send("Getting F2 - Tier 2 Standings")
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=2%3A16&format=png", headers={"X-Figma-Token": info.figmaToken})
      if(r):
        await msg.delete()
      r = r.json()
      url = r["images"]["2:16"] ## TODO: Change this to the correct image
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
  except KeyError:
    await ctx.send("There was an error while getting the standings. Please report this issue to the admins")
    print(KeyError)
  except Exception as e:
    print("standings:")
    print(e)

@bot.command("lineup")
async def getLineupLink(ctx):
  await ctx.reply("<https://www.f1abeez.com/line-ups>")

@bot.command("dotd")
@commands.has_any_role("Admin", "Moderator")
async def dotdMessage(ctx, *, args):
  await ctx.message.delete()
  try:
    arguments = str(args)
    splitStr = arguments.split(",")
    if(splitStr.__len__() == 11):
      msg = dotdMessageFun(splitStr)
      dcMSG = await ctx.send(msg)
      await dcMSG.add_reaction("1️⃣")
      await dcMSG.add_reaction("2️⃣")
      await dcMSG.add_reaction("3️⃣")   
      await dcMSG.add_reaction("4️⃣")
      await dcMSG.add_reaction("5️⃣")
    elif(splitStr.__len__() > 11):
      await ctx.author.send("Too many arguments provided, please try again")
    elif(splitStr.__len__() < 11):
      await ctx.author.send("Too few arguments provided, please try again")
  except Exception as e:
    print("dotd")
    print(e)

@bot.command("dotdwinner")
@commands.has_any_role("Admin", "Moderator")
async def dotdWinner(ctx, *, args):
  await ctx.message.delete()
  try:
    arguments = str(args)
    arguments = arguments.split(",")
    if(arguments.__len__() == 2):
      tier = arguments[0]
      driver = arguments[1]
      msg = dotdWinnerMsg(tier, driver)
      await ctx.send(msg)
    elif(arguments.__len__() > 2):
        await ctx.author.send("Too many arguments provided, please try again")
    elif(arguments.__len__() < 2):
      await ctx.author.send("Too few arguments provided, please try again")
  except Exception as e:
    print("dotdwinner:")
    print(e)

@bot.command("channelname")
@commands.has_any_role("Admin", "Moderator")
async def channelName(ctx, name):
  nameDic = {"a": "ᴀ","b": "ʙ", "c": "ᴄ", "d":  "ᴅ", "e": "ᴇ", "f":"ꜰ", "g": "ɢ", "h":"ʜ", "i":"ɪ", "j":"ᴊ", "k":"ᴋ", "l":"ʟ", "m":"ᴍ", "n": "ɴ", "o": "ᴏ", "p":"ᴘ", "q":"Q", "r":"ʀ", "s":"ꜱ", "t":"ᴛ", "u":"ᴜ", "v":"ᴠ", "w":"ᴡ", "x":"x", "y":"ʏ", "z":"ᴢ", "-":"-", "0":"0", "1":"1", "2":"2", "3":"3", "4":"4", "5":"5", "6":"6", "7":"7", "8":"8", "9":"9"}
  returnName = ""
  for i in range(len(name)):
    char = name[i].lower()
    returnName += nameDic.get(char)

  await ctx.reply("︱" + returnName)

for fn in os.listdir("./cogs"):
  if fn.endswith(".py"):
    logging.info("Loading %s", fn)
    bot.load_extension(f"cogs.{fn[:-3]}")

bot.run(info.discord_token)