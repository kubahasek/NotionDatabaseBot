from code import InteractiveInterpreter
from discord import SelectOption
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.ext import commands
import nextcord
import logging
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import utils.info as info
import utils.utilities as utils

class Announcements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="academymessage", description="Sends a message to the Academy Channel", guild_ids=[int(info.f1abeezID), int(info.testServerID)])
    async def academyMSG(self, interaction: Interaction):
        roles = interaction.user.roles
        rolesToFind = ["Admin", "Moderator", "Trialist Manager"]
        await interaction.response.send_message(f"Working on it...")
        if(utils.check_roles(roles, rolesToFind)):
            await interaction.delete_original_message()
            academyID = info.get_roleID(interaction.guild.id, "academyRole")
            await interaction.send(f"<@&{academyID}>\n**TRIAL RACE BRIEFING:**\nWelcome to the F1ABEEZ trial race! I would just like to run through what is expected of you from your trial:\n- Please drive clean - we are a clean racing league, show respect to your fellow drivers! dirty driving will not be tolerated\n- Drive fast! It's still a race after all, we would like to see a true reflection of your pace\n- Do not use medium tyres in Qualifying for this trial race, as this lets us compare your quali pace!\n- Have fun! That's what we're all here for\n\nThe format is short qualifying, 25% race\nAfter the race is completed, one of the trialist leaders will DM you individually with their decision\nPlease react with a thumbs up once you have read this, good luck!")
            last = interaction.channel.last_message_id
            msg = await interaction.channel.fetch_message(int(last))
            await msg.add_reaction("👍")
        else:
            await interaction.delete_original_message()
            await interaction.send("You do not have permission to use this command!")

    @nextcord.slash_command(name="stewardsdecisions", description="Sends the stewards decisions message", guild_ids=[int(info.f1abeezID), int(info.f2abeezID), int(info.testServerID)])
    async def stewardDecisions(self, interaction: Interaction, round: int = SlashOption(name="round", description="Enter the round number")):
        await interaction.response.send_message(f"Working on it...")
        if(utils.check_roles(interaction.user.roles, ["Admin", "Moderator", "Steward"])):
            channel = self.bot.get_channel(info.get_channelID(interaction.guild.id, "stewardsAnnouncementChannel"))
            roundNO = int(round)
            round = f"r{roundNO}"
            tier1URL = f"<https://f1abeez.com/race-reports/t1/{round}>"
            tier2URL = f"<https://f1abeez.com/race-reports/t2/{round}>"
            tier3URL = f"<https://f1abeez.com/race-reports/t3/{round}>"
            tier4URL = f"<https://f1abeez.com/race-reports/t4/{round}>"
            tier5URL = f"<https://f1abeez.com/race-reports/t5/{round}>"
            tierMURL = f"<https://f1abeez.com/race-reports/tm/{round}>"
            tierNAURL = f"<https://f1abeez.com/race-reports/tna/{round}>"
            f2Tier1URL = f"" ## TODO: add URL
            f2Tier2URL = f"" ## TODO: add URL
            
            if(type(channel) != type(None)):
                if(interaction.guild.id == int(info.f1abeezID)):
                    await interaction.delete_original_message()
                    await channel.send(f"🦺 @everyone\n\n**All Stewards decisions are finalised**\nPlease check this week's race-report for all the incidents reported and decisions made.\n\n**F1 - Tier 1** - {tier1URL}\n**F1 - Tier 2** - {tier2URL}\n**F1 - Tier 3** - {tier3URL}\n\n**F1 - Tier 4** - {tier4URL}\n\n**F1 - Tier 5** - {tier5URL}\n\n**F1 - Tier M** - {tierMURL}\n\n**F1 - Tier NA** - {tierNAURL}\n\nPlease file your appeals with the correct case number **in the next 24 hours**, and standings will be posted after all appeals are finalised \nFollow the instructions in <#864999507238322186> to submit your appeals \n\nThank you,\nStewards of F1ABEEZ")
                    await interaction.send("Sent the message")
                elif(interaction.guild.id == int(info.f2abeezID)):
                    await interaction.delete_original_message()
                    await channel.send(f"🦺 @everyone\n\n**All Stewards decisions are finalised**\nPlease check this week's race-report for all the incidents reported and decisions made.\n\n**F2 - Tier 1** - {f2Tier1URL}\n**F2 - Tier 2** - {f2Tier2URL}\n\nThank You,\nStewards of F2ABEEZ.")
                    await interaction.send("Sent the message")
            else:
                await interaction.delete_original_message()
                logging.error("stewardsAnnouncementChannel not found")
                await interaction.send("ERROR: stewardsAnnouncementChannel not found, contact KubaH04")
        else:
            await interaction.delete_original_message()
            await interaction.send("You do not have permission to use this command!")

    @nextcord.slash_command(name="racereport", description="Sends the race report message.", guild_ids=[int(info.f1abeezID), int(info.f2abeezID), int(info.testServerID)])
    async def raceReport(self, interaction: Interaction, round: int = SlashOption(name="round", description="Enter the round number")):
        await interaction.response.send_message(f"Working on it...")
        if(utils.check_roles(interaction.user.roles, ["Admin", "Moderator", "Steward"])):
            channel = self.bot.get_channel(info.get_channelID(interaction.guild.id, "generalAnnoucementChannel"))
            roundNO = int(round)
            # f2RoundNO = roundNO - 1
            # f2round = f"R{f2RoundNO}"
            round = f"r{roundNO}"
            tier1URL = f"<https://f1abeez.com/race-reports/t1/{round}>"
            tier2URL = f"<https://f1abeez.com/race-reports/t2/{round}>"
            tier3URL = f"<https://f1abeez.com/race-reports/t3/{round}>"
            tier4URL = f"<https://f1abeez.com/race-reports/t4/{round}>"
            tier5URL = f"<https://f1abeez.com/race-reports/t5/{round}>"
            tierMURL = f"<https://f1abeez.com/race-reports/tm/{round}>"
            tierNAURL = f"<https://f1abeez.com/race-reports/tna/{round}>"
            f2Tier1URL = f"" ## TODO: add URL
            f2Tier2URL = f"" ## TODO: add URL
            if(type(channel) != type(None)):
                if(interaction.guild.id == int(info.f1abeezID)):
                    await interaction.delete_original_message()
                    await channel.send(f"@everyone\n\n**Race Reports have now been published**\n\n**F1 - Tier 1** - {tier1URL}\n**F1 - Tier 2** - {tier2URL}\n**F1 - Tier 3** - {tier3URL}\n**F1 - Tier 4** - {tier4URL}\n**F1 - Tier 5** - {tier5URL}\n**F1 - Tier M** - {tierMURL}\n**F1 - Tier NA** - {tierNAURL}\n\nThank you,\nStewards of F1ABEEZ")
                    await interaction.send("Sent the message")
                elif(interaction.guild.id == int(info.f2abeezID)):
                    await interaction.delete_original_message()
                    await channel.send(f"@everyone\n\n**F2 - Tier 1** - {f2Tier1URL}\n**F2 - Tier 2** - {f2Tier2URL}\n\nThank you,\nStewards of F2ABEEZ")
                    await interaction.send("Sent the message")
            else:
                await interaction.delete_original_message()
                logging.error("generalAnnoucementChannel not found", exc_info=True)
                await interaction.send("ERROR: generalAnnoucementChannel not found, contact KubaH04")
        else:
            await interaction.delete_original_message()
            await interaction.send("You do not have permission to use this command!")

def setup(bot):
    bot.add_cog(Announcements(bot))