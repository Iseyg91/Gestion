import discord
from discord.ext import commands, tasks
from discord import app_commands, Embed, ButtonStyle, ui
from discord.ui import Button, View, Select, Modal, TextInput
from discord.utils import get
from discord import TextStyle
from functools import wraps
import os
import io
import random
import asyncio
import time
import re
import subprocess
import sys
import math
import traceback
from keep_alive import keep_alive
from datetime import datetime, timedelta  # Tu as déjà la bonne importation pour datetime et timedelta
from collections import defaultdict, deque
import pymongo
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import psutil
import pytz
import platform
from discord import Interaction
import logging
from typing import Optional

token = os.environ['ETHERYA']
intents = discord.Intents.all()
start_time = time.time()
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

#Configuration du Bot:
# --- ID Owner Bot ---
ISEY_ID = 792755123587645461
# Définir GUILD_ID
GUILD_ID = 1034007767050104892

# --- ID Etherya Partenariats ---
partnership_channel_id = 1355158081855688745
ROLE_ID = 1355157749994098860

# -- ID TICKET --
TRANSCRIPT_CHANNEL_ID = 1355158107956707498
SUPPORT_ROLE_ID = 1355157686815293441

# --- ID Etherya ---
ETHERYA_SERVER_ID = 1034007767050104892
AUTORIZED_SERVER_ID = 1034007767050104892
WELCOME_CHANNEL_ID = 1355198748296351854

log_channels = {
    "sanctions": 1365674258591912018,
    "messages": 1365674387700977684,
    "utilisateurs": 1365674425394921602,
    "nicknames": 1365674498791051394,
    "roles": 1365674530793586758,
    "vocal": 1365674563458826271,
    "serveur": 1365674597692997662,
    "permissions": 1365674740915765278,
    "channels": 1365674773107052644,
    "webhooks": 1365674805143146506,
    "bots": 1365674841344049162,
    "boosts": 1365674914740441158
}

def get_log_channel(guild, key):
    log_channel_id = log_channels.get(key)
    if log_channel_id:
        return guild.get_channel(log_channel_id)
    return None

# Fonction pour créer des embeds formatés
def create_embed(title, description, color=discord.Color.blue(), footer_text=""):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text=footer_text)
    return embed

# Connexion MongoDB
mongo_uri = os.getenv("MONGO_DB")  # URI de connexion à MongoDB
print("Mongo URI :", mongo_uri)  # Cela affichera l'URI de connexion (assure-toi de ne pas laisser cela en prod)
client = MongoClient(mongo_uri)
db = client['Cass-Eco2']

# Collections
collection = db['ether_eco']  #Stock les Bal
collection2 = db['ether_daily']  #Stock les cd de daily
collection3 = db['ether_slut']  #Stock les cd de slut
collection4 = db['ether_crime']  #Stock les cd de slut
collection5 = db['ether_collect'] #Stock les cd de collect
collection6 = db['ether_work'] #Stock les cd de Work
collection7 = db['ether_inventory'] #Stock les inventaires
collection8 = db['info_cf'] #Stock les Info du cf
collection9 = db['info_logs'] #Stock le Salon logs
collection10 = db['info_bj'] #Stock les Info du Bj
collection11 = db['info_rr'] #Stock les Info de RR
collection12 = db['info_roulette'] #Stock les Info de SM
collection13 = db['info_sm'] #Stock les Info de SM
collection14 = db['ether_rob'] #Stock les cd de Rob
collection15 = db['anti_rob'] #Stock les rôle anti-rob
collection16 = db['ether_boutique'] #Stock les Items dans la boutique
collection17 = db['joueur_ether_inventaire'] #Stock les items de joueurs
collection18 = db['ether_effects'] #Stock les effets
collection19 = db['ether_badge'] #Stock les bagde
collection20 = db['inventaire_badge'] #Stock les bagde des joueurs
collection21 = db['daily_badge'] #Stock les cd des daily badge
collection22 = db['start_date'] #Stock la date de commencemant des rewards
collection23 = db['joueur_rewards'] #Stock ou les joueurs sont
collection24 = db['cd_renforcement'] #Stock les cd
collection25 = db['cd_emission'] #Stock les cd
collection26 = db['cd_manipulation'] #Stock les cd
collection27 = db['cd_materialisation'] #Stock les cd
collection28 = db['cd_transformation'] #Stock les cd
collection29 = db['cd_specialisation'] #Stock les cd
collection30 = db['cd_haki_attaque'] #Stock les cd
collection31 = db['cd_haki_subis'] #Stock les cd
collection32 = db['ether_quetes'] #Stock les quetes
collection33 = db['inventory_collect'] #Stock les items de quetes
collection34 = db['collect_items'] #Stock les items collector
collection35 = db['ether_guild'] #Stock les Guild
collection36 = db['guild_inventaire'] #Stock les inventaire de Guild
collection37 = db['ether_bounty'] #Stock les Primes de Pirates
collection38 = db['ether_honor'] #Stock les Honor des Marines
collection39 = db['cd_capture_ether'] #Stock les cd d'attaque
collection40 = db['cd_bombe'] #Stock les cd des bombes
collection41 = db['cd_gura'] #Stock les cd de seismes
collection42 = db['cd_glace'] #Stock les cd d'attaque de glace
collection43 = db['glace_subis'] #Stock le cd avant de retirer le rôle de subis de glace
collection44 = db['cd_tenebre'] #Stock les cd de Yami
collection45 = db['cd_protection_tenebre'] #Stock le temps de protection de Yami
collection46 = db['cd_gear_second'] #Stock le cd des Gear Second
collection47 = db['cd_gear_fourth'] #Stock les cd des Gear Fourth
collection48 = db['cd_use_fourth'] #Stock les cd des utilisation du Gear Fourth
collection49 = db['cd_royaume_nika'] #Stock le cd des utilisation du Royaume
collection50 = db['cd_acces_royaume'] #Stock le cd d'acces au Royaume
collection51 = db['cd_nika_collect'] #Stock le cd de reutilisation du Nika Collect
collection52 = db['cd_eveil_attaque'] #Stock le cd de reutilisation du Nika Eveil
collection53 = db['cd_eveil_subis'] #Stock le cd de soumission du Nika Eveil
collection54 = db['cd_bourrasque'] #Stock le cd de reutilisation du Uo Uo no Mi
collection55 = db['cd_bourrasque_subis'] #Stock le cd de soumission du Uo Uo no Mi
collection56 = db['cd_tonnerre_attaque'] #Stock les cd de reutillisation du Tonnerre Divin
collection57 = db['cd_tonnerre_subis'] #Stock les cd de soumission du Tonnerre Divin
collection58 = db['cd_eveil_uo'] #Stock les cd d'eveil du Dragon
collection59 = db['message_jour'] #Stock les message des membres chaque jour
collection60 = db['cd_wobservation'] #Stock les cd de W Observation
collection61 = db['cd_observation']
collection62 = db['ether_ticket'] 

