import os
from contextlib import asynccontextmanager
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, Update
from fastapi import FastAPI, Request
import uvicorn

TOKEN = os.getenv("BOT_TOKEN")
URL = os.getenv("RENDER_EXTERNAL_URL")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")
if not URL:
    raise RuntimeError("RENDER_EXTERNAL_URL is missing")

bot = Bot(TOKEN)
dp = Dispatcher()

main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🛍 فروشگاه"), KeyboardButton(text="💳 پرداخت")],
    [KeyboardButton(text="🎁 سه دوره رایگان"), KeyboardButton(text="📚 دوره‌های آموزشی")],
    [KeyboardButton(text="🚀 خدمات"), KeyboardButton(text="👤 حساب من")],
    [KeyboardButton(text="🎟 پشتیبانی"), KeyboardButton(text="📞 ارتباط با ما")],
], resize_keyboard=True)

free_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🎁 دوره رایگان ۱")],
    [KeyboardButton(text="🎁 دوره رایگان ۲")],
    [KeyboardButton(text="🎁 دوره رایگان ۳")],
    [KeyboardButton(text="🔙 بازگشت به منوی اصلی")],
], resize_keyboard=True)

shop_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📦 محصولات")],
    [KeyboardButton(text="📚 دوره‌های پولی")],
    [KeyboardButton(text="🔙 بازگشت به منوی اصلی")],
], resize_keyboard=True)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("سلام 👋\nبه 🚀 حسین فرضی‌زاده | موتور فروش خوش آمدی.\nاز منوی زیر انتخاب کن:", reply_markup=main_kb)

@dp.message(F.text == "🛍 فروشگاه")
async def shop(message: Message):
    await message.answer("🛍 فروشگاه\nیکی از گزینه‌ها را انتخاب کن:", reply_markup=shop_kb)

@dp.message(F.text == "📦 محصولات")
async def products(message: Message):
    await message.answer("📦 بخش محصولات به‌زودی فعال می‌شود.")

@dp.message(F.text == "📚 دوره‌های پولی")
async def paid(message: Message):
    await message.answer("📚 دوره‌های پولی به‌زودی اضافه می‌شوند.")

@dp.message(F.text == "💳 پرداخت")
async def payment(message: Message):
    await message.answer("💳 بخش پرداخت هنوز به درگاه پرداخت متصل نشده است.")

@dp.message(F.text == "🎁 سه دوره رایگان")
async def free(message: Message):
    await message.answer("🎁 سه دوره رایگان:", reply_markup=free_kb)

@dp.message(F.text.in_({"🎁 دوره رایگان ۱", "🎁 دوره رایگان ۲", "🎁 دوره رایگان ۳"}))
async def free_course(message: Message):
    await message.answer(f"{message.text}\nمحتوای این دوره را می‌توانیم بعداً اضافه کنیم.")

@dp.message(F.text == "🚀 خدمات")
async def services(message: Message):
    await message.answer("🚀 بخش خدمات به‌زودی فعال می‌شود.")

@dp.message(F.text == "👤 حساب من")
async def account(message: Message):
    await message.answer(f"👤 حساب من\n\nنام: {message.from_user.full_name}\nشناسه کاربری: {message.from_user.id}")

@dp.message(F.text == "🎟 پشتیبانی")
async def support(message: Message):
    await message.answer("🎟 پشتیبانی به‌زودی فعال می‌شود.")

@dp.message(F.text == "📞 ارتباط با ما")
async def contact(message: Message):
    await message.answer("📞 اطلاعات ارتباط با ما به‌زودی اضافه می‌شود.")

@dp.message(F.text == "🔙 بازگشت به منوی اصلی")
async def back(message: Message):
    await message.answer("🏠 منوی اصلی", reply_markup=main_kb)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(URL.rstrip("/") + "/webhook")
    yield
    await bot.delete_webhook()
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def health():
    return {"status": "ok"}

@app.post("/webhook")
async def webhook(request: Request):
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
