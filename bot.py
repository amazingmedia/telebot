import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post
    if not message:
        return

    file = None
    if message.video:
        file = message.video
    elif message.document:
        file = message.document

    if not file:
        return

    tg_file = await context.bot.get_file(file.file_id)
    direct_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{tg_file.file_path}"

    await context.bot.send_message(
        chat_id=message.chat_id,
        text=f"🎬 Direct Link:\n{direct_link}"
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))
    print("Bot is running...")
    app.run_polling()
