from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from pyrogram import Client, filters


@Client.on_callback_query(filters.regex('upgrade'))
async def upgrade(bot, update):
    text = """**Utilisateur du Plan Gratuit**  
Limite de téléversement quotidienne : 2 Go  
Prix : 0  

**🪙 Basique**  
Limite de téléversement quotidienne : 20 Go  
Prix : 49 etoile (Inde) / 🌎 0,59$ par mois  

**⚡ Standard**  
Limite de téléversement quotidienne : 50 Go  
Prix : 99 etoile (Inde) / 🌎 1,19$ par mois  

**💎 Pro**  
Limite de téléversement quotidienne : 100 Go  
Prix : 179 etoile (Inde) / 🌎 2,16$ par mois  

**Détails de paiement :**  
<b>➜ UPI ID :</b> <code>@REQUETE_ANIME_30sbot</code>  

Après le paiement, envoyez une capture d'écran de la transaction à l'admin @altof2.
    """
    
    clavier = InlineKeyboardMarkup([
        [InlineKeyboardButton("🦋 Admin", url="https://t.me/calladminrobot"),
        InlineKeyboardButton("✖️ Annuler", callback_data="cancel")]
    ])
    
    await update.message.edit(text=text, reply_markup=clavier, disable_web_page_preview=True)
    

@Client.on_message(filters.private & filters.command(["upgrade"]))
async def upgradecm(bot, message):
    text = """**Utilisateur du Plan Gratuit**  
Limite de téléversement quotidienne : 2 Go  
Prix : 0  

**🪙 Basique**  
Limite de téléversement quotidienne : 20 Go  
Prix : 49 etoile (Inde) / 🌎 0,59$ par mois  

**⚡ Standard**  
Limite de téléversement quotidienne : 50 Go  
Prix : 99 etoile (Inde) / 🌎 1,19$ par mois  

**💎 Pro**  
Limite de téléversement quotidienne : 100 Go  
Prix : 179 etoile (Inde) / 🌎 2,16$ par mois  

**Détails de paiement :**  
<b>➜ UPI ID :</b> <code>@REQUETE_ANIME_30sbot</code>  

Après le paiement, envoyez une capture d'écran de la transaction à l'admin @altof2.
    """
    
    clavier = InlineKeyboardMarkup([
        [InlineKeyboardButton("🦋 Admin", url="https://t.me/calladminrobot"),
        InlineKeyboardButton("✖️ Annuler", callback_data="cancel")]
    ])
    
    await message.reply_text(text=text, reply_markup=clavier, quote=True, disable_web_page_preview=True)
