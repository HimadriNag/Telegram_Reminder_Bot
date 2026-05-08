import json
import os
from dotenv import load_dotenv
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")



def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except:
        return {}



def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = (
        "Hello Himadri 👋\n\n"
        "Send me your daily tasks.\n"
        "I will remind you at:\n\n"
        "🕗 6 AM\n"
        "🕑 2 PM\n"
        "🌙 6 PM\n\n"
        "Example:\n"
        "- Attend Signals class\n"
        "- Solve DSA\n"
        "- Revise Analog Circuits"
    )

    await update.message.reply_text(message)





async def save_user_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.message.chat_id)

    text = update.message.text

    tasks = load_tasks()

    tasks[user_id] = {
        "tasks": text,
        "date": str(datetime.now())
    }

    save_tasks(tasks)

    await update.message.reply_text(
        "✅ Tasks saved successfully!\n\n"
        "You will receive reminders at:\n"
        "🕗 6 AM\n"
        "🕑 2 PM\n"
        "🌙 6 PM"
    )



async def send_morning_reminder(app):

    tasks = load_tasks()

    for user_id, data in tasks.items():

        task_text = data["tasks"]

        message = (
            "🌞 GOOD MORNING!\n\n"
            "📌 Today's Tasks:\n\n"
            f"{task_text}\n\n"
            "🔥 Start strong!"
        )

        try:
            await app.bot.send_message(
                chat_id=int(user_id),
                text=message
            )

        except Exception as e:
            print(e)



async def send_afternoon_reminder(app):

    tasks = load_tasks()

    for user_id, data in tasks.items():

        task_text = data["tasks"]

        message = (
            "☀️ AFTERNOON REMINDER\n\n"
            "📌 Your Tasks:\n\n"
            f"{task_text}\n\n"
            "⚡ Stay focused!"
        )

        try:
            await app.bot.send_message(
                chat_id=int(user_id),
                text=message
            )

        except Exception as e:
            print(e)


async def send_night_reminder(app):

    tasks = load_tasks()

    for user_id, data in tasks.items():

        task_text = data["tasks"]

        message = (
            "🌙 NIGHT REMINDER\n\n"
            "📌 Remaining Tasks:\n\n"
            f"{task_text}\n\n"
            "🔥 Finish your day strong!"
        )

        try:
            await app.bot.send_message(
                chat_id=int(user_id),
                text=message
            )

        except Exception as e:
            print(e)



def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Start command
    app.add_handler(CommandHandler("start", start))

    # Save text messages
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            save_user_tasks
        )
    )

    # Scheduler
    scheduler = AsyncIOScheduler()

    # 6 AM
    scheduler.add_job(
        send_morning_reminder,
        trigger="cron",
        hour=6,
        minute=0,
        args=[app]
    )

    # 2 PM
    scheduler.add_job(
        send_afternoon_reminder,
        trigger="cron",
        hour=14,
        minute=0,
        args=[app]
    )

    # 6 PM
    scheduler.add_job(
        send_night_reminder,
        trigger="cron",
        hour=18,
        minute=0,
        args=[app]
    )

    scheduler.start()

    print("✅ Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()