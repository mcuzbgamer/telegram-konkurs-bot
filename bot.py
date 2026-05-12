import random
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# 🔑 TOKEN
TOKEN = "8902027223:AAHd9510R51kq9WKTkWaSxQ-y11QsLGuzhg

# 📢 Kanallar
CHANNELS = ["@fazkooo", "@kanal2", "@kanal3"]

# 👑 ADMIN ID
ADMIN_ID = 1594801802

# 📊 DATA
participants = {}
forced_winners = []   # ⭐ TOP 1-2 qo‘lda
random_winners = []


# 🔍 OBUNA TEKSHIRISH
async def check_sub(user_id, bot):
    try:
        for ch in CHANNELS:
            member = await bot.get_chat_member(ch, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        return True
    except:
        return False


# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎉 Qatnashish", callback_data="join")],
        [
            InlineKeyboardButton("Kanal 1", url="https://t.me/fazkooo"),
            InlineKeyboardButton("Kanal 2", url="https://t.me/kanal2"),
        ],
        [InlineKeyboardButton("Kanal 3", url="https://t.me/kanal3")]
    ]

    await update.message.reply_text(
        "🎁 KONKURS!\nQatnashish uchun tugmani bosing:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# 🎯 JOIN
async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    user = q.from_user

    if not await check_sub(user.id, context.bot):
        await q.answer("❌ 3 ta kanalga obuna bo‘ling!", show_alert=True)
        return

    participants[user.id] = user.username or user.first_name
    await q.answer("✅ Siz ro‘yxatga qo‘shildingiz!")


# ⭐ TOP WINNER QO‘SHISH (ADMIN)
async def setwinner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage: /setwinner user_id")
        return

    uid = int(context.args[0])

    if uid in participants and uid not in forced_winners:
        forced_winners.append(uid)
        await update.message.reply_text("⭐ TOP winner qo‘shildi")
    else:
        await update.message.reply_text("❌ User topilmadi yoki allaqachon qo‘shilgan")


# 🏆 WINNER DRAW (23 TA: 2 TOP + 21 RANDOM)
async def drawwinners(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    total_winners = 23
    top_count = len(forced_winners)

    remain = [x for x in participants if x not in forced_winners]

    needed_random = total_winners - top_count

    if needed_random < 0:
        await update.message.reply_text("❌ TOP winner 23 tadan oshib ketdi!")
        return

    if len(remain) < needed_random:
        await update.message.reply_text("❌ Yetarli ishtirokchi yo‘q!")
        return

    random_winners = random.sample(remain, needed_random)

    text = "🏆 WINNERS LIST:\n\n"

    i = 1

    # ⭐ TOP winners (sen tanlagan 1-2)
    for w in forced_winners:
        text += f"⭐ TOP {i}: {participants[w]}\n"
        i += 1

    # 🎲 RANDOM winners (21 ta)
    for w in random_winners:
        text += f"{i}: {participants[w]}\n"
        i += 1

    await update.message.reply_text(text)


# 🚀 BOT START
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(join, pattern="join"))
app.add_handler(CommandHandler("setwinner", setwinner))
app.add_handler(CommandHandler("drawwinners", drawwinners))

app.run_polling()
