from discord.ext.commands import Bot, Cog
from discord import app_commands, Interaction

class CogsCog(Cog):
    
    def __init__(self, bot: Bot):
        self.bot = bot
    
    
    @app_commands.command(name="reload_cog", description="reload_cog")
    async def reload_cog(self, interaction: Interaction, cog_name: str):
        try:
            await self.bot.reload_extension(cog_name)
            await interaction.response.send_message(f"Sucessfully reloaded {cog_name} cog")
        except:
            await interaction.response.send_message(f"Failed to reload {cog_name} cog, make sure to enter the good cog name ")


async def setup(bot: Bot):
    await bot.add_cog(CogsCog(bot))
            
