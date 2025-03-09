from pyrogram.errors import FloodWait
import asyncio
from pyrogram import Client, filters
from helper.database import getid, delete
from config import *


@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["broadcast"]))
async def broadcast(bot, message):
    if message.reply_to_message:
        ms = await message.reply_text("Getting all IDs from the database. Please wait...")
        ids = getid()
        tot = len(ids)
        success = 0
        failed = 0
        await ms.edit(f"Starting broadcast... \n\nSending message to {tot} users")

        for user_id in ids:
            try:
                await asyncio.sleep(1)  # Utilisation de asyncio.sleep pour éviter de bloquer l'exécution
                await message.reply_to_message.copy(user_id)
                success += 1
            except FloodWait as e:
                print(f"FloodWait detected! Waiting for {e.value} seconds...")
                await asyncio.sleep(e.value)
            except Exception as err:
                print(f"Failed to send message to {user_id}: {err}")
                failed += 1
                delete({"_id": user_id})  # Supprime l'ID de la base de données

            try:
                await ms.edit(f"Message sent to {success} chats. \n\n{failed} chats failed to receive the message. \n\nTotal - {tot}")
            except Exception as err:
                print(f"Error updating message: {err}")
