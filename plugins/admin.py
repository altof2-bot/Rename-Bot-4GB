from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from config import *
from pyrogram import Client, filters
from helper.date import add_date
from helper.database import uploadlimit, usertype, addpre

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["warn"]))
async def warn(c, m):
    if len(m.command) >= 3:
        try:
            user_id = m.text.split(' ', 2)[1]
            reason = m.text.split(' ', 2)[2]
            await m.reply_text("Utilisateur notifié avec succès 😁")
            await c.send_message(chat_id=int(user_id), text=reason)
        except:
            await m.reply_text("L'utilisateur n'a pas été notifié avec succès 😔")
            

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["addpremium"]))
async def buypremium(bot, message):
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("🪙 Basique", callback_data="vip1"),
         InlineKeyboardButton("⚡ Standard", callback_data="vip2")],
        [InlineKeyboardButton("💎 Pro", callback_data="vip3")],
        [InlineKeyboardButton("✖️ Annuler ✖️", callback_data="cancel")]
    ])
        
    await message.reply_text("🦋 Sélectionnez un plan pour passer en premium...", quote=True, reply_markup=button)
    

@Client.on_message((filters.channel | filters.private) & filters.user(ADMIN) & filters.command(["ceasepower"]))
async def ceasepremium(bot, message):
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Limite 1GB", callback_data="cp1"),
         InlineKeyboardButton("Désactivation totale", callback_data="cp2")],
        [InlineKeyboardButton("✖️ Annuler ✖️", callback_data="cancel")]
    ])
    
    await message.reply_text("😁 Mode de désactivation des privilèges...", quote=True, reply_markup=button)


@Client.on_message((filters.channel | filters.private) & filters.user(ADMIN) & filters.command(["resetpower"]))
async def resetpower(bot, message):
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Oui", callback_data="dft"),
         InlineKeyboardButton("❌ Non", callback_data="cancel")]
    ])
        
    await message.reply_text(text="Voulez-vous vraiment réinitialiser la limite quotidienne à la limite par défaut de 2GB ?", quote=True, reply_markup=button)
    
    
# MODE PREMIUM POWER @JISHUDEVELOPER
@Client.on_callback_query(filters.regex('vip1'))
async def vip1(bot, update):
    id = update.message.reply_to_message.text.split("/addpremium")
    user_id = id[1].replace(" ", "")
    inlimit = 21474836500
    uploadlimit(int(user_id), 21474836500)
    usertype(int(user_id), "🪙 Basique")
    addpre(int(user_id))
    await update.message.edit("Ajouté avec succès à la limite de téléchargement premium de 20 GB")
    await bot.send_message(user_id, f"Salut {update.from_user.mention} \n\nVous avez été mis à niveau vers <b>🪙 Basique</b>. Consultez votre plan ici /myplan")


@Client.on_callback_query(filters.regex('vip2'))
async def vip2(bot, update):
    id = update.message.reply_to_message.text.split("/addpremium")
    user_id = id[1].replace(" ", "")
    inlimit = 53687091200
    uploadlimit(int(user_id), 53687091200)
    usertype(int(user_id), "⚡ Standard")
    addpre(int(user_id))
    await update.message.edit("Ajouté avec succès à la limite de téléchargement premium de 50 GB")
    await bot.send_message(user_id, f"Salut {update.from_user.mention} \n\nVous avez été mis à niveau vers <b>⚡ Standard</b>. Consultez votre plan ici /myplan")


@Client.on_callback_query(filters.regex('vip3'))
async def vip3(bot, update):
    id = update.message.reply_to_message.text.split("/addpremium")
    user_id = id[1].replace(" ", "")
    inlimit = 107374182400
    uploadlimit(int(user_id), 107374182400)
    usertype(int(user_id), "💎 Pro")
    addpre(int(user_id))
    await update.message.edit("Ajouté avec succès à la limite de téléchargement premium de 100 GB")
    await bot.send_message(user_id, f"Salut {update.from_user.mention} \n\nVous avez été mis à niveau vers <b>💎 Pro</b>. Consultez votre plan ici /myplan")



# MODE CEASE POWER @JISHUDEVELOPER
@Client.on_callback_query(filters.regex('cp1'))
async def cp1(bot, update):
    id = update.message.reply_to_message.text.split("/ceasepower")
    user_id = id[1].replace(" ", "")
    inlimit = 2147483652
    uploadlimit(int(user_id), 2147483652)
    usertype(int(user_id), "⚠️ Compte rétrogradé")
    addpre(int(user_id))
    await update.message.edit("Ajouté avec succès à la limite de téléchargement de 2GB")
    await bot.send_message(user_id, f"Salut {update.from_user.mention} \n\nVous avez été rétrogradé à la limite de <b>2GB</b>. Consultez votre plan ici /myplan \n\n<b>Contactez l'administrateur :</b> @MadflixOfficials")


@Client.on_callback_query(filters.regex('cp2'))
async def cp2(bot, update):
    id = update.message.reply_to_message.text.split("/ceasepower")
    user_id = id[1].replace(" ", "")
    inlimit = 0
    uploadlimit(int(user_id), 0)
    usertype(int(user_id), "⚠️ Compte rétrogradé")
    addpre(int(user_id))
    await update.message.edit("Ajouté avec succès à la limite de téléchargement de 0GB")
    await bot.send_message(user_id, f"Salut {update.from_user.mention} \n\nVous avez été rétrogradé à la limite de <b>0GB</b>. Consultez votre plan ici /myplan \n\n<b>Contactez l'administrateur :</b> @MadflixOfficials")



# MODE RESET POWER @JISHUDEVELOPER
@Client.on_callback_query(filters.regex('dft'))
async def dft(bot, update):
    id = update.message.reply_to_message.text.split("/resetpower")
    user_id = id[1].replace(" ", "")
    inlimit = 2147483652
    uploadlimit(int(user_id), 2147483652)
    usertype(int(user_id), "🆓 Free")
    addpre(int(user_id))
    await update.message.edit("La limite quotidienne de données a été réinitialisée avec succès.\n\nCe compte dispose par défaut d'une capacité restante de 2GB")
    await bot.send_message(user_id, f"Salut {update.from_user.mention} \n\nVotre limite quotidienne de données a été réinitialisée avec succès. Consultez votre plan ici /myplan\n\n<b>Contactez l'administrateur :</b> @MadflixOfficials")

# Jishu Developer 
# Ne supprimez pas le crédit 🥺
# Chaîne Telegram : @Madflix_Bots
# Chaîne de secours : @JishuBotz
# Développeur : @JishuDeveloper & @MadflixOfficials
