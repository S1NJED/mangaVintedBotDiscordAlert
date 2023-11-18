import requests, logging, os, discord
from vinted_notifier.utils import UtilsVintedNotifier
from discord.ext.commands import Bot

filename = "error.log"
logging.basicConfig(filename=os.path.join(os.getcwd(), filename), level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class VintedNotifier(UtilsVintedNotifier):
    
    def __init__(
        self, 
        search_text,
        items_per_page,
        bot: Bot,
        channel: discord.TextChannel,
        country_code: str = None
        
    ):

        UtilsVintedNotifier.__init__(self, bot=bot)
        
        self.search_text = search_text
        self.items_per_page = items_per_page
        self.country_code = country_code
        self.channel = channel
        
        self.session = requests.Session()
        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0"
        self.session.headers = {
            "User-Agent": USER_AGENT
        }
        self.session.get("https://vinted.fr") # to get valid cookies | todo pass the session object to the constructtor to avoid getting many
        self.ITEMS: list = self.getNewestItems()

        
    async def checkNewestItems(self) -> None:
        NEWEST_ITEMS = self.getNewestItems()
        
        # to get all the newest items
        NEW_ITEM_COUNT = 0
        try:
            NEW_ITEM_COUNT = NEWEST_ITEMS.index(self.ITEMS[0])
        except ValueError:
            NEW_ITEM_COUNT = len(NEWEST_ITEMS)
        
        for index in range(NEW_ITEM_COUNT):
            current_item = list(NEWEST_ITEMS[index].values())[0]
            
            try:
                text = self.search_text.lower()
                
                if text in current_item['title'].lower() or text in current_item['description'].lower():

                    # To get only article from your country
                    if self.country_code and current_item['user']['country_code'] != self.country_code:
                        continue
                    
                    await self.sendAlert(current_item)

            except Exception as err:
                logging.error(err)
            
        self.ITEMS = NEWEST_ITEMS
    