import os, aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, Update
from aiogram.filters import CommandStart
from fastapi import FastAPI, Request, HTTPException

TOKEN = os.getenv("TG_BOT_TOKEN")
PUBLIC_BASE = os.getenv("PUBLIC_BASE", "https://butontap.com")
API_BASE    = os.getenv("API_BASE", f"{PUBLIC_BASE}/api")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH","/bot/webhook")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET","secret")

bot = Bot(TOKEN, parse_mode="HTML")
dp  = Dispatcher()

kb = InlineKeyboardMarkup(inline_keyboard=[[
  InlineKeyboardButton(text="Join Channel", url="https://t.me/butontap"),
  InlineKeyboardButton(text="Play", web_app=WebAppInfo(url=PUBLIC_BASE))
]])

@dp.message(CommandStart())
async def start(m: Message):
    # регистрируем игрока
    async with aiohttp.ClientSession() as s:
        await s.post(f"{API_BASE}/players/me", json={"telegram_id": m.from_user.id, "username": m.from_user.username})
    await m.answer("Го тапать 🌷", reply_markup=kb)

# webhook обёртка
app = FastAPI()

@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    secret = request.headers.get("x-telegram-bot-api-secret-token")
    if secret != WEBHOOK_SECRET:
        raise HTTPException(403, "bad secret")
    data = await request.json()
    await dp.feed_update(bot, Update.model_validate(data))
    return {"ok": True}

@app.get("/health")
async def health():
    return {"ok": True}