# Fonction pour vérifier si l'utilisateur possède un item (fictif, à adapter à ta DB)
async def check_user_has_item(user: discord.Member, item_id: int):
    # Ici tu devras interroger la base de données MongoDB ou autre pour savoir si l'utilisateur possède cet item
    # Par exemple:
    # result = collection.find_one({"user_id": user.id, "item_id": item_id})
    # return result is not None
    return True  # Pour l'exemple, on suppose que l'utilisateur a toujours l'item.

def get_cf_config(guild_id):
    config = collection8.find_one({"guild_id": guild_id})
    if not config:
        # Valeurs par défaut
        config = {
            "guild_id": guild_id,
            "start_chance": 50,
            "max_chance": 100,
            "max_bet": 20000
        }
        collection8.insert_one(config)
    return config

def load_guild_settings(guild_id):
    # Charger les données de la collection principale
    ether_eco_data = collection.find_one({"guild_id": guild_id}) or {}
    ether_daily_data = collection2.find_one({"guild_id": guild_id}) or {}
    ether_slut_data = collection3.find_one({"guild_id": guild_id}) or {}
    ether_crime_data = collection4.find_one({"guild_id": guild_id}) or {}
    ether_collect = collection5.find_one({"guild_id": guild_id}) or {}
    ether_work_data = collection6.find_one({"guild_id": guild_id}) or {}
    ether_inventory_data = collection7.find_one({"guild_id": guild_id}) or {}
    info_cf_data = collection8.find_one({"guild_id": guild_id}) or {}
    info_logs_data = collection9.find_one({"guild_id": guild_id}) or {}
    info_bj_data = collection10.find_one({"guild_id": guild_id}) or {}
    info_rr_data = collection11.find_one({"guild_id": guild_id}) or {}
    info_roulette_data = collection12.find_one({"guild_id": guild_id}) or {}
    info_sm_roulette_data = collection13.find_one({"guild_id": guild_id}) or {}
    ether_rob_data = collection14.find_one({"guild_id": guild_id}) or {}
    anti_rob_data = collection15.find_one({"guild_id": guild_id}) or {}
    ether_boutique_data = collection16.find_one({"guild_id": guild_id}) or {}
    joueur_ether_inventaire_data = collection17.find_one({"guild_id": guild_id}) or {}
    ether_effects_data = collection18.find_one({"guild_id": guild_id}) or {}
    ether_badge_data = collection19.find_one({"guild_id": guild_id}) or {}
    inventaire_badge_data = collection20.find_one({"guild_id": guild_id}) or {}
    daily_badge_data = collection21.find_one({"guild_id": guild_id}) or {}
    start_date_data = collection22.find_one({"guild_id": guild_id}) or {}
    joueur_rewards_data = collection23.find_one({"guild_id": guild_id}) or {}
    cd_renforcement_data = collection24.find_one({"guild_id": guild_id}) or {}
    cd_emission_data = collection25.find_one({"guild_id": guild_id}) or {}
    cd_manipultation_data = collection26.find_one({"guild_id": guild_id}) or {}
    cd_materialisation_data = collection27.find_one({"guidl_id": guild_id}) or {}
    cd_transformation_data = collection28.find_one({"guild_id": guild_id}) or {}
    cd_specialisation_data = collection29.find_one({"guild_id": guild_id}) or {}
    cd_haki_attaque_data = collection30.find_one({"guild_id": guild_id}) or {}
    cd_haki_subis_data = collection31.find_one({"guild_id": guild_id}) or {}
    ether_quetes_data = collection32.find_one({"guild_id": guild_id}) or {}
    inventory_collect_data = collection33.find_one({"guild_id": guild_id}) or {}
    collect_items_data = collection34.find_one({"guild_id": guild_id}) or {}
    ether_guild_data = collection35.find_one({"guild_id": guild_id}) or {}
    guild_inventaire_data = collection36.find_one({"guild_id": guild_id}) or {}
    ether_bounty_data = collection37.find_one({"guild_id": guild_id}) or {}
    ether_honnor_data = collection38.find_one({"guild_id": guild_id}) or {}
    cd_capture_ether_data = collection39.find_one({"guild_id": guild_id}) or {}
    cd_bombe_data = collection40.find_one({"guild_id": guild_id}) or {}
    cd_gura_data = collection41.find_one({"guild_id": guild_id}) or {}
    cd_glace_data = collection42.fing_one({"guild_id": guild_id}) or {}
    glace_subis_data = collection43.find_one({"guild_id": guild_id}) or {}
    cd_tenebre_data = collection44.find_one({"guild_id": guild_id}) or {}
    cd_protection_tenebre_data = collection45.find_one({"guild_id": guild_id}) or {}
    cd_gear_second_data = collection46.find_one({"guild_id": guild_id}) or {}
    cd_gear_fourth_data = collection47.find_one({"guild_id": guild_id}) or {}
    cd_use_fourth_data = collection48.find_one({"guild_id": guild_id}) or {}
    cd_royaume_nika_data = collection49.find_one({"guild_id": guild_id}) or {}
    cd_acces_royaume_data = collection50.find_one({"guild_id": guild_id}) or {}
    cd_nika_collect_data = collection51.find_one({"guild_id": guild_id}) or {}
    cd_eveil_attaque_data = collection52.find_one({"guild_id": guild_id}) or {}
    cd_eveil_subis_data = collection53.find_one({"guild_id": guild_id}) or {}
    cd_bourrasque_data = collection54.find_one({"guild_id": guild_id}) or {}
    cd_bourrasque_subis_data = collection55.find_one({"guild_id": guild_id}) or {}
    cd_tonnerre_attaque_data = collection56.find_one({"guild_id": guil_id}) or {}
    cd_tonnerre_subis_data = collection57.find_one({"guild_id": guild_id}) or {}
    cd_eveil_uo_data = collection58.find_one({"guild_id": guild_id}) or {}
    message_jour_data = collection59.find_one({"guild_id": guild_id}) or {}
    cd_wobservation_data = collection60.find_one({"guild_id": guild_id}) or {}
    cd_observation_data = collection61.find_one({"guild_id": guild_id}) or {}
    ether_ticket_data = collection62.find_one({"guild_id": guildu_id}) or {}
    
    # Débogage : Afficher les données de setup
    print(f"Setup data for guild {guild_id}: {setup_data}")

    combined_data = {
        "ether_eco": ether_eco_data,
        "ether_daily": ether_daily_data,
        "ether_slut": ether_slut_data,
        "ether_crime": ether_crime_data,
        "ether_collect": ether_collect_data,
        "ether_work": ether_work_data,
        "ether_inventory": ether_inventory_data,
        "info_cf": info_cf_data,
        "info_logs": info_logs_data,
        "info_bj": info_bj_data,
        "info_rr": info_rr_data,
        "info_roulette": info_roulette_data,
        "info_sm": info_sm_data,
        "ether_rob": ether_rob_data,
        "anti_rob": anti_rob_data,
        "ether_boutique": ether_boutique_data,
        "joueur_ether_inventaire": joueur_ether_inventaire_data,
        "ether_effects": ether_effects_data,
        "ether_badge": ether_badge_data,
        "inventaire_badge": inventaire_badge_data,
        "daily_badge": daily_badge_data,
        "start_date": start_date_data,
        "joueur_rewards": joueur_rewards_data,
        "cd_renforcement": cd_renforcement_data,
        "cd_emission": cd_emission_data,
        "cd_manipultation": cd_manipultation_data,
        "cd_materialisation": cd_materialisation_data,
        "cd_transformation" : cd_transformation_data,
        "cd_specialisation" : cd_specialisation_data,
        "cd_haki_attaque": cd_haki_attaque_data,
        "cd_haki_subis": cd_haki_subis_data,
        "ether_quetes": ether_quetes_data,
        "inventory_collect": inventory_collect_data,
        "collect_items": collect_items_data,
        "ether_guild": ether_guild_data,
        "guild_inventaire": guild_inventaire_data,
        "ether_bounty": ether_bounty_data,
        "ether_honnor": ether_honnor_data,
        "cd_capture_ether": cd_capture_ether_data,
        "cd_bombe": cd_bombe_data,
        "cd_gura": cd_gura_data,
        "cd_glace": cd_glace_data,
        "glace_subis": glace_subis_data,
        "cd_tenebre": cd_tenebre_data,
        "cd_protection_tenebre": cd_protection_tenebre_data,
        "cd_gear_second": cd_gear_second_data,
        "cd_gear_fourth": cd_gear_fourth_data,
        "cd_use_fourth": cd_use_fourth_data,
        "cd_royaume_nika": cd_royaume_nika_data,
        "cd_acces_royaume": cd_acces_royaume_data,
        "cd_nika_collect": cd_nika_collect_data,
        "cd_eveil_attaque": cd_eveil_attaque_data,
        "cd_eveil_subis": cd_eveil_subis_data,
        "cd_bourrasque": cd_bourrasque_data,
        "cd_bourrasque_subis": cd_bourrasque_subis_data,
        "cd_tonnerre_attaque": cd_tonnerre_attaque_data,
        "cd_tonnerre_subis": cd_tonnerre_subis_data,
        "cd_eveil_uo": cd_eveil_uo_data,
        "message_jour": message_jour_data,
        "cd_wobservation": cd_wobservation_data,
        "cd_observation": cd_observation_data,
        "ether_ticket": ether_ticket_data
    }

    return combined_data

