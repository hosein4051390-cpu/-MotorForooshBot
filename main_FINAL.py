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

MAIN = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 فروشگاه"), KeyboardButton(text="💳 پرداخت")],
        [KeyboardButton(text="🎁 سه دوره رایگان"), KeyboardButton(text="📚 دوره‌های آموزشی")],
        [KeyboardButton(text="🚀 خدمات"), KeyboardButton(text="👤 حساب من")],
        [KeyboardButton(text="🎟 پشتیبانی"), KeyboardButton(text="📞 ارتباط با ما")],
    ],
    resize_keyboard=True,
)

SHOP = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📦 محصولات")],
        [KeyboardButton(text="📚 دوره‌های پولی")],
        [KeyboardButton(text="🔙 بازگشت به منوی اصلی")],
    ],
    resize_keyboard=True,
)

FREE = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎁 دوره رایگان ۱")],
        [KeyboardButton(text="🎁 دوره رایگان ۲")],
        [KeyboardButton(text="🎁 دوره رایگان ۳")],
        [KeyboardButton(text="🔙 بازگشت به منوی اصلی")],
    ],
    resize_keyboard=True,
)

COURSES = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 دوره چرخه پولساز")],
        [KeyboardButton(text="💣 کمپین نویسی بمب فروش")],
        [KeyboardButton(text="🧠 ذهنیت ثروت ساز")],
        [KeyboardButton(text="🔙 بازگشت به منوی اصلی")],
    ],
    resize_keyboard=True,
)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "سلام 👋\nبه 🚀 حسین فرضی‌زاده | موتور فروش خوش آمدی.\n\nاز منوی زیر انتخاب کن:",
        reply_markup=MAIN,
    )

@dp.message(F.text == "🛍 فروشگاه")
async def shop(message: Message):
    await message.answer("🛍 فروشگاه\n\nگزینه موردنظر را انتخاب کن:", reply_markup=SHOP)

@dp.message(F.text == "📦 محصولات")
async def products(message: Message):
    await message.answer(
        "📦 لیست محصولات\n\n"
        "1️⃣ دوره چرخه پولساز\n💰 ۸٬۹۰۰٬۰۰۰ تومان\n\n"
        "2️⃣ کمپین نویسی بمب فروش\n💰 ۹٬۹۰۰٬۰۰۰ تومان\n\n"
        "3️⃣ ذهنیت ثروت ساز\n💰 ۵٬۹۰۰٬۰۰۰ تومان\n\n"
        "برای اطلاعات هر دوره، «📚 دوره‌های پولی» را انتخاب کن."
    )

@dp.message(F.text == "📚 دوره‌های پولی")
async def paid_courses(message: Message):
    await message.answer("📚 دوره‌های آموزشی\n\nدوره موردنظر را انتخاب کن:", reply_markup=COURSES)

@dp.message(F.text == "💰 دوره چرخه پولساز")
async def cycle(message: Message):
    await message.answer(
        "💰 دوره چرخه پولساز\n\n"
        "💵 قیمت: ۸٬۹۰۰٬۰۰۰ تومان\n\n"
        "📝 آموزش مسیر و اصول ساخت یک چرخه فروش و درآمد.\n\n"
        "💳 برای خرید، بخش پرداخت را انتخاب کن."
    )

@dp.message(F.text == "💣 کمپین نویسی بمب فروش")
async def campaign(message: Message):
    await message.answer(
        "💣 کمپین نویسی بمب فروش\n\n"
        "💵 قیمت: ۹٬۹۰۰٬۰۰۰ تومان\n\n"
        "📝 آموزش طراحی و نوشتن کمپین‌های فروش جذاب و منظم.\n\n"
        "💳 برای خرید، بخش پرداخت را انتخاب کن."
    )

@dp.message(F.text == "🧠 ذهنیت ثروت ساز")
async def mindset(message: Message):
    await message.answer(
        "🧠 ذهنیت ثروت ساز\n\n"
        "💵 قیمت: ۵٬۹۰۰٬۰۰۰ تومان\n\n"
        "📝 آموزش مفاهیم ذهنیت مالی، هدف‌گذاری و نگرش نسبت به پول.\n\n"
        "💳 برای خرید، بخش پرداخت را انتخاب کن."
    )

@dp.message(F.text == "💳 پرداخت")
async def payment(message: Message):
    await message.answer(
        "💳 پرداخت\n\n"
        "سیستم پرداخت هنوز به درگاه پرداخت متصل نشده است.\n"
        "بعداً می‌توانیم پرداخت واقعی هر دوره را اضافه کنیم."
    )

@dp.message(F.text == "🎁 سه دوره رایگان")
async def free_courses(message: Message):
    await message.answer("🎁 سه دوره رایگان\n\nیکی را انتخاب کن:", reply_markup=FREE)

@dp.message(F.text.in_({"🎁 دوره رایگان ۱", "🎁 دوره رایگان ۲", "🎁 دوره رایگان ۳"}))
async def free_course(message: Message):
    await message.answer(f"{message.text}\n\n📚 محتوای این دوره را می‌توانیم در مرحله بعد اضافه کنیم.")

@dp.message(F.text == "📚 دوره‌های آموزشی")
async def educational_courses(message: Message):
    await message.answer("📚 دوره‌های آموزشی\n\nدوره موردنظر را انتخاب کن:", reply_markup=COURSES)

@dp.message(F.text == "🚀 خدمات")
async def services(message: Message):
    await message.answer(
        "🚀 خدمات\n\n"
        "🔹 طراحی و اجرای کمپین فروش\n"
        "🔹 مشاوره و آموزش فروش\n"
        "🔹 طراحی مسیر جذب و تبدیل مخاطب\n"
        "🔹 خدمات بازاریابی و فروش"
    )

@dp.message(F.text == "👤 حساب من")
async def account(message: Message):
    await message.answer(
        f"👤 حساب من\n\nنام: {message.from_user.full_name}\nشناسه کاربری: {message.from_user.id}"
    )

@dp.message(F.text == "🎟 پشتیبانی")
async def support(message: Message):
    await message.answer("🎟 پشتیبانی\n\nپیام خودت را ارسال کن تا بخش پشتیبانی را در مرحله بعد کامل کنیم.")

@dp.message(F.text == "📞 ارتباط با ما")
async def contact(message: Message):
    await message.answer("📞 ارتباط با ما\n\nاطلاعات تماس را می‌توانیم در مرحله بعد اضافه کنیم.")

@dp.message(F.text == "🔙 بازگشت به منوی اصلی")
async def back(message: Message):
    await message.answer("🏠 منوی اصلی", reply_markup=MAIN)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(URL.rstrip("/") + "/webhook")
    yield
    await bot.delete_webhook()
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def health():
    return {"status": "ok", "bot": "MotorFrooshBot"}

@app.post("/webhook")
async def webhook(request: Request):
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run("main_FINAL:app", host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
