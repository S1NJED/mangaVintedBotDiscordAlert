import discord, os, dotenv, asyncio
from discord.ext import commands, tasks
from vinted_notifier.notifier import VintedNotifier

class Bot(commands.Bot):
    
    def __init__(self):
        self.alerts = []
        self.delay = 30
        super().__init__(command_prefix="$", intents=discord.Intents.all()) # TODO: specify some intents mais la g la flemme
     
        
    async def setup_hook(self):
        
        try:
            for file in os.listdir("./cogs"):
                try:
                    if file.endswith('.py'):
                        file = file.removesuffix('.py')
                        await self.load_extension("cogs." + file)
                        print(f"Sucessfully added {file} cog")
                except Exception as err:
                    raise err
        except Exception as err:
            raise err

        self.checkingStock.start()
        
        try:
            await self.tree.sync()
            print("Sucessfully sync commands")
        except:
            print("Failed to sync commands")
    
    async def on_ready(self):
        await self.change_presence(status=discord.Status.idle)
        print("Bot is active!")

    @tasks.loop(seconds=30)
    async def checkingStock(self):
        alert: VintedNotifier
        for alert in self.alerts:
            await alert.checkNewestItems()
            await asyncio.sleep(3)
            

    @checkingStock.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("Make sure to add your discord bot token to the .env file like (Example: TOKEN=Nzsadjpzajeoze...)")

bot = Bot()
bot.run(token=TOKEN)