# --- Initialisation au démarrage ---
@bot.event
async def on_ready():
    bot.add_view(TicketView(author_id=ISEY_ID))  # pour bouton "Passé Commande"
    bot.add_view(ClaimCloseView())               # pour "Claim" et "Fermer"
    print(f"{bot.user.name} est connecté.")
    bot.uptime = time.time()
    activity = discord.Activity(
        type=discord.ActivityType.streaming,
        name="Etherya",
    )
    await bot.change_presence(activity=activity, status=discord.Status.online)

    print(f"🎉 **{bot.user}** est maintenant connecté et affiche son activité de stream avec succès !")
    print("📌 Commandes disponibles 😊")
    for command in bot.commands:
        print(f"- {command.name}")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Commandes slash synchronisées : {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"❌ Erreur de synchronisation des commandes slash : {e}")

# --- Gestion globale des erreurs ---
@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Une erreur s'est produite : {event}")
    embed = discord.Embed(
        title="❗ Erreur inattendue",
        description="Une erreur s'est produite lors de l'exécution de la commande. Veuillez réessayer plus tard.",
        color=discord.Color.red()
    )
    try:
        await args[0].response.send_message(embed=embed)
    except Exception:
        pass

# Ton on_message reste pratiquement pareil
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # Gestion des partenariats dans un salon spécifique
    if message.channel.id == partnership_channel_id:
        rank, partnerships = get_user_partner_info(message.author.id)

        await message.channel.send("<@&1355157749994098860>")

        embed = discord.Embed(
            title="Merci du partenariat 🤝",
            description=f"{message.author.mention}\nTu es rank **{rank}**\nTu as effectué **{partnerships}** partenariats.",
            color=discord.Color.green()
        )
        embed.set_footer(
            text="Partenariat réalisé",
            icon_url="https://github.com/Iseyg91/KNSKS-ET/blob/main/Images_GITHUB/Capture_decran_2024-09-28_211041.png?raw=true"
        )
        embed.set_image(
            url="https://github.com/Iseyg91/KNSKS-ET/blob/main/Images_GITHUB/Capture_decran_2025-02-15_231405.png?raw=true"
        )
        await message.channel.send(embed=embed)

    # Permet à la commande de continuer à fonctionner si d'autres événements sont enregistrés
    await bot.process_commands(message)

#Bienvenue : Message de Bienvenue + Ghost Ping Join
private_threads = {}  # Stocke les fils privés des nouveaux membres

# Liste des salons à pinguer
salon_ids = [
    1355198748296351854
]

class GuideView(View):
    def __init__(self, thread):
        super().__init__()
        self.thread = thread
        self.message_sent = False  # Variable pour contrôler l'envoi du message

    @discord.ui.button(label="📘 Guide", style=discord.ButtonStyle.success, custom_id="guide_button_unique")
    async def guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.message_sent:  # Empêche l'envoi du message en doublon
            await interaction.response.defer()
            await start_tutorial(self.thread, interaction.user)
            self.message_sent = True

    @discord.ui.button(label="❌ Non merci", style=discord.ButtonStyle.danger, custom_id="no_guide_button_unique")
    async def no_guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔒 Fermeture du fil...", ephemeral=True)
        await asyncio.sleep(2)
        await self.thread.delete()

