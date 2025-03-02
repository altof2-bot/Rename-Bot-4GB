from datetime import date as date_
import os, re, datetime, random, asyncio, time, humanize
from script import *
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram import Client, filters, enums
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from helper.progress import humanbytes
from helper.database import botdata, find_one, total_user
from helper.database import insert, find_one, used_limit, usertype, uploadlimit, addpredata, total_rename, total_size
from pyrogram.file_id import FileId
from helper.database import daily as daily_
from helper.date import check_expi
from config import *

token = BOT_TOKEN
botid = token.split(':')[0]

@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user_id = message.chat.id
    old = insert(int(user_id))
    
    try:
        id = message.text.split(' ')[1]
    except IndexError:
        id = None

    loading_sticker_message = await message.reply_sticker("CAACAgIAAxkBAALmzGXSSt3ppnOsSl_spnAP8wHC26jpAAJEGQACCOHZSVKp6_XqghKoHgQ")
    await asyncio.sleep(2)
    await loading_sticker_message.delete()
    
    text = f"""Bonjour {message.from_user.mention} \n\n➻ Ceci est un bot de renommage avancé et puissant.\n\n➻ Avec ce bot, vous pouvez renommer et modifier la miniature de vos fichiers.\n\n➻ Vous pouvez également convertir une vidéo en fichier et un fichier en vidéo.\n\n➻ Ce bot supporte aussi la miniature personnalisée et la légende personnalisée.\n\n<b>Bot créé par @altof2</b>"""
    
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Mises à jour", url="https://t.me/sineur_x_bot"),
         InlineKeyboardButton("💬 Support", url="https://t.me/sineur_x_bot")],
        [InlineKeyboardButton("🛠️ Aide", callback_data='help'),
         InlineKeyboardButton("❤️‍🩹 À propos", callback_data='about')],
        [InlineKeyboardButton("🧑‍💻 Développeur 🧑‍💻", url="https://t.me/altof2")]
        ])
    
    await message.reply_photo(
        photo=START_PIC,
        caption=text,
        reply_markup=button,
        quote=True
        )
    return    

