from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)

def main_menu():

    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(
            "🛍 محصولات",
            callback_data="products"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "🛠 خدمات",
            callback_data="services"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "📞 پشتیبانی",
            callback_data="support"
        )
    )

    return keyboard

def products_menu():

    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(
            "💻 لپ‌تاپ",
            callback_data="product_1"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "📱 موبایل",
            callback_data="product_2"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "🎧 هدفون",
            callback_data="product_3"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "🏠 منوی اصلی",
            callback_data="main_menu"
        )
    )

    return keyboard

def services_menu():

    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(
            "💻 طراحی سایت",
            callback_data="service_101"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "🤖 ساخت ربات تلگرام",
            callback_data="service_102"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "🎨 طراحی گرافیکی",
            callback_data="service_103"
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            "🏠 منوی اصلی",
            callback_data="main_menu"
        )
    )

    return keyboard

def order_button(item_id, item_type):

    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            "🛒 سفارش این مورد",
            callback_data=f"order_{item_type}_{item_id}"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "🏠 منوی اصلی",
            callback_data="main_menu"
        )
    )

    return keyboard

def quantity_menu():

    keyboard = InlineKeyboardMarkup(row_width=3)

    keyboard.add(
        InlineKeyboardButton("1️⃣", callback_data="quantity_1"),
        InlineKeyboardButton("2️⃣", callback_data="quantity_2"),
        InlineKeyboardButton("3️⃣", callback_data="quantity_3")
    )

    keyboard.add(
        InlineKeyboardButton("4️⃣", callback_data="quantity_4"),
        InlineKeyboardButton("5️⃣", callback_data="quantity_5"),
        InlineKeyboardButton("🔟", callback_data="quantity_10")
    )

    keyboard.add(
        InlineKeyboardButton(
            "❌ لغو سفارش",
            callback_data="cancel_order"
        )
    )

    return keyboard

def confirm_order_menu():

    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(
        InlineKeyboardButton(
            "✅ تأیید",
            callback_data="confirm_order"
        ),
        InlineKeyboardButton(
            "❌ لغو",
            callback_data="cancel_order"
        )
    )

    return keyboard

def payment_menu():

    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(
            "💳 کارت به کارت",
            callback_data="payment_card"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "❌ لغو سفارش",
            callback_data="cancel_order"
        )
    )

    return keyboard


def phone_keyboard():

    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    keyboard.add(
        KeyboardButton(
            "📱 ارسال شماره تلفن",
            request_contact=True
        )
    )

    return keyboard

def admin_order_menu(order_id):

    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(

        InlineKeyboardButton(
            "✅ تأیید پرداخت",
            callback_data=f"approve_{order_id}"
        ),

        InlineKeyboardButton(
            "❌ رد پرداخت",
            callback_data=f"reject_{order_id}"
        )
    )

    return keyboard

def admin_menu():

    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(
            "📦 سفارش‌های جدید",
            callback_data="admin_pending"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "✅ سفارش‌های تأیید شده",
            callback_data="admin_approved"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "❌ سفارش‌های رد شده",
            callback_data="admin_rejected"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "📊 آمار سفارش‌ها",
            callback_data="admin_stats"
        )
    )

    return keyboard

def admin_orders_list(orders):

    keyboard = InlineKeyboardMarkup(row_width=1)

    for order in orders:

        keyboard.add(
            InlineKeyboardButton(
                f"🛒 سفارش #{order['id']} - {order['name']}",
                callback_data=f"view_order_{order['id']}"
            )
        )

    keyboard.add(
        InlineKeyboardButton(
            "🔙 پنل مدیریت",
            callback_data="admin_panel"
        )
    )

    return keyboard


def admin_order_actions(order_id):

    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(
        InlineKeyboardButton(
            "✅ تأیید پرداخت",
            callback_data=f"approve_{order_id}"
        ),
        InlineKeyboardButton(
            "❌ رد پرداخت",
            callback_data=f"reject_{order_id}"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "🔙 بازگشت",
            callback_data="admin_pending"
        )
    )

    return keyboard