class NextStepView(View):
    def __init__(self, thread):
        super().__init__()
        self.thread = thread

    @discord.ui.button(label="➡️ Passer à la suite", style=discord.ButtonStyle.primary, custom_id="next_button")
    async def next_step(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        user = interaction.user

        # Envoi du message privé
        await send_economy_info(user)

        # Envoi du message de confirmation dans le fil privé
        await self.thread.send("📩 Les détails de cette étape ont été envoyés en message privé.")

        # Attente de 2 secondes
        await asyncio.sleep(2)

        # Message d'avertissement avant suppression
        await self.thread.send("🗑️ Ce fil sera supprimé dans quelques instants.")

        # Suppression du fil privé
        await asyncio.sleep(3)
        await self.thread.delete()

async def wait_for_command(thread, user, command):
    def check(msg):
        return msg.channel == thread and msg.author == user and msg.content.startswith(command)

    await thread.send(f"🕒 En attente de `{command}`...")  # Envoi du message d'attente
    await bot.wait_for("message", check=check)  # Attente du message de la commande
    await thread.send("✅ Commande exécutée ! Passons à la suite. 🚀")  # Confirmation après la commande
    await asyncio.sleep(2)  # Pause avant de passer à l'étape suivante

async def start_tutorial(thread, user):
    tutorial_steps = [
        ("💼 **Commande Travail**", "Utilise `!!work` pour gagner un salaire régulièrement !", "!!work"),
        ("📦 **Commande Quotidient**", "Utilise !!daily pour gagner un salaire quotidient !", "!!daily"),
        ("💃 **Commande Slut**", "Avec `!!slut`, tente de gagner de l'argent... Mais attention aux risques !", "!!slut"),
        ("🔫 **Commande Crime**", "Besoin de plus de frissons ? `!!crime` te plonge dans des activités illégales !", "!!crime"),
        ("🌿 **Commande Collecte**", "Avec `!!collect`, tu peux ramasser des ressources utiles !", "!!collect"),
        ("📊 **Classement**", "Découvre qui a le plus d'argent en cash avec `!!lb -cash` !", "!!lb -cash"),
        ("🕵️ **Voler un joueur**", "Tente de dérober l'argent d'un autre avec `!!rob @user` !", "!!rob"),
        ("🏦 **Dépôt Bancaire**", "Pense à sécuriser ton argent avec `!!dep all` !", "!!dep all"),
        ("💰 **Solde Bancaire**", "Vérifie ton argent avec `!!bal` !", "!!bal"),
    ]

    for title, desc, cmd in tutorial_steps:
        embed = discord.Embed(title=title, description=desc, color=discord.Color.blue())
        await thread.send(embed=embed)
        await wait_for_command(thread, user, cmd)  # Attente de la commande de l'utilisateur

    # Embed final des jeux
    games_embed = discord.Embed(
        title="🎲 **Autres Commandes de Jeux**",
        description="Découvre encore plus de moyens de t'amuser et gagner des Ezryn Coins !",
        color=discord.Color.gold()
    )
    games_embed.add_field(name="🐔 Cock-Fight", value="`!!cf <amount>` - Combat de Poulet !", inline=False)
    games_embed.add_field(name="🃏 Blackjack", value="`!!bj <amount>` - Jeux de Carte !", inline=False)
    games_embed.add_field(name="🎰 Slot Machine", value="`!!sm <amount>` - Tente un jeu risqué !", inline=False)
    games_embed.add_field(name="🔫 Roulette Russe", value="`!!rr <amount>` - Joue avec le destin !", inline=False)
    games_embed.add_field(name="🎡 Roulette", value="`!!roulette <amount>` - Fais tourner la roue de la fortune !", inline=False)
    games_embed.set_footer(text="Amuse-toi bien sur Etherya ! 🚀")

    await thread.send(embed=games_embed)
    await thread.send("Clique sur **Passer à la suite** pour découvrir les systèmes impressionnants de notre Economie !", view=NextStepView(thread))

async def send_economy_info(user: discord.Member):
    try:
        economy_embed = discord.Embed(
            title="📌 **Lis ces salons pour optimiser tes gains !**",
            description=(
                "Bienvenue dans l'économie du serveur ! Pour en tirer le meilleur profit, assure-toi de lire ces salons :\n\n"
                "💰 **Comment accéder à l'economie ?**\n➜ <#1355190022047011117>\n\n"
                "📖 **Informations générales**\n➜ <#1355158018517500086>\n\n"
                "💰 **Comment gagner des Coins ?**\n➜ <#1355157853299675247>\n\n"
                "🏦 **Banque de l'Économie **\n➜ <#1364531840144244819>\n\n"
                "🎟️ **Ticket Finances** *(Pose tes questions ici !)*\n➜ <#1355157942005006558>\n\n"
                "📈 **Astuce :** Plus tu en sais, plus tu gagnes ! Alors prends quelques minutes pour lire ces infos. 🚀"
            ),
            color=discord.Color.gold()
        )
        economy_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1168755764760559637.webp?size=96&quality=lossless")
        economy_embed.set_footer(text="Bon jeu et bons profits ! 💰")

        dm_channel = await user.create_dm()
        await dm_channel.send(embed=economy_embed)
    except discord.Forbidden:
        print(f"Impossible d'envoyer un MP à {user.name} ({user.id})")
        
@bot.event
async def on_member_join(member):
    guild_id = str(member.guild.id)

    # Vérifie si c'est le serveur Etherya
    if member.guild.id == ETHERYA_SERVER_ID:
        # Envoi du message de bienvenue dans le salon de bienvenue
        channel = bot.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title="<a:fete:1172810362261880873> Bienvenue sur le serveur ! <a:fete:1172810362261880873>",
                description=(
                    "*<a:fire:1343873843730579478> Ici, l’économie règne en maître, les alliances se forment, les trahisons éclatent... et ta richesse ne tient qu’à un fil ! <a:fire:1343873843730579478>*\n\n"
                    "<:better_scroll:1342376863909285930> **Avant de commencer, prends le temps de lire :**\n\n"
                    "- <a:fleche3:1290077283100397672> **<#1355157955804139560>** pour éviter les problèmes dès le départ.\n"
                    "- <a:fleche3:1290077283100397672> **<#1364473395982630945>** pour comprendre les bases de l’économie.\n"
                    "- <a:fleche3:1290077283100397672> **<#1364477906096623746>** pour savoir ce que tu peux obtenir.\n\n"
                    "💡 *Un doute ? Une question ? Ouvre un ticket et le staff t’aidera !*\n\n"
                    "**Prépare-toi à bâtir ton empire... ou à tout perdre. Bonne chance ! 🍀**"
                ),
                color=discord.Color.gold()
            )
            embed.set_image(url="https://raw.githubusercontent.com/Cass64/EtheryaBot/main/images_etherya/etheryaBot_banniere.png")
            await channel.send(f"{member.mention}", embed=embed)

        # Envoi du ghost ping une seule fois par salon
        for salon_id in salon_ids:
            salon = bot.get_channel(salon_id)
            if salon:
                try:
                    message = await salon.send(f"{member.mention}")
                    await message.delete()
                except discord.Forbidden:
                    print(f"Le bot n'a pas la permission d'envoyer un message dans {salon.name}.")
                except discord.HTTPException:
                    print("Une erreur est survenue lors de l'envoi du message.")

        # Création d'un fil privé pour le membre
        channel_id = 1355158120095027220  # Remplace par l'ID du salon souhaité
        channel = bot.get_channel(channel_id)

        if channel and isinstance(channel, discord.TextChannel):
            thread = await channel.create_thread(name=f"🎉 Bienvenue {member.name} !", type=discord.ChannelType.private_thread)
            await thread.add_user(member)
            private_threads[member.id] = thread

            # Embed de bienvenue
            welcome_embed = discord.Embed(
                title="🌌 Bienvenue à Etherya !",
                description=(
                    "Une aventure unique t'attend, entre **économie dynamique**, **stratégies** et **opportunités**. "
                    "Prêt à découvrir tout ce que le serveur a à offrir ?"
                ),
                color=discord.Color.blue()
            )
            welcome_embed.set_thumbnail(url=member.avatar.url if member.avatar else bot.user.avatar.url)
            await thread.send(embed=welcome_embed)

            # Embed du guide
            guide_embed = discord.Embed(
                title="📖 Besoin d'un Guide ?",
                description=(
                    "Nous avons préparé un **Guide de l'Économie** pour t'aider à comprendre notre système monétaire et "
                    "les différentes façons d'évoluer. Veux-tu le suivre ?"
                ),
                color=discord.Color.gold()
            )
            guide_embed.set_footer(text="Tu peux toujours y accéder plus tard via la commande /guide ! 🚀")
            await thread.send(embed=guide_embed, view=GuideView(thread))  # Envoie le guide immédiatement

        # Envoi d'une notification de log dans le salon spécifique du serveur
        if member.guild.id == ETHERYA_SERVER_ID:
            channel = get_log_channel(member.guild, "utilisateurs")
            if channel:
                embed = discord.Embed(
                    title="✅ Nouveau Membre",
                    description=f"{member.mention} a rejoint le serveur.",
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=member.display_avatar.url)
                embed.set_footer(text=f"ID de l'utilisateur : {member.id}")
                embed.timestamp = member.joined_at or discord.utils.utcnow()

                await channel.send(embed=embed)

