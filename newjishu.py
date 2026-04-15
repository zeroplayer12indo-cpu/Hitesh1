import asyncio
import json
import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from telegram.request import HTTPXRequest

# --- CONFIGURATION ---
TOKEN = "8635540065:AAFABE78uPMP9z_fe7BPBK7Nt3BCC51cpbY"
ADMIN_CHAT_ID = 8706083203
VIDEO_FILE = "videos.json"
QR_IMAGE_URL = "https://repgyetdcodkynrbxocg.supabase.co/storage/v1/object/public/images/telegram-1776006097119-e53b66c4.jpg" 
WELCOME_IMAGE_URL = "https://i.ibb.co/wNSBv26D/IMG-20260411-141508-854.jpg"

# Links for buttons
PAYMENT_PROOF_LINK = "https://t.me/feedbacksproofsaofia"
ADMIN_USERNAME = "@Sofiavideoprovider"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

admin_temp_list = {}

def load_videos():
    if not os.path.exists(VIDEO_FILE): return []
    try:
        with open(VIDEO_FILE, 'r') as f: return json.load(f)
    except: return []

# --- KEYBOARDS ---

def get_main_reply_keyboard():
    keyboard = [
        [KeyboardButton("🛍️ Products"), KeyboardButton("🔓 Unlock Premium")],
        [KeyboardButton("🎥 Demo"), KeyboardButton("👤 Contact Admin")],
        [KeyboardButton("📸 Submit Screenshot")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_main_inline_keyboard():
    # Exactly 3 buttons as requested
    keyboard = [
        [InlineKeyboardButton("👀 VIEW PROOF", url=PAYMENT_PROOF_LINK)],
        [InlineKeyboardButton("💰 BUY NOW", callback_data='buy_now')],
        [InlineKeyboardButton("👤 CONTACT ADMIN", url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_video_access_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔞 Get Access ₹49 🔞", callback_data="get_access_49")],
        [InlineKeyboardButton("👶 ONLY KIDS VIDEO ₹99 👶", callback_data="kids_video_99")],
        [InlineKeyboardButton("50k FRESH K!DS ₹179", callback_data="kids_179")],
        [InlineKeyboardButton("ACTRESS HIDEN CAME ₹79", callback_data="actress_99")],
        [InlineKeyboardButton("15K ADULT VIDEOS ₹69", callback_data="adult_69")],
        [InlineKeyboardButton("5 GROUP ENTRY 299₹", callback_data="group_299")]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- CAPTIONS ---
VIDEO_CAPTION = (
    "<b>🔞 VVIP MEGA COLLECTION 2026 🔞</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "✨ <b>𝐀𝐋𝐋 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐂𝐀𝐓𝐄𝐆𝐎𝐑𝐈𝐄𝐒:</b>\n\n"
    "📌 MOM-SON 🤤💦\n"
    "📌 DESI BHABHI 🤤💦\n"
    "📌 INSTAGR@M STAR 🤤💦\n"
    "📌 TEEN INDIAN 🤤💦\n"
    "📌 BR@THER-SISTER 🤤💦\n"
    "📌 AUNTY-P*RN 🤤💦\n"
    "📌 FOREIGNER 🤤💦\n"
    "📌 LESBIAN P@N 🔞🔥\n"
    "📌 HIDDEN C@M 🤫💦\n"
    "📌 SCHOOL GIRL 🎒🍑\n"
    "📌 STEP-SISTER 💋🔥\n"
    "📌 COLLEGE ROM@NCE 🎓💦\n"
    "🔥 𝐀𝐮𝐧𝐭𝐲 &amp; 𝐇𝐨𝐮𝐬𝐞𝐰𝐢𝐟𝐞 🤤💦\n\n"
    "✨ <b>NOTE: DAILY 1,00,000+ NEW MMS UPLOADS!</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "💎 <b>FULL ACCESS ONLY AT: ₹199/- ✅</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━"
)

QR_CAPTION_49 = (
    "🚀 <b>PREMIUM ACCESS UNLOCKED</b> 🚀\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "💰 <b>PAYMENT:</b> ⚡️ <b>₹49</b> ⚡️\n"
    "📍 <b>UPI ID:</b> <code>krishnagod999@fam</code>\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "1️⃣ QR Scan karke ₹49 Pay karein.\n"
    "2️⃣ Screenshot lein.\n"
    "3️⃣ Niche <b>'✅ MENE PAYMENT KRDIYA'</b> dabayein."
)

QR_CAPTION_99 = (
    "👶 <b>ONLY KIDS VIDEO ACCESS</b> 👶\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "💰 <b>PAYMENT:</b> ⚡️ <b>₹99</b> ⚡️\n"
    "📍 <b>UPI ID:</b> <code>krishnagod999@fam</code>\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "1️⃣ QR Scan karke ₹99 Pay karein.\n"
    "2️⃣ Screenshot lein.\n"
    "3️⃣ Niche <b>'✅ MENE PAYMENT KRDIYA'</b> dabayein."
)

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    
    welcome_text = (
        "<b>Welcome to our Premium Digital Store!</b>\n\n"
        "Browse our exclusive collections and unlock lifetime access to premium content.\n\n"
        "Click below to explore our products or get premium access."
    )

    try:
        # Send Welcome Photo with 3 Inline Buttons
        await update.message.reply_photo(
            photo=WELCOME_IMAGE_URL,
            caption=welcome_text,
            reply_markup=get_main_inline_keyboard(),
            parse_mode='HTML'
        )
        # Send Reply Keyboard
        await update.message.reply_text(
            "Use the menu below to navigate:",
            reply_markup=get_main_reply_keyboard()
        )
    except Exception as e:
        logging.error(f"Error in start: {e}")
        await update.message.reply_text(welcome_text, reply_markup=get_main_inline_keyboard(), parse_mode='HTML')

    # Original logic: Show videos
    videos_list = load_videos()
    if not videos_list: return

    for vid in videos_list[:10]: 
        try:
            await update.message.reply_video(
                video=vid,
                caption=VIDEO_CAPTION,
                parse_mode='HTML',
                reply_markup=get_video_access_keyboard()
            )
            await asyncio.sleep(0.5)
        except: continue

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query: return
    await query.answer()

    if query.data == "buy_now":
        await query.message.reply_text("✨ <b>Choose a category to buy:</b>", reply_markup=get_video_access_keyboard(), parse_mode='HTML')

    elif query.data == "get_access_49":
        keyboard = [[InlineKeyboardButton("✅ MENE PAYMENT KRDIYA ✅", callback_data="paid_proof")]]
        await query.message.reply_photo(photo=QR_IMAGE_URL, caption=QR_CAPTION_49, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "kids_video_99":
        keyboard = [[InlineKeyboardButton("✅ MENE PAYMENT KRDIYA ✅", callback_data="paid_proof")]]
        await query.message.reply_photo(photo=QR_IMAGE_URL, caption=QR_CAPTION_99, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "kids_179":
        keyboard = [[InlineKeyboardButton("✅ MENE PAYMENT KRDIYA ✅", callback_data="paid_proof")]]
        await query.message.reply_photo(photo=QR_IMAGE_URL, caption="50k FRESH K!DS ₹179\n\nUPI: krishnagod999@fam", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "actress_99":
        keyboard = [[InlineKeyboardButton("✅ MENE PAYMENT KRDIYA ✅", callback_data="paid_proof")]]
        await query.message.reply_photo(photo=QR_IMAGE_URL, caption="ACTRESS HIDEN CAME ₹99\n\nUPI: krishnagod999@fam", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "adult_69":
        keyboard = [[InlineKeyboardButton("✅ MENE PAYMENT KRDIYA ✅", callback_data="paid_proof")]]
        await query.message.reply_photo(photo=QR_IMAGE_URL, caption="15K ADULT VIDEOS ₹69\n\nUPI: krishnagod999@fam", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "group_299":
        keyboard = [[InlineKeyboardButton("✅ MENE PAYMENT KRDIYA ✅", callback_data="paid_proof")]]
        await query.message.reply_photo(photo=QR_IMAGE_URL, caption="5 GROUP ENTRY 299₹\n\nUPI: krishnagod999@fam", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "paid_proof":
        final_msg = f"<b>✅ PAYMENT PROOFS DO!</b>\n\nBhai, abhi <b>{ADMIN_USERNAME}</b> par payment ka <b>Screenshot</b> bhejo.\n\nProof check hote hi Link mil jayega! 🔥⚡"
        await query.message.reply_text(final_msg, parse_mode='HTML')

    elif query.data == "save_permanent":
        if ADMIN_CHAT_ID in admin_temp_list and admin_temp_list[ADMIN_CHAT_ID]:
            current_videos = load_videos()
            current_videos.extend(admin_temp_list[ADMIN_CHAT_ID])
            with open(VIDEO_FILE, 'w') as f: json.dump(current_videos, f)
            count = len(admin_temp_list[ADMIN_CHAT_ID])
            admin_temp_list.pop(ADMIN_CHAT_ID)
            await query.message.edit_text(f"✅ {count} Videos Saved Permanently!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    text = update.message.text
    
    if text == "🛍️ Products":
        await update.message.reply_text("✨ <b>Choose a category:</b>", reply_markup=get_video_access_keyboard(), parse_mode='HTML')
    elif text == "🔓 Unlock Premium":
        keyboard = [[InlineKeyboardButton("✅ MENE PAYMENT KRDIYA ✅", callback_data="paid_proof")]]
        await update.message.reply_photo(photo=QR_IMAGE_URL, caption=QR_CAPTION_49, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
    elif text == "🎥 Demo":
        await update.message.reply_text("🎥 Watch our demo here: https://t.me/your_demo_link")
    elif text == "👤 Contact Admin":
        await update.message.reply_text(f"👤 Contact Admin for support: {ADMIN_USERNAME}")
    elif text == "📸 Submit Screenshot":
        await update.message.reply_text(f"📸 Please send your payment screenshot to: {ADMIN_USERNAME}")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.video: return
    if update.effective_user.id != ADMIN_CHAT_ID: return
    
    if ADMIN_CHAT_ID not in admin_temp_list: admin_temp_list[ADMIN_CHAT_ID] = []
    file_id = update.message.video.file_id
    admin_temp_list[ADMIN_CHAT_ID].append(file_id)
    keyboard = [[InlineKeyboardButton("✅ SAVE PERMANENT", callback_data="save_permanent")]]
    await update.message.reply_text(f"📥 Received! Total queue: {len(admin_temp_list[ADMIN_CHAT_ID])}", reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    t_request = HTTPXRequest(connect_timeout=150, read_timeout=150)
    app = ApplicationBuilder().token(TOKEN).request(t_request).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is LIVE!")
    app.run_polling(drop_pending_updates=True)
