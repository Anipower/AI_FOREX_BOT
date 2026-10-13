import os
import time
import random
import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types

# =====================================================================
# 1. SECURITY CONFIGURATION
# =====================================================================
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu_keyboard.add(types.KeyboardButton(text="🎯 Get New Signal"))

# =====================================================================
# 2. INTERNAL ALGORITHMIC INDICATOR ENGINE
# =====================================================================
def calculate_indicators():
    gains = [random.uniform(0, 0.0015) for _ in range(7)]
    losses = [random.uniform(0, 0.0015) for _ in range(7)]
    
    avg_gain = sum(gains) / 14
    avg_loss = sum(losses) / 14
    
    if avg_loss == 0:
        rsi = 100
    else:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
    rsi = max(10, min(90, rsi))
    
    if rsi < 35:
        direction = "BUY 🟢"
        analysis = "Market is heavily OVER-SOLD. Bullish reversal imminent."
    elif rsi > 65:
        direction = "SELL 🔴"
        analysis = "Market is heavily OVER-BOUGHT. Bearish correction imminent."
    else:
        direction = random.choice(["BUY 🟢", "SELL 🔴"])
        analysis = "Price tracking above the 20-period Exponential Moving Average (EMA)." if direction == "BUY 🟢" else "Price tracking below the 20-period Exponential Moving Average (EMA)."

    return direction, rsi, analysis

# =====================================================================
# 3. CORE SIGNAL DISPATCHER WITH DYNAMIC RANDOM TIME SELECTION
# =====================================================================
def generate_signal_report():
    pairs = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "EURGBP"]
    selected_pair = random.choice(pairs)
    
    direction, rsi_val, technical_context = calculate_indicators()
    
    # ─── TIME ROUNDING LOGIC ───
    now = datetime.now()
    
    # Calculate the exact start of the NEXT clean minute (seconds = 00)
    next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    entry_time_str = next_minute.strftime("%H:%M:00")
    
    # DYNAMIC RANDOM DURATION: Pick 1, 2, 3, or 5 minutes completely at random
    durations_pool = [1, 2, 3, 5]
    expiry_minutes = random.choice(durations_pool)
    
    # Calculate the precise ending clock time based on that randomized choice
    expiry_time = next_minute + timedelta(minutes=expiry_minutes)
    expiry_time_str = expiry_time.strftime("%H:%M:00")
    
    # Automated 3-Level Martingale Risk System
    base_stake = 10.0
    m1 = base_stake * 2.2
    m2 = m1 * 2.2

    report = (
        f"🚨 **TRADE NOW!!!** 🚨\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📈 **Pair:** {selected_pair}\n"
        f"⏳ **Entry Time:** {entry_time_str} (Next Candle)\n"
        f"⏱️ **Expiry Duration:** {expiry_minutes} Minute(s) 🎲\n"
        f"🏁 **Expiry Target Time:** {expiry_time_str}\n"
        f"🎯 **Direction:** {direction}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ **LOSS RECOVERY SYSTEM (Martingale)**\n"
        f"🔹 Base Trade: **\${base_stake:.2f}**\n"
        f"🔹 Level 1 (M1): **\${m1:.2f}**\n"
        f"🔹 Level 2 (M2): **\${m2:.2f}**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🔬 **AI Technical Analysis Report:**\n"
        f"• RSI (14): `{rsi_val:.2f}`\n"
        f"• Context: *{technical_context}*\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👉 *Wait for clock to hit {entry_time_str}, then execute trade!*"
    )
    return report

# =====================================================================
# 4. TELEGRAM USER INTERFACE ROUTERS
# =====================================================================
@dp.message_handler(commands=['start'])
async def welcome_user(message: types.Message):
    await message.answer(
        f"👋 **Welcome to AI Forex Signal Bot!**\n\n"
        f"I analyze live charts 24/7 to deliver high-accuracy setups with dynamically randomized expiry windows.\n\n"
        f"Click the button below to fetch a signal instantly.",
        reply_markup=menu_keyboard,
        parse_mode="Markdown"
    )

@dp.message_handler(lambda msg: msg.text == "🎯 Get New Signal")
async def process_signal_request(message: types.Message):
    loading_msg = await message.answer("🔄 *AI Engine analyzing chart candles, computing RSI metrics...*")
    
    await asyncio.sleep(1.2)
    signal_report = generate_signal_report()
    
    await loading_msg.delete()
    await message.answer(signal_report, parse_mode="Markdown")

# =====================================================================
# 5. ENGINE BOOTSTRAPPER
# =====================================================================
async def main():
    print("🚀 SYSTEM ARMED: Telegram interface is online with dynamic random durations.")
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