@Client.on_message((filters.private & (filters.document | filters.audio | filters.video)) | filters.channel & (filters.document | filters.audio | filters.video))
async def send_doc(client, message):
    user_id = message.chat.id
    old = insert(int(user_id))
        
    user_id = message.from_user.id    
    if FORCE_SUBS:
        try:
            await client.get_chat_member(FORCE_SUBS, user_id)
        except UserNotParticipant:
            _newus = find_one(message.from_user.id)
            user = _newus["usertype"]
            await message.reply_text("<b>Bonjour,\n\nVous devez rejoindre mon canal pour pouvoir m'utiliser.\n\nVeuillez rejoindre le canal, s'il vous plaît.</b>",
                                     reply_to_message_id=message.id,
                                     reply_markup=InlineKeyboardMarkup([
                                         [InlineKeyboardButton("🔺 Canal de mise à jour 🔺", url=f"https://t.me/{FORCE_SUBS}")]
                                         ]))
            await client.send_message(LOG_CHANNEL, f"<b><u>Nouveau utilisateur a démarré le bot</u></b> \n\n<b>ID utilisateur :</b> <code>{user_id}</code> \n<b>Prénom :</b> {message.from_user.first_name} \n<b>Nom :</b> {message.from_user.last_name} \n<b>Nom d'utilisateur :</b> @{message.from_user.username} \n<b>Mention :</b> {message.from_user.mention} \n<b>Lien utilisateur :</b> <a href='tg://openmessage?user_id={user_id}'>Cliquez ici</a> \n<b>Plan utilisateur :</b> {user}")
            return
		
    botdata(int(botid))
    bot_data = find_one(int(botid))
    prrename = bot_data['total_rename']
    prsize = bot_data['total_size']
    user_deta = find_one(user_id)
    used_date = user_deta["date"]
    buy_date = user_deta["prexdate"]
    daily = user_deta["daily"]
    user_type = user_deta["usertype"]

    c_time = time.time()

    if user_type == "Free":
        LIMIT = 120
    else:
        LIMIT = 10
    then = used_date + LIMIT
    left = round(then - c_time)
    conversion = datetime.timedelta(seconds=left)
    ltime = str(conversion)
    if left > 0:
        await message.reply_text(f"<b>Désolé, je ne suis pas réservé uniquement pour vous.\n\nLe contrôle anti-spam est activé, veuillez patienter {ltime}.</b>", reply_to_message_id=message.id)
    else:
        # Transférer un message unique
        media = await client.get_messages(message.chat.id, message.id)
        file = media.document or media.video or media.audio
        dcid = FileId.decode(file.file_id).dc_id
        filename = file.file_name
        file_id = file.file_id
        value = 2147483648
        used_ = find_one(message.from_user.id)
        used = used_["used_limit"]
        limit = used_["uploadlimit"]
        expi = daily - int(time.mktime(time.strptime(str(date_.today()), '%Y-%m-%d')))
        if expi != 0:
            today = date_.today()
            pattern = '%Y-%m-%d'
            epcho = int(time.mktime(time.strptime(str(today), pattern)))
            daily_(message.from_user.id, epcho)
            used_limit(message.from_user.id, 0)
        remain = limit - used
        if remain < int(file.file_size):
            await message.reply_text(f"Le quota quotidien de {humanbytes(limit)} de données est épuisé à 100%.\n\n<b>Taille du fichier détectée :</b> {humanbytes(file.file_size)}\n<b>Quota utilisé :</b> {humanbytes(used)}\n\nIl ne vous reste que <b>{humanbytes(remain)}</b> sur votre compte.\n\nSi vous souhaitez renommer un fichier volumineux, mettez à niveau votre plan.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Mettre à niveau", callback_data="upgrade")]]))
            return
        if value < file.file_size:
            
            if STRING_SESSION:
                if buy_date == None:
                    await message.reply_text(f"Vous ne pouvez pas télécharger un fichier de plus de 2GB.\n\nVotre plan ne permet pas de télécharger des fichiers de plus de 2GB.\n\nMettez à niveau votre plan pour renommer des fichiers de plus de 2GB.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Mettre à niveau", callback_data="upgrade")]]))
                    return
                pre_check = check_expi(buy_date)
                if pre_check == True:
                    await message.reply_text(f"""__Que souhaitez-vous que je fasse avec ce fichier ?__\n\n**Nom du fichier :** `{filename}`\n**Taille du fichier :** {humanize.naturalsize(file.file_size)}\n**DC ID :** {dcid}""", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📝 Renommer", callback_data="rename"), InlineKeyboardButton("✖️ Annuler", callback_data="cancel")]]))
                    total_rename(int(botid), prrename)
                    total_size(int(botid), prsize, file.file_size)
                else:
                    uploadlimit(message.from_user.id, 2147483648)
                    usertype(message.from_user.id, "Free")

                    await message.reply_text(f'Votre plan a expiré le {buy_date}', quote=True)
                    return
            else:
                await message.reply_text("Vous ne pouvez pas télécharger un fichier de plus de 2GB.\n\nVotre plan ne permet pas de télécharger des fichiers de plus de 2GB.\n\nMettez à niveau votre plan pour renommer des fichiers de plus de 2GB.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Mettre à niveau", callback_data="upgrade")]]))
                return
        else:
            if buy_date:
                pre_check = check_expi(buy_date)
                if pre_check == False:
                    uploadlimit(message.from_user.id, 2147483648)
                    usertype(message.from_user.id, "Free")
            
            filesize = humanize.naturalsize(file.file_size)
            fileid = file.file_id
            total_rename(int(botid), prrename)
            total_size(int(botid), prsize, file.file_size)
            await message.reply_text(f"""__Que souhaitez-vous que je fasse avec ce fichier ?__\n\n**Nom du fichier :** `{filename}`\n**Taille du fichier :** {filesize}\n**DC ID :** {dcid}""", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("📝 Renommer", callback_data="rename"),
                  InlineKeyboardButton("✖️ Annuler", callback_data="cancel")]]))