@bot.tree.command(name="guide", description="Ouvre un guide personnalisé pour comprendre l'économie du serveur.")
async def guide_command(interaction: discord.Interaction):
    user = interaction.user

    # Vérifie si le serveur est Etherya avant d'exécuter le reste du code
    if interaction.guild.id != ETHERYA_SERVER_ID:
        await interaction.response.send_message("❌ Cette commande est uniquement disponible sur le serveur Etherya.", ephemeral=True)
        return

    # Crée un nouveau thread privé à chaque commande
    channel_id = 1355158120095027220
    channel = bot.get_channel(channel_id)

    if not channel:
        await interaction.response.send_message("❌ Le canal est introuvable ou le bot n'a pas accès à ce salon.", ephemeral=True)
        return

    # Vérifie si le bot peut créer des threads dans ce canal
    if not channel.permissions_for(channel.guild.me).send_messages or not channel.permissions_for(channel.guild.me).manage_threads:
        await interaction.response.send_message("❌ Le bot n'a pas les permissions nécessaires pour créer des threads dans ce canal.", ephemeral=True)
        return

    try:
        # Crée un nouveau thread à chaque fois que la commande est exécutée
        thread = await channel.create_thread(
            name=f"🎉 Bienvenue {user.name} !", 
            type=discord.ChannelType.private_thread,
            invitable=True
        )
        await thread.add_user(user)  # Ajoute l'utilisateur au thread

        # Embed de bienvenue et guide pour un nouveau thread
        welcome_embed = discord.Embed(
            title="🌌 Bienvenue à Etherya !",
            description="Une aventure unique t'attend, entre **économie dynamique**, **stratégies** et **opportunités**. "
                        "Prêt à découvrir tout ce que le serveur a à offrir ?",
            color=discord.Color.blue()
        )
        welcome_embed.set_thumbnail(url=user.avatar.url if user.avatar else bot.user.avatar.url)
        await thread.send(embed=welcome_embed)

    except discord.errors.Forbidden:
        await interaction.response.send_message("❌ Le bot n'a pas les permissions nécessaires pour créer un thread privé dans ce canal.", ephemeral=True)
        return

    # Embed du guide
    guide_embed = discord.Embed(
        title="📖 Besoin d'un Guide ?",
        description="Nous avons préparé un **Guide de l'Économie** pour t'aider à comprendre notre système monétaire et "
                    "les différentes façons d'évoluer. Veux-tu le suivre ?",
        color=discord.Color.gold()
    )
    guide_embed.set_footer(text="Tu peux toujours y accéder plus tard via cette commande ! 🚀")
    await thread.send(embed=guide_embed, view=GuideView(thread))  # Envoie le guide avec les boutons

    await interaction.response.send_message("📩 Ton guide personnalisé a été ouvert.", ephemeral=True)

    # IMPORTANT : Permet au bot de continuer à traiter les commandes
    await bot.process_commands(message)

#---------------------------------------------------------------------------------------- LOGGER LOG:

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return  # Ignore les messages de bots
    # Log du message supprimé (si sur le serveur ETHERYA)
    if message.guild and message.guild.id == ETHERYA_SERVER_ID:
        log_channel = get_log_channel(message.guild, "messages")
        if log_channel:
            embed = discord.Embed(
                title="🗑️ Message Supprimé",
                description=f"**Auteur :** {message.author.mention}\n**Salon :** {message.channel.mention}",
                color=discord.Color.red()
            )
            if message.content:
                embed.add_field(name="Contenu", value=message.content, inline=False)
            else:
                embed.add_field(name="Contenu", value="*Aucun texte (peut-être un embed ou une pièce jointe)*", inline=False)

            embed.set_footer(text=f"ID de l'utilisateur : {message.author.id}")
            embed.timestamp = message.created_at

            await log_channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):
    if before.guild and before.guild.id == ETHERYA_SERVER_ID and before.content != after.content:
        channel = get_log_channel(before.guild, "messages")
        if channel:
            embed = discord.Embed(
                title="✏️ Message Édité",
                description=f"**Auteur :** {before.author.mention}\n**Salon :** {before.channel.mention}",
                color=discord.Color.orange()
            )
            embed.add_field(name="Avant", value=before.content or "*Vide*", inline=False)
            embed.add_field(name="Après", value=after.content or "*Vide*", inline=False)
            embed.set_footer(text=f"ID de l'utilisateur : {before.author.id}")
            embed.timestamp = after.edited_at or discord.utils.utcnow()

            await channel.send(embed=embed)

