import time, datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper.database import find_one, used_limit
from helper.database import daily as daily_
from datetime import datetime
from datetime import date as date_
from helper.progress import humanbytes
from helper.database import daily as daily_
from helper.date import check_expi
from helper.database import uploadlimit, usertype


@Client.on_message(filters.private & filters.command(["myplan"]))
async def start(client, message):
    used_ = find_one(message.from_user.id)
    daily = used_["daily"]
    expi = daily - int(time.mktime(time.strptime(str(date_.today()), '%Y-%m-%d')))
    
    if expi != 0:
        today = date_.today()
        pattern = '%Y-%m-%d'
        epcho = int(time.mktime(time.strptime(str(today), pattern)))
        daily_(message.from_user.id, epcho)
        used_limit(message.from_user.id, 0)
    
    _newus = find_one(message.from_user.id)
    used = _newus["used_limit"]
    limit = _newus["uploadlimit"]
    remain = int(limit) - int(used)
    user = _newus["usertype"]
    ends = _newus["prexdate"]
    
    if ends:
        pre_check = check_expi(ends)
        if pre_check == False:
            uploadlimit(message.from_user.id, 2147483652)
            usertype(message.from_user.id, "Gratuit")
    
    if ends is None:
        text = (f"<b>ID utilisateur :</b> <code>{message.from_user.id}</code>\n"
                f"<b>Nom :</b> {message.from_user.mention}\n\n"
                f"<b>🏷 Plan :</b> {user}\n\n"
                f"✓ Téléversement de fichiers jusqu'à 2 Go\n"
                f"✓ Téléversement quotidien : {humanbytes(limit)}\n"
                f"✓ Utilisé aujourd'hui : {humanbytes(used)}\n"
                f"✓ Restant : {humanbytes(remain)}\n"
                f"✓ Temps d'attente : 2 minutes\n"
                f"✓ Processus parallèles : Illimités\n"
                f"✓ Intervalle entre les tâches : Oui\n\n"
                f"<b>Validité :</b> À vie")
    else:
        normal_date = datetime.fromtimestamp(ends).strftime('%Y-%m-%d')
        text = (f"<b>ID utilisateur :</b> <code>{message.from_user.id}</code>\n"
                f"<b>Nom :</b> {message.from_user.mention}\n\n"
                f"<b>🏷 Plan :</b> {user}\n\n"
                f"✓ Priorité élevée\n"
                f"✓ Téléversement de fichiers jusqu'à 4 Go\n"
                f"✓ Téléversement quotidien : {humanbytes(limit)}\n"
                f"✓ Utilisé aujourd'hui : {humanbytes(used)}\n"
                f"✓ Restant : {humanbytes(remain)}\n"
                f"✓ Temps d'attente : 0 seconde\n"
                f"✓ Processus parallèles : Illimités\n"
                f"✓ Intervalle entre les tâches : Oui\n\n"
                f"<b>Votre abonnement expire le :</b> {normal_date}")

    if user == "Gratuit":
        await message.reply(
            text, 
            quote=True, 
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 Mettre à niveau", callback_data="upgrade"),
                 InlineKeyboardButton("✖️ Annuler", callback_data="cancel")]
            ])
        )
    else:
        await message.reply(
            text, 
            quote=True, 
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✖️ Annuler ✖️", callback_data="cancel")]
            ])
        )


# Jishu Developer 
# Ne supprimez pas le crédit 🥺
# Chaîne Telegram : @Madflix_Bots
# Chaîne de secours : @JishuBotz
# Développeur : @JishuDeveloper & @MadflixOfficials
