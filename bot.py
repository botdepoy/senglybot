import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 机器人正常运行！\n\n"
        "修改群名：\n"
        "/rename 新群名称"
    )


async def rename(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("❌ 请在群里使用")
        return

    if not context.args:
        await update.message.reply_text(
            "❌ 请填写群名称\n\n"
            "例如：\n"
            "/rename 招聘交流群"
        )
        return

    new_title = " ".join(context.args)

    try:
        await context.bot.set_chat_title(
            chat_id=chat.id,
            title=new_title
        )

        await update.message.reply_text(
            f"✅ 群名称修改成功！\n\n"
            f"新名称：{new_title}"
        )

        print(f"✅ 群名已修改：{new_title}")

    except Exception as e:
        await update.message.reply_text(f"❌ 修改失败：\n{e}")
        print(f"❌ 错误：{e}")


def main():
    print("🤖 改群名机器人正在启动")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rename", rename))

    print("✅ 机器人启动成功")
    app.run_polling()


if __name__ == "__main__":
    main()