@bot.event
async def on_member_remove(member: discord.Member):
    guild_id = str(member.guild.id)

    # Traitement du départ de membre pour un serveur spécifique (PROJECT_DELTA)
    if member.guild.id == ETHERYA_SERVER_ID:
        channel = get_log_channel(member.guild, "utilisateurs")
        if channel:
            embed = discord.Embed(
                title="❌ Départ d'un Membre",
                description=f"{member.mention} a quitté le serveur.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"ID de l'utilisateur : {member.id}")
            embed.timestamp = discord.utils.utcnow()

            # Ajouter la durée de présence si disponible
            if member.joined_at:
                duration = discord.utils.utcnow() - member.joined_at
                days = duration.days
                hours = duration.seconds // 3600
                minutes = (duration.seconds % 3600) // 60

                formatted_duration = f"{days}j {hours}h {minutes}min"
                embed.add_field(name="Durée sur le serveur", value=formatted_duration, inline=False)

            await channel.send(embed=embed)

# --- Nickname update ---
@bot.event
async def on_user_update(before, after):
    # Check for username changes (this affects all mutual servers)
    for guild in bot.guilds:
        if guild.id == ETHERYA_SERVER_Id:
            if before.name != after.name:
                channel = get_log_channel(guild, "nicknames")
                if channel:
                    embed = discord.Embed(
                        title="📝 Changement de Pseudo Global",
                        description=f"{after.mention} a changé son pseudo global.",
                        color=discord.Color.blurple()
                    )
                    embed.add_field(name="Avant", value=f"`{before.name}`", inline=True)
                    embed.add_field(name="Après", value=f"`{after.name}`", inline=True)
                    embed.set_footer(text=f"ID de l'utilisateur : {after.id}")
                    embed.timestamp = discord.utils.utcnow()

                    await channel.send(embed=embed)

@bot.event
async def on_member_update(before, after):
    if before.guild.id != ETHERYA_SERVER_ID:  # Vérifier si c'est le bon serveur
        return

    # --- Nickname logs ---
    if before.nick != after.nick:
        channel = get_log_channel(before.guild, "nicknames")
        if channel:
            embed = discord.Embed(
                title="📝 Changement de Surnom",
                description=f"{before.mention} a modifié son surnom sur le serveur.",
                color=discord.Color.blue()
            )
            embed.add_field(name="Avant", value=f"`{before.nick}`" if before.nick else "*Aucun*", inline=True)
            embed.add_field(name="Après", value=f"`{after.nick}`" if after.nick else "*Aucun*", inline=True)
            embed.set_footer(text=f"ID de l'utilisateur : {after.id}")
            embed.timestamp = discord.utils.utcnow()

            await channel.send(embed=embed)

    # --- Boost du serveur ---
    if before.premium_since is None and after.premium_since is not None:
        channel = get_log_channel(before.guild, "boosts")
        if channel:
            embed = discord.Embed(
                title="💎 Nouveau Boost",
                description=f"{after.mention} a boosté le serveur !",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=after.display_avatar.url)
            embed.set_footer(text=f"ID de l'utilisateur : {after.id}")
            embed.timestamp = discord.utils.utcnow()

            await channel.send(embed=embed)
@bot.event
async def on_guild_role_create(role):
    guild_id = str(role.guild.id)
    # Log classique si protection désactivée
    if role.guild.id == ETHERYA_SERVER_ID:
        log_channel = get_log_channel(role.guild, "roles")
        if log_channel:
            embed = discord.Embed(
                title="🎭 Nouveau Rôle Créé",
                description=f"Un nouveau rôle a été créé : **{role.name}**",
                color=discord.Color.purple()
            )
            embed.add_field(name="ID du Rôle", value=str(role.id), inline=False)
            embed.set_footer(text="Rôle créé sur le serveur PROJECT_DELTA")
            embed.timestamp = discord.utils.utcnow()
            try:
                await log_channel.send(embed=embed)
                print(f"Log de création de rôle envoyé pour {role.name}.")
            except Exception as e:
                print(f"Erreur lors de l'envoi du log pour le rôle {role.name} : {e}")

@bot.event
async def on_guild_role_delete(role):
    guild_id = str(role.guild.id)

    # Log classique si suppression sans protection ou whitelistée
    if role.guild.id == ETHERYA_SERVER_ID:
        channel = get_log_channel(role.guild, "roles")
        if channel:
            embed = discord.Embed(
                title="🎭 Rôle Supprimé",
                description=f"Le rôle **{role.name}** a été supprimé.",
                color=discord.Color.red()
            )
            embed.add_field(name="ID du Rôle", value=str(role.id), inline=False)
            embed.set_footer(text="Rôle supprimé sur PROJECT_DELTA")
            embed.timestamp = discord.utils.utcnow()

            try:
                await channel.send(embed=embed)
                print(f"Log de suppression de rôle envoyé pour {role.name}.")
            except Exception as e:
                print(f"Erreur lors de l'envoi du log pour le rôle {role.name} : {e}")

# Logs pour les mises à jour de rôle
@bot.event
async def on_guild_role_update(before, after):
    if before.guild.id == ETHERYA_SERVER_ID:
        channel = get_log_channel(before.guild, "roles")
        if channel:
            embed = discord.Embed(
                title="🎭 Mise à Jour de Rôle",
                description=f"Le rôle **{before.name}** a été mis à jour :",
                color=discord.Color.orange()
            )
            embed.add_field(name="Avant", value=f"`{before.name}`", inline=False)
            embed.add_field(name="Après", value=f"`{after.name}`", inline=False)
            embed.add_field(name="ID du Rôle", value=str(after.id), inline=False)

            # Ajouter des informations supplémentaires, si nécessaire
            if before.permissions != after.permissions:
                embed.add_field(name="Permissions", value="Permissions modifiées", inline=False)
            
            embed.set_footer(text="Mise à jour du rôle")
            embed.timestamp = discord.utils.utcnow()

            await channel.send(embed=embed)

@bot.event
async def on_guild_channel_create(channel):
    guild_id = str(channel.guild.id)
    # Log de création si la protection n’est pas activée
    if channel.guild.id == ETHERYA_SERVER_ID:
        channel_log = get_log_channel(channel.guild, "channels")
        if channel_log:
            embed = discord.Embed(
                title="🗂️ Nouveau Salon Créé",
                description=f"Le salon **{channel.name}** a été créé.",
                color=discord.Color.blue()
            )
            embed.add_field(name="ID du Salon", value=str(channel.id), inline=False)
            embed.set_footer(text="Salon créé sur le serveur PROJECT_DELTA")
            embed.timestamp = discord.utils.utcnow()

            try:
                await channel_log.send(embed=embed)
            except Exception as e:
                print(f"Erreur lors du log de création de salon : {e}")

@bot.event
async def on_guild_channel_delete(channel):
    guild_id = str(channel.guild.id)
    # Log normal de suppression si protection non activée
    if channel.guild.id == ETHERYA_SERVER_ID:
        channel_log = get_log_channel(channel.guild, "channels")
        if channel_log:
            embed = discord.Embed(
                title="🗂️ Salon Supprimé",
                description=f"Le salon **{channel.name}** a été supprimé.",
                color=discord.Color.red()
            )
            embed.add_field(name="ID du Salon", value=str(channel.id), inline=False)
            embed.set_footer(text="Salon supprimé sur le serveur PROJECT_DELTA")
            embed.timestamp = discord.utils.utcnow()

            try:
                await channel_log.send(embed=embed)
                print(f"Log de suppression envoyé pour {channel.name}.")
            except Exception as e:
                print(f"Erreur lors de l'envoi du log pour la suppression : {e}")

# Log de la mise à jour de salon dans le serveur PROJECT_DELTA
@bot.event
async def on_guild_channel_update(before, after):
    if before.guild.id == ETHERYA_SERVER_ID:
        # Ignorer si c'est l'admin (toi) qui modifie le salon
        if before.guild.me.id == after.guild.me.id:
            return
        
        # Récupérer le salon de log pour les channels
        channel_log = get_log_channel(before.guild, "channels")
        if channel_log:
            embed = discord.Embed(
                title="🗂️ Mise à Jour de Salon",
                description=f"Le salon **{before.name}** a été mis à jour.",
                color=discord.Color.orange()
            )
            embed.add_field(name="Avant", value=f"`{before.name}`", inline=False)
            embed.add_field(name="Après", value=f"`{after.name}`", inline=False)

            # Log de modifications supplémentaires (comme les permissions, la description, etc.)
            if before.topic != after.topic:
                embed.add_field(name="Description", value=f"Avant : {before.topic if before.topic else 'Aucune'}\nAprès : {after.topic if after.topic else 'Aucune'}", inline=False)
            if before.position != after.position:
                embed.add_field(name="Position", value=f"Avant : {before.position}\nAprès : {after.position}", inline=False)

            embed.set_footer(text="Mise à jour du salon sur PROJECT_DELTA")
            embed.timestamp = discord.utils.utcnow()

            await channel_log.send(embed=embed)


# --- Voice state update ---
@bot.event
async def on_voice_state_update(member, before, after):
    if member.guild.id == ETHERYA_SERVER_ID:
        channel = get_log_channel(member.guild, "vocal")
        if channel:
            embed = discord.Embed(
                title="🎙️ Changement d'État Vocal",
                description=f"Changement d'état vocal pour {member.mention}",
                color=discord.Color.blue()
            )
            embed.set_footer(text="Logs des salons vocaux")
            embed.timestamp = discord.utils.utcnow()

            if after.channel:
                embed.add_field(name="Rejoint le salon vocal", value=f"{after.channel.name}", inline=False)
            if before.channel:
                embed.add_field(name="Quitte le salon vocal", value=f"{before.channel.name}", inline=False)

            await channel.send(embed=embed)

# --- Guild update ---
@bot.event
async def on_guild_update(before, after):
    if before.id == ETHERYA_SERVER_ID:
        channel = get_log_channel(after, "serveur")  # Assurez-vous que 'after' est le bon paramètre pour obtenir le canal
        if channel:
            embed = discord.Embed(
                title="⚙️ Mise à Jour du Serveur",
                description="Des modifications ont été apportées au serveur.",
                color=discord.Color.green()
            )
            embed.add_field(name="Nom du Serveur", value=f"{before.name} → {after.name}", inline=False)

            # Ajouter d'autres modifications si nécessaires (par exemple, les icônes ou les paramètres de vérification)
            if before.icon != after.icon:
                embed.add_field(name="Icône du Serveur", value="L'icône a été changée.", inline=False)

            if before.verification_level != after.verification_level:
                embed.add_field(name="Niveau de vérification", value=f"Avant : {before.verification_level}\nAprès : {after.verification_level}", inline=False)

            embed.set_footer(text="Mise à jour du serveur PROJECT_DELTA")
            embed.timestamp = discord.utils.utcnow()

            await channel.send(embed=embed)

# --- Webhooks update ---
@bot.event
async def on_webhooks_update(guild, channel):
    if guild.id == ETHERYA_SERVER_ID:
        webhook_channel = get_log_channel(guild, "webhooks")
        if webhook_channel:
            embed = discord.Embed(
                title="🛰️ Mise à Jour des Webhooks",
                description=f"Les webhooks ont été mis à jour dans le salon **{channel.name}**.",
                color=discord.Color.purple()
            )
            embed.add_field(name="Nom du Salon", value=channel.name, inline=False)
            embed.add_field(name="ID du Salon", value=str(channel.id), inline=False)
            embed.set_footer(text="Mise à jour des webhooks")
            embed.timestamp = discord.utils.utcnow()

            await webhook_channel.send(embed=embed)

@bot.event
async def on_member_ban(guild, user):
    guild_id = str(guild.id)
    # --- Logs de ban pour PROJECT_DELTA ---
    if guild.id == ETHERYA_SERVER_ID:
        channel = get_log_channel(guild, "sanctions")
        if channel:
            embed = discord.Embed(
                title="🔨 Membre Banni",
                description=f"Le membre **{user.mention}** a été banni du serveur.",
                color=discord.Color.red()
            )
            embed.add_field(name="ID du Membre", value=str(user.id), inline=False)
            embed.set_footer(text="Ban sur PROJECT_DELTA")
            embed.timestamp = discord.utils.utcnow()

            await channel.send(embed=embed)

# --- Logs de débannissement ---
@bot.event
async def on_member_unban(guild, user):
    if guild.id == ETHERYA_SERVER_ID:
        channel = get_log_channel(guild, "sanctions")
        if channel:
            embed = discord.Embed(
                title="🔓 Membre Débanni",
                description=f"Le membre **{user.mention}** a été débanni du serveur.",
                color=discord.Color.green()
            )
            embed.add_field(name="ID du Membre", value=str(user.id), inline=False)
            embed.set_footer(text="Débannissement sur PROJECT_DELTA")
            embed.timestamp = discord.utils.utcnow()

            await channel.send(embed=embed)

# --- Bot logs ---
@bot.event
async def on_guild_update(before, after):
    if before.id == ETHERYA_SERVER_ID:
        bot_channel = get_log_channel(after, "bots")
        if bot_channel:
            embed = discord.Embed(
                title="🤖 Mise à Jour du Serveur",
                description=f"Le serveur **{before.name}** a été mis à jour.",
                color=discord.Color.blue()
            )
            embed.add_field(name="Nom du Serveur", value=f"{before.name} → {after.name}", inline=False)

            # Ajouter d'autres informations si nécessaire
            if before.icon != after.icon:
                embed.add_field(name="Icône du Serveur", value="L'icône a été changée.", inline=False)

            embed.set_footer(text="Mise à jour du serveur sur PROJECT_DELTA")
            embed.timestamp = discord.utils.utcnow()

            await bot_channel.send(embed=embed)


# --- MODAL POUR FERMETURE ---
class TicketModal(ui.Modal, title="Fermer le ticket"):
    reason = ui.TextInput(label="Raison de fermeture", style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        channel = interaction.channel
        guild = interaction.guild
        reason = self.reason.value

        transcript_channel = guild.get_channel(TRANSCRIPT_CHANNEL_ID)

        # Génération du transcript
        messages = [msg async for msg in channel.history(limit=None)]
        transcript_text = "\n".join([
            f"{msg.created_at.strftime('%Y-%m-%d %H:%M')} - {msg.author}: {msg.content}"
            for msg in messages if msg.content
        ])
        file = discord.File(fp=io.StringIO(transcript_text), filename="transcript.txt")

        # Récupération de qui a ouvert et claim
        ether_ticket_data = collection62.find_one({"channel_id": str(channel.id)})

        opened_by = guild.get_member(int(ticket_data["user_id"])) if ticket_data else None
        claimed_by = None
        # Recherche dans le dernier message envoyé contenant l'embed de création
        async for msg in channel.history(limit=50):
            if msg.embeds:
                embed = msg.embeds[0]
                if embed.footer and "Claimé par" in embed.footer.text:
                    user_id = int(embed.footer.text.split("Claimé par ")[-1].replace(">", "").replace("<@", ""))
                    claimed_by = guild.get_member(user_id)
                    break

        # Log dans le canal transcript
        embed_log = discord.Embed(
            title="📁 Ticket Fermé",
            color=discord.Color.red()
        )
        embed_log.add_field(name="Ouvert par", value=opened_by.mention if opened_by else "Inconnu", inline=True)
        embed_log.add_field(name="Claimé par", value=claimed_by.mention if claimed_by else "Non claim", inline=True)
        embed_log.add_field(name="Fermé par", value=interaction.user.mention, inline=True)
        embed_log.add_field(name="Raison", value=reason, inline=False)
        embed_log.set_footer(text=f"Ticket: {channel.name} | ID: {channel.id}")
        embed_log.timestamp = discord.utils.utcnow()

        await transcript_channel.send(embed=embed_log, file=file)

        # Suppression du channel
        await interaction.response.send_message("✅ Ticket fermé.", ephemeral=True)
        await channel.delete()

# --- VIEW AVEC CLAIM & FERMETURE ---
class ClaimCloseView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Claim", style=ButtonStyle.blurple, custom_id="claim")
    async def claim_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if SUPPORT_ROLE_ID not in [role.id for role in interaction.user.roles]:
            return await interaction.response.send_message("❌ Tu n'as pas la permission de claim.", ephemeral=True)

        # Désactive le bouton
        button.disabled = True
        await interaction.message.edit(view=self)

        # Ajoute une note dans le footer de l'embed
        embed = interaction.message.embeds[0]
        embed.set_footer(text=f"Claimé par {interaction.user.mention}")
        await interaction.message.edit(embed=embed)

        await interaction.response.send_message(f"📌 Ticket claim par {interaction.user.mention}.")

    @ui.button(label="Fermer", style=ButtonStyle.red, custom_id="close")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TicketModal())

class TicketView(ui.View):
    def __init__(self, author_id):
        super().__init__(timeout=None)
        self.author_id = author_id

    @ui.button(label="Support Finance", style=ButtonStyle.primary, custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
    
        guild = interaction.guild
        category = guild.get_channel(1355157940243529789)  # ← Catégorie spécifique

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        channel_name = f"︱🚫・{interaction.user.name}"
        ticket_channel = await guild.create_text_channel(
            name=channel_name,
            overwrites=overwrites,
            category=category  # ← Ajout ici
        )

        # Mention puis suppression du message
        await ticket_channel.send("@everyone")
        await ticket_channel.purge(limit=1)

        # Embed d'accueil
        embed = discord.Embed(
            title="Bienvenue dans votre ticket commande",
            description=(
                """Bienvenue dans le support des Finances !
                Avant de continuer, merci de respecter ces règles :
                Restez respectueux envers l’équipe.
                Répondez rapidement pour éviter de ralentir le traitement de votre demande.

                Informations à fournir dès l’ouverture du ticket :
                La raison de votre demande

                Temps de réponse estimé : 1 à 5 minutes.

                Merci de votre patience et de votre compréhension !"""
            ),
            color=0x5865F2
        )
        embed.set_image(url="https://github.com/Iseyg91/KNSKS-ET/blob/main/Images_GITHUB/Capture_decran_2025-02-15_231405.png?raw=true")

        # Envoi de l’embed avec les boutons
        await ticket_channel.send(embed=embed, view=ClaimCloseView())

        # Sauvegarde MongoDB
        collection16.insert_one({
            "guild_id": str(guild.id),
            "user_id": str(interaction.user.id),
            "channel_id": str(ticket_channel.id),
            "opened_at": datetime.utcnow(),
            "status": "open"
        })

        await interaction.response.send_message(f"✅ Ton ticket a été créé : {ticket_channel.mention}", ephemeral=True)

# --- COMMANDE PANEL ---
@bot.command(name="panel")
async def panel(ctx):
    if ctx.author.id != ISEY_ID:
        return await ctx.send("❌ Tu n'es pas autorisé à utiliser cette commande.")

    embed = discord.Embed(
        title="Support Finanace",
        description="Besoin d'aide ou de contacter un Trésorier pour un achat, une vente ou des questions fiscales ? Ouvrez un ticket !",
        color=0x6A0DAD
    )
    
    # Ajouter une image à l'embed
    embed.set_image(url="https://github.com/Iseyg91/KNSKS-ET/blob/main/Images_GITHUB/Capture_decran_2025-02-15_231405.png?raw=true")

    await ctx.send(embed=embed, view=TicketView(author_id=ctx.author.id))

# --- PANEL2 ---
@bot.command(name="panel2")
async def panel2(ctx):
    if ctx.author.id != ISEY_ID:
        return await ctx.send("❌ Tu n'es pas autorisé à utiliser cette commande.")

    embed = discord.Embed(
        title="Support ",
        description="Ouvrez un ticket afin de contacter le Staff de Etherya !",
        color=0x2ecc71
    )
    # Mise à jour du bouton avec l'emoji 🎨
    await ctx.send(embed=embed, view=TicketView(author_id=ctx.author.id))

# Token pour démarrer le bot (à partir des secrets)
# Lancer le bot avec ton token depuis l'environnement  
keep_alive()
bot.run(token)
