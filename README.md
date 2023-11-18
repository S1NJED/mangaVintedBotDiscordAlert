# mangaVintedBotDiscordAlert

🇫🇷 ~ Un bot discord pour ajouter des alertes dès qu'un nouvel article basé sur les mangas est posté sur Vinted. <br>
🇬🇧 ~ A discord bot to add alerts as soon as a new manga-based article is posted on Vinted. <br>
🇮🇹 ~ Un bot discordia per aggiungere avvisi non appena un nuovo articolo basato su manga è pubblicato su Vinted. <br>

Il utilise les catégories de recherches suivantes: Livre (TOUS) et Le plus récent

## Installation

Windows10:
1. Créer un environment virtuel: `python3 -m venv .venv`
2. Activez le: `.venv\Scripts\activate`
3. Installez les libraires: `pip3 install -r requirements.txt`

Unix:
1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip3 install -r requirements.txt` 

## Configuration

Copiez-collez le `TOKEN` de votre Bot Dicord dans le fichier .env (TOKEN=VOTRE_TOKEN)
Votre Bot doit avoir tout les *intents* d'activé

## Usage

Lancez le fichier `bot.py`.

## Commandes

* `/create_alert`: Créer une alerte
  * channel: le text channel où recevoir les alertes
  * name: le nom de l'article auquel vous voulez recevoir des alertes
  * country_code: si spécifié alors vous n'allez recevoir que des articles provenant du pays sélectionné


* `/get_alerts`: Voir toutes les alertes actives

* `/delete_alert`
  * alert_index: l'indice de l'alerte, utilisez /get_alerts pour voir l'indice

* `/get_loop_interval`: Récupère le délai en secondes de la boucle qui check les nouveaux articles en fond (Vérification des nouveaux articles toutes les X secondes)

* `/edit_loop_interval`: Modifie le délai (Je ne recommande pas d'y mettre la valeur en dessous de 20-30 secondes)

