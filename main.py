import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN در فایل .env تنظیم نشده است.")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# =========================
# منوی اصلی
# =========================
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛍 فروشگاه"),
            KeyboardButton(text="💳 پرداخت"),
        ],
        [
            KeyboardButton(text="🎁 سه دوره رایگان"),
            KeyboardButton(text="📚 دوره‌های آموزشی"),
        ],
        [
            KeyboardButton(text="🚀 خدمات"),
            KeyboardButton(text="👤 حساب من"),
        ],
        [
            KeyboardButton(text="🎟 پشتیبانی"),
            KeyboardButton(text="📞 ارتباط با ما"),
        ],
    ],
    resize_keyboard=True,
    is_persistent=True,
    input_field_placeholder="یک گزینه را انتخاب کنید 👇",
)

# منوی سه دوره رایگان
free_courses_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎁 دوره رایگان ۱")],
        [KeyboardButton(text="🎁 دوره رایگان ۲")],
        [KeyboardButton(text="🎁 دوره رایگان ۳")],
        [KeyboardButton(text="🔙 بازگشت به منوی اصلی")],
    ],
    resize_keyboard=True,
)

# منوی فروشگاه
shop_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📦 محصولات")],
        [KeyboardButton(text="📚 دوره‌های پولی")],
        [KeyboardButton(text="🔙 بازگشت به منوی اصلی")],
    ],
    resize_keyboard=True,
)


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "👋 سلام! به 🚀 موتور فروش خوش اومدی.\n\n"
        "از منوی زیر انتخاب کن 👇",
        reply_markup=main_menu,
    )


# =========================
# فروشگاه
# =========================
@dp.message(F.text == "🛍 فروشگاه")
async def shop(message: Message):
    await message.answer(
        "🛍 فروشگاه\n\n"
        "محصول یا دوره موردنظرت رو انتخاب کن:",
        reply_markup=shop_menu,
    )


@dp.message(F.text == "📦 محصولات")
async def products(message: Message):
    await message.answer(
        "📦 محصولات\n\n"
        "محصولات فروشگاه اینجا نمایش داده می‌شوند.\n"
        "بعداً می‌توانیم قیمت، توضیحات و دکمه خرید را اضافه کنیم."
    )


@dp.message(F.text == "📚 دوره‌های پولی")
async def paid_courses(message: Message):
    await message.answer(
        "📚 دوره‌های پولی\n\n"
        "لیست دوره‌های قابل خرید اینجا قرار می‌گیرد."
    )


# =========================
# پرداخت
# =========================
@dp.message(F.text == "💳 پرداخت")
async def payment(message: Message):
    await message.answer(
        "💳 بخش پرداخت\n\n"
        "در این قسمت می‌توانیم سفارش‌های شما را نمایش دهیم "
        "و پرداخت آنلاین را به ربات متصل کنیم."
    )


# =========================
# سه دوره رایگان
# =========================
@dp.message(F.text == "🎁 سه دوره رایگان")
async def free_courses(message: Message):
    await message.answer(
        "🎁 سه دوره رایگان\n\n"
        "یکی از دوره‌ها را انتخاب کن:",
        reply_markup=free_courses_menu,
    )


@dp.message(F.text == "🎁 دوره رایگان ۱")
async def free_course_1(message: Message):
    await message.answer(
        "🎁 دوره رایگان ۱\n\n"
        "عنوان و محتوای دوره اول را اینجا قرار می‌دهیم."
    )


@dp.message(F.text == "🎁 دوره رایگان ۲")
async def free_course_2(message: Message):
    await message.answer(
        "🎁 دوره رایگان ۲\n\n"
        "عنوان و محتوای دوره دوم را اینجا قرار می‌دهیم."
    )


@dp.message(F.text == "🎁 دوره رایگان ۳")
async def free_course_3(message: Message):
    await message.answer(
        "🎁 دوره رایگان ۳\n\n"
        "عنوان و محتوای دوره سوم را اینجا قرار می‌دهیم."
    )


# =========================
# سایر بخش‌ها
# =========================
@dp.message(F.text == "📚 دوره‌های آموزشی")
async def educational_courses(message: Message):
    await message.answer(
        "📚 دوره‌های آموزشی\n\n"
        "در این قسمت می‌توانیم تمام دوره‌های آموزشی را دسته‌بندی کنیم."
    )


@dp.message(F.text == "🚀 خدمات")
async def services(message: Message):
    await message.answer(
        "🚀 خدمات\n\n"
        "خدمات شما اینجا قرار می‌گیرند."
    )


@dp.message(F.text == "👤 حساب من")
async def account(message: Message):
    await message.answer(
        "👤 حساب من\n\n"
        f"نام: {message.from_user.full_name}\n"
        f"شناسه: {message.from_user.id}\n\n"
        "در نسخه بعدی می‌توانیم خریدها، دوره‌های فعال و موجودی "
        "را هم نمایش دهیم."
    )


@dp.message(F.text == "🎟 پشتیبانی")
async def support(message: Message):
    await message.answer(
        "🎟 پشتیبانی\n\n"
        "پیامت را همین‌جا ارسال کن تا در نسخه بعدی سیستم تیکت "
        "و اتصال به ادمین را اضافه کنیم."
    )


@dp.message(F.text == "📞 ارتباط با ما")
async def contact(message: Message):
    await message.answer(
        "📞 ارتباط با ما\n\n"
        "اطلاعات تماس و لینک شبکه‌های اجتماعی را می‌توانیم اینجا قرار دهیم."
    )


@dp.message(F.text == "🔙 بازگشت به منوی اصلی")
async def back_to_main(message: Message):
    await message.answer(
        "🏠 منوی اصلی",
        reply_markup=main_menu,
    )


async def main():
    print("🤖 MotorFrooshBot v2 started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
