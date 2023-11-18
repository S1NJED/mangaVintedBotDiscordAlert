import discord, logging, os
from discord.ext.commands import Bot, Cog
from discord import app_commands, Interaction
from vinted_notifier.notifier import VintedNotifier
from vinted_notifier.country_codes import CountryCodes
from typing import Literal

filename = "error.log"
logging.basicConfig(filename=os.path.join(os.getcwd(), filename), level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class CreateAlertCog(Cog):
    
    def __init__(self, bot: Bot):
        self.bot = bot
    
    def isAlertExist(self, search_text: str) -> bool:
        alert: VintedNotifier
        for alert in self.bot.alerts:
            if search_text.lower() == alert.search_text.lower():
                return True
        return False
        
    
    @app_commands.command(name="create_alert", description="Get notified when new articles is on posted on vinted!")
    async def create_alert(self, interaction: Interaction, channel: discord.TextChannel, name: str, country_code: Literal["FR", "IT"] = None):
        if self.isAlertExist(name):
            return await interaction.response.send_message(f"An alert with the name `{name}` already exist.", ephemeral=True)

        await interaction.response.defer()
        
        try:
            alert = VintedNotifier(
                search_text=name,
                items_per_page=6,
                bot=self.bot,
                channel=channel,
                country_code=country_code
            )
            
            self.bot.alerts.append(alert)
            await interaction.followup.send(f"Sucessfully added an alert for the `{name}` search on Vinted !")
        except Exception as err:
            await interaction.followup.send(f"Failed to add an alert for the `{name}` search, check `'error.log'` file for more", ephemeral=True)
            logging.error(err)


    @app_commands.command(name="get_alerts", description="Get all existing alerts.")
    async def get_alerts(self, interaction: Interaction):
        if not len(self.bot.alerts):
            return await interaction.response.send_message("There is no alerts for the moment.", ephemeral=True)
        
        msg = f"{interaction.user.mention}\n\n"
        
        alert: VintedNotifier
        for i, alert in enumerate(self.bot.alerts):
            msg += f"## \#Alert `{i}`: \n> '{alert.search_text}'\n\n" # add full custom later
        
        msg += "\n *NB: the index is the number of the alert*"
        await interaction.response.send_message(msg)

    
    @app_commands.command(name="delete_alert", description="Delete an existing alert by providing his index, /get_alerts to get the index")
    async def delete_alert(self, interaction: Interaction, alert_index: int):
        if not len(self.bot.alerts):
            return await interaction.response.send_message("There is no alerts to delete for the moment.") 
        
        if alert_index > len(self.bot.alerts):
            return await interaction.response.send_message("You provided an index higher than the lenght of the alerts, use /get_alerts to see your currents alerts")
        
        try:
            del self.bot.alerts[alert_index]
            await interaction.response.send_message(f"Sucessfully deleted the {alert_index} alert.")
        except Exception as err:
            await interaction.response.send_message(f"Failed to remove {alert_index} alert, check the error.log file to see more", ephemeral=True)
            logging.error(err)

    

    @app_commands.command(name="get_loop_interval", description="Get the current value of the loop interval")
    async def get_loop_interval(self, interaction: Interaction):
        await interaction.response.send_message(f"Loop interval = {self.bot.delay} seconds")

    @app_commands.command(name="edit_loop_interval", description="Edit the delay of the loop that check")
    async def edit_loop_interval(self, interaction: Interaction, delay: int):
        try:
            self.bot.checkingStock.change_interval(seconds=delay)
            await interaction.response.send_message(f"Sucessfully changed delay from {self.bot.delay}s to {delay}s")
            self.bot.delay = delay
        except Exception as err:
            await interaction.response.send_message("Failed to change delay, error logged in `error.log` file")
            logging.error(err)
        
    
async def setup(bot: Bot):
    await bot.add_cog(CreateAlertCog(bot))        