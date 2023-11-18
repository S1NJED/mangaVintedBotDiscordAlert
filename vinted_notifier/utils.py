import discord, json
from discord.ext.commands import Bot
from math import floor
from time import sleep

class UtilsVintedNotifier:
    
    def __init__(self, bot: Bot):
        self.bot = bot
        self.countryFlags = {
            "FR": "🇫🇷",
            "IT": "🇮🇹"
        }
    
    def getUserCountryCode(
        self,
        user_id
    ) -> None | str:
        
        URL = f"https://www.vinted.fr/api/v2/users/{user_id}?localize=false"
        req = self.session.get(URL)
        
        if req.status_code < 300:
            data = req.json()
            return data['user']['country_code']
        return None


    def createUrl(self) -> str:
        
        MODEL_URL = "https://www.vinted.fr/api/v2/catalog/items?" \
        + f"page=1" \
        + f"&per_page={self.items_per_page}" \
        + f"&search_text={self.search_text}" \
        + f"&catalog_ids=2312" \
        + f"&order=newest_first" 
        
        return MODEL_URL


    def getNewestItems(self) -> list:
        
        URL = self.createUrl()
        req = self.session.get(URL)
        data = req.json()
        
        
        NEWEST_ITEMS = []
        
        for item in data['items']:
            item_id = item['id']
            item = self.getItemData(item_id)

            NEWEST_ITEMS.append(item)

        return NEWEST_ITEMS


    async def sendAlert(self, item_data) -> None:
        embed = discord.Embed(title="New item !", description="")
        
        embed.description = f"**[{item_data['title']}]({item_data['item_url']})**"
        embed.color = 1157560
        embed.set_image(url=item_data['item_photo'])
        
        embed.add_field(name="Price", value=f"{item_data['total_item_price']} {item_data['currency']} ({item_data['price']} + {item_data['service_fee']})")
        
        if item_data['user']['feedback_count']:
            embed.add_field(name="Reputation", value="⭐"*floor(item_data['user']['feedback_reputation']*5) + f"({item_data['user']['feedback_count']})")
        
        embed.set_footer(text=item_data['user']['login'] + " | " + self.countryFlags.get(item_data['user']['country_code']), icon_url=item_data['user']['pfp'])
        
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Go to", url=item_data['item_url'], style=discord.ButtonStyle.green))
        
        await self.channel.send(embed=embed, view=view)
    
    
    def getItemData(self, article_id):
        base_url = f"https://www.vinted.fr/api/v2/items/{article_id}?localize=false"
        req = self.session.get(base_url)
        
        # 429: Too Many Requests -> recursivity until code 200
        if req.status_code == 429:
            sleep(3)
            return self.getItemData(article_id)
        
        data = req.json()['item']
        
        with open('bruger.json', 'w') as file:
            json.dump(data, file)
        
        item = {
            article_id: {
                'title': data['title'],
                'description': data['description'],
                'item_photo': data['photos'][0]['url'],
                
                'price': data['price']['amount'],
                'currency': data['price']['currency_code'],
                'service_fee': data['service_fee'],
                'total_item_price': data['total_item_price'],
                
                'item_url':data['url'],
                
                'user': {
                    "login": data['user']['login'],
                    "pfp": None, # check after bc sometimes there is not
                    "country_code": data['user']['country_code'],
                    "feedback_reputation": data['user']['feedback_reputation'],
                    "feedback_count": data['user']['feedback_count']
                }
            }
        }
        
        try:
            item[article_id]['user']['pfp'] = data['user']['photo']['url']
        except:
            item[article_id]['user']['pfp'] = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"
        
        return item