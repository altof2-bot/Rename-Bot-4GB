import os, sys, asyncio
from config import *
from pyrogram import filters, Client

@Client.on_message(filters.command("restart") & filters.user(ADMIN))
async def stop_button(bot, message):
    msg = await bot.send_message(text="🔄 Processus arrêtés. Le bot redémarre...", chat_id=message.chat.id)
    await asyncio.sleep(3)
    await msg.edit("✅️ Le bot a redémarré. Vous pouvez maintenant m'utiliser.")
    os.execl(sys.executable, sys.executable, *sys.argv)

# Jishu Developer 
# Ne supprimez pas le crédit 🥺
# Chaîne Telegram : @Madflix_Bots
# Chaîne de secours : @JishuBotz
# Développeur : @JishuDeveloper & @MadflixOfficials
