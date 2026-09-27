import telebot

from telebot.types import ReplyKeyboardRemove
from database import (
    create_tables,
    create_order,
    update_order_status,
    get_order,
    get_pending_orders,
    get_approved_orders,
    get_rejected_orders,
    get_order_statistics
)

from config import (
    BOT_TOKEN,
    ADMIN_ID,
    CARD_NUMBER,
    CARD_OWNER
)

from keyboards import (
    main_menu,
    products_menu,
    services_menu,
    order_button,
    quantity_menu,
    confirm_order_menu,
    payment_menu,
    phone_keyboard,
    admin_order_menu,
    admin_menu,
    admin_orders_list,
    admin_order_actions
)

from products import products, services

from states import user_orders


bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):

    bot.send_message(
        message.chat.id,
        "👋 سلام!\n\n"
        "به ربات سفارش خوش آمدید.\n\n"
        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=main_menu()
    )

@bot.message_handler(commands=["admin"])
def admin_panel(message):

    if message.from_user.id != ADMIN_ID:

        bot.send_message(
            message.chat.id,
            "❌ شما دسترسی به پنل مدیریت ندارید."
        )

        return

    bot.send_message(
        message.chat.id,
        "👨‍💼 <b>پنل مدیریت</b>\n\n"
        "یکی از گزینه‌های زیر را انتخاب کنید:",
        parse_mode="HTML",
        reply_markup=admin_menu()
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    user_id = call.from_user.id

    if call.data == "main_menu":

        bot.edit_message_text(
            "🏠 <b>منوی اصلی</b>\n\n"
            "لطفاً یکی از گزینه‌ها را انتخاب کنید:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=main_menu()
        )

    elif call.data == "products":

        bot.edit_message_text(
            "🛍 <b>محصولات</b>\n\n"
            "محصول موردنظر خود را انتخاب کنید:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=products_menu()
        )

    elif call.data == "services":

        bot.edit_message_text(
            "🛠 <b>خدمات</b>\n\n"
            "خدمت موردنظر خود را انتخاب کنید:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=services_menu()
        )

    elif call.data == "support":

        bot.edit_message_text(
            "📞 <b>پشتیبانی</b>\n\n"
            "برای ارتباط با پشتیبانی با ما در تماس باشید.",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=main_menu()
        )

    elif call.data.startswith("product_"):

        item_id = int(call.data.split("_")[1])

        item = products[item_id]

        text = (
            f"<b>{item['name']}</b>\n\n"
            f"📝 {item['description']}\n\n"
            f"💰 قیمت: {item['price']:,} تومان"
        )

        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=order_button(item_id, "product")
        )

    elif call.data.startswith("service_"):

        item_id = int(call.data.split("_")[1])

        item = services[item_id]

        text = (
            f"<b>{item['name']}</b>\n\n"
            f"📝 {item['description']}\n\n"
            f"💰 قیمت: {item['price']:,} تومان"
        )

        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=order_button(item_id, "service")
        )

    elif call.data.startswith("order_"):

        parts = call.data.split("_")

        item_type = parts[1]
        item_id = int(parts[2])

        if item_type == "product":
            item = products[item_id]

        else:
            item = services[item_id]

        user_orders[user_id] = {
            "item_type": item_type,
            "item_id": item_id,
            "item_name": item["name"],
            "price": item["price"]
        }

        if item_type == "product":

            bot.edit_message_text(
                "🔢 <b>انتخاب تعداد</b>\n\n"
                "تعداد موردنظر را انتخاب کنید:",
                call.message.chat.id,
                call.message.message_id,
                parse_mode="HTML",
                reply_markup=quantity_menu()
            )

        else:

            user_orders[user_id]["quantity"] = 1

            bot.edit_message_text(
                "👤 لطفاً نام و نام خانوادگی خود را ارسال کنید:",
                call.message.chat.id,
                call.message.message_id
            )

            bot.register_next_step_handler(
                call.message,
                get_name
            )


    elif call.data.startswith("quantity_"):
        quantity = int(call.data.split("_")[1])

        user_orders[user_id]["quantity"] = quantity

        bot.edit_message_text(
            "👤 <b>اطلاعات مشتری</b>\n\n"
            "لطفاً نام و نام خانوادگی خود را ارسال کنید:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML"
        )

        bot.register_next_step_handler(
            call.message,
            get_name
        )

    elif call.data == "payment_card":

        order = user_orders[user_id]

        total_price = (
            order["price"] *
            order["quantity"]
        )

        order["total_price"] = total_price

        bot.edit_message_text(
            "💳 <b>پرداخت کارت به کارت</b>\n\n"
            f"💰 مبلغ قابل پرداخت:\n"
            f"<b>{total_price:,} تومان</b>\n\n"
            f"🏦 شماره کارت:\n"
            f"<code>{CARD_NUMBER}</code>\n\n"
            f"👤 به نام:\n"
            f"<b>{CARD_OWNER}</b>\n\n"
            "پس از پرداخت، تصویر فیش را ارسال کنید.",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML"
        )

        bot.register_next_step_handler(
            call.message,
            get_receipt
        )


    elif call.data == "confirm_order":

        send_order_to_admin(call.message.chat.id, user_id)


    elif call.data == "cancel_order":

        if user_id in user_orders:
            del user_orders[user_id]

        bot.edit_message_text(
            "❌ سفارش شما لغو شد.\n\n"
            "برای ثبت سفارش جدید می‌توانید از منوی اصلی استفاده کنید.",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu()
        )


    elif call.data.startswith("approve_"):

        # فقط ادمین اجازه دارد
        if call.from_user.id != ADMIN_ID:

            bot.answer_callback_query(
                call.id,
                "❌ شما اجازه انجام این کار را ندارید.",
                show_alert=True
            )

            return


        order_id = int(
            call.data.split("_")[1]
        )


        # تغییر وضعیت
        update_order_status(
            order_id,
            "approved"
        )


        # گرفتن سفارش
        order = get_order(order_id)


        if order:

            # اطلاع به مشتری
            bot.send_message(

                order["user_id"],

                f"✅ <b>پرداخت سفارش #{order_id} تأیید شد.</b>\n\n"

                f"🛍 {order['item_name']}\n"

                f"💰 مبلغ: "
                f"{order['total_price']:,} تومان\n\n"

                "🎉 سفارش شما با موفقیت تأیید شد.",

                parse_mode="HTML",

                reply_markup=main_menu()
            )


        # تغییر پیام ادمین
        bot.edit_message_reply_markup(

            call.message.chat.id,

            call.message.message_id,

            reply_markup=None
        )


        bot.send_message(

            call.message.chat.id,

            f"✅ سفارش #{order_id} تأیید شد."
        )

    elif call.data.startswith("reject_"):

    # فقط ادمین
        if call.from_user.id != ADMIN_ID:

            bot.answer_callback_query(
                call.id,
                "❌ شما اجازه انجام این کار را ندارید.",
                show_alert=True
            )

            return


        order_id = int(
            call.data.split("_")[1]
        )


        # تغییر وضعیت
        update_order_status(
            order_id,
            "rejected"
        )


        # گرفتن سفارش
        order = get_order(order_id)


        if order:

            bot.send_message(

                order["user_id"],

                f"❌ <b>پرداخت سفارش #{order_id} تأیید نشد.</b>\n\n"

                "لطفاً فیش پرداخت خود را بررسی کنید "
                "و در صورت نیاز با پشتیبانی تماس بگیرید.",

                parse_mode="HTML",

                reply_markup=main_menu()
            )


        bot.edit_message_reply_markup(

            call.message.chat.id,

            call.message.message_id,

            reply_markup=None
        )


        bot.send_message(

            call.message.chat.id,

            f"❌ سفارش #{order_id} رد شد."
        )

    elif call.data == "admin_pending":

        if call.from_user.id != ADMIN_ID:
            return

        orders = get_pending_orders()

        if not orders:

            bot.edit_message_text(
                "📦 <b>سفارش‌های جدید</b>\n\n"
                "در حال حاضر سفارش جدیدی برای بررسی وجود ندارد.",
                call.message.chat.id,
                call.message.message_id,
                parse_mode="HTML",
                reply_markup=admin_menu()
            )

            return

        bot.edit_message_text(
            "📦 <b>سفارش‌های در انتظار بررسی</b>\n\n"
            "برای مشاهده جزئیات، سفارش موردنظر را انتخاب کنید:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=admin_orders_list(orders)
        )
    
    elif call.data == "admin_approved":

        if call.from_user.id != ADMIN_ID:
            return

        orders = get_approved_orders()

        if not orders:

            bot.edit_message_text(
                "✅ <b>سفارش‌های تأیید شده</b>\n\n"
                "هنوز سفارشی تأیید نشده است.",
                call.message.chat.id,
                call.message.message_id,
                parse_mode="HTML",
                reply_markup=admin_menu()
            )

            return

        text = "✅ <b>سفارش‌های تأیید شده</b>\n\n"

        for order in orders:

            text += (
                f"🆔 سفارش #{order['id']}\n"
                f"👤 {order['name']}\n"
                f"🛍 {order['item_name']}\n"
                f"💰 {order['total_price']:,} تومان\n"
                f"📅 {order['created_at']}\n\n"
            )

        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=admin_menu()
        )

    elif call.data.startswith("approve_"):

        if call.from_user.id != ADMIN_ID:
            return

        order_id = int(
            call.data.split("_")[1]
        )

        order = get_order(order_id)

        if not order:
            return

        if order["status"] != "pending":

            bot.answer_callback_query(
                call.id,
                "⚠️ این سفارش قبلاً بررسی شده.",
                show_alert=True
            )

            return

        update_order_status(
            order_id,
            "approved"
        )

        bot.send_message(
            order["user_id"],
            f"✅ <b>پرداخت سفارش #{order_id} تأیید شد.</b>\n\n"
            f"🛍 {order['item_name']}\n"
            f"💰 مبلغ: {order['total_price']:,} تومان\n\n"
            "🎉 سفارش شما با موفقیت تأیید شد.",
            parse_mode="HTML",
            reply_markup=main_menu()
        )

        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=None
        )

        bot.answer_callback_query(
            call.id,
            "✅ پرداخت تأیید شد."
        )

    elif call.data.startswith("reject_"):

        if call.from_user.id != ADMIN_ID:
            return

        order_id = int(
            call.data.split("_")[1]
        )

        order = get_order(order_id)

        if not order:
            return

        if order["status"] != "pending":

            bot.answer_callback_query(
                call.id,
                "⚠️ این سفارش قبلاً بررسی شده.",
                show_alert=True
            )

            return

        update_order_status(
            order_id,
            "rejected"
        )

        bot.send_message(
            order["user_id"],
            f"❌ <b>پرداخت سفارش #{order_id} تأیید نشد.</b>\n\n"
            "لطفاً فیش پرداخت خود را بررسی کنید.\n\n"
            "در صورت نیاز می‌توانید با پشتیبانی تماس بگیرید.",
            parse_mode="HTML",
            reply_markup=main_menu()
        )

        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=None
        )

        bot.answer_callback_query(
            call.id,
            "❌ پرداخت رد شد."
        )

    elif call.data == "admin_stats":

        if call.from_user.id != ADMIN_ID:
            return

        stats = get_order_statistics()

        total = stats["total"] or 0
        pending = stats["pending"] or 0
        approved = stats["approved"] or 0
        rejected = stats["rejected"] or 0

        text = (
            "📊 <b>آمار سفارش‌ها</b>\n\n"

            f"📦 کل سفارش‌ها: <b>{total}</b>\n\n"

            f"⏳ در انتظار بررسی: <b>{pending}</b>\n"

            f"✅ تأیید شده: <b>{approved}</b>\n"

            f"❌ رد شده: <b>{rejected}</b>"
        )

        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=admin_menu()
        )

    elif call.data.startswith("view_order_"):

        if call.from_user.id != ADMIN_ID:
            return

        order_id = int(
            call.data.split("_")[2]
        )

        order = get_order(order_id)

        if not order:

            bot.answer_callback_query(
                call.id,
                "❌ سفارش پیدا نشد.",
                show_alert=True
            )

            return

        status_text = {
            "pending": "⏳ در انتظار بررسی",
            "approved": "✅ تأیید شده",
            "rejected": "❌ رد شده"
        }

        text = (
            f"🛒 <b>جزئیات سفارش #{order['id']}</b>\n\n"

            f"👤 نام: {order['name']}\n"
            f"📱 شماره تماس: {order['phone']}\n\n"

            f"📦 نوع: {order['item_type']}\n"
            f"🛍 مورد: {order['item_name']}\n"
            f"🔢 تعداد: {order['quantity']}\n\n"

            f"💰 قیمت واحد: "
            f"{order['price']:,} تومان\n"

            f"💵 مبلغ نهایی: "
            f"{order['total_price']:,} تومان\n\n"

            f"💳 روش پرداخت: کارت به کارت\n"

            f"📊 وضعیت: "
            f"{status_text.get(order['status'], order['status'])}\n\n"

            f"📅 تاریخ: {order['created_at']}"
        )

        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=admin_order_actions(order_id)
        )

        if order["receipt_file_id"]:

            bot.send_photo(
                call.message.chat.id,
                order["receipt_file_id"],
                caption=f"📸 فیش پرداخت سفارش #{order_id}"
            )

    bot.answer_callback_query(call.id)

def get_name(message):

    user_id = message.from_user.id

    if not message.text:

        bot.send_message(
            message.chat.id,
            "❌ لطفاً نام خود را به صورت متنی ارسال کنید."
        )

        bot.register_next_step_handler(
            message,
            get_name
        )

        return

    user_orders[user_id]["name"] = message.text

    bot.send_message(
        message.chat.id,
        "📱 لطفاً شماره تلفن خود را ارسال کنید:",
        reply_markup=phone_keyboard()
    )

    bot.register_next_step_handler(
        message,
        get_phone
    )

def get_phone(message):

    user_id = message.from_user.id

    if message.content_type != "contact":

        bot.send_message(
            message.chat.id,
            "❌ لطفاً از دکمه «📱 ارسال شماره تلفن» استفاده کنید.",
            reply_markup=phone_keyboard()
        )

        bot.register_next_step_handler(
            message,
            get_phone
        )

        return

    user_orders[user_id]["phone"] = message.contact.phone_number

    bot.send_message(
        message.chat.id,
        "💳 لطفاً روش پرداخت را انتخاب کنید:",
        reply_markup=ReplyKeyboardRemove()
    )

    bot.send_message(
        message.chat.id,
        "💳 روش پرداخت:",
        reply_markup=payment_menu()
    )

def get_receipt(message):

    user_id = message.from_user.id

    if message.content_type != "photo":

        bot.send_message(
            message.chat.id,
            "❌ لطفاً تصویر فیش پرداخت را ارسال کنید."
        )

        bot.register_next_step_handler(
            message,
            get_receipt
        )

        return

    receipt_file_id = message.photo[-1].file_id

    user_orders[user_id]["receipt"] = receipt_file_id

    order = user_orders[user_id]

    text = (
        "📋 <b>خلاصه سفارش</b>\n\n"
        f"👤 نام: {order['name']}\n"
        f"📱 شماره: {order['phone']}\n\n"
        f"🛍 مورد: {order['item_name']}\n"
        f"🔢 تعداد: {order['quantity']}\n"
        f"💰 قیمت واحد: {order['price']:,} تومان\n"
        f"💵 مبلغ نهایی: {order['total_price']:,} تومان\n\n"
        "💳 پرداخت: کارت به کارت\n"
        "📸 فیش پرداخت دریافت شد.\n\n"
        "آیا اطلاعات سفارش صحیح است؟"
    )

    bot.send_message(
        message.chat.id,
        text,
        parse_mode="HTML",
        reply_markup=confirm_order_menu()
    )

def send_order_to_admin(chat_id, user_id):

    if user_id not in user_orders:
        return

    order = user_orders[user_id]

    order_id = create_order(

        user_id=user_id,

        name=order["name"],

        phone=order["phone"],

        item_type=order["item_type"],

        item_name=order["item_name"],

        quantity=order["quantity"],

        price=order["price"],

        total_price=order["total_price"],

        payment_method="card_to_card",

        receipt_file_id=order["receipt"]
    )


    admin_text = (

        f"🛒 <b>سفارش جدید #{order_id}</b>\n\n"

        f"👤 نام: {order['name']}\n"

        f"📱 شماره تماس: {order['phone']}\n\n"

        f"📦 نوع: {order['item_type']}\n"

        f"🛍 مورد: {order['item_name']}\n"

        f"🔢 تعداد: {order['quantity']}\n\n"

        f"💰 قیمت واحد: "
        f"{order['price']:,} تومان\n"

        f"💵 مبلغ نهایی: "
        f"{order['total_price']:,} تومان\n\n"

        "💳 روش پرداخت: کارت به کارت\n"

        "⏳ وضعیت: در انتظار بررسی"
    )


    bot.send_message(

        ADMIN_ID,

        admin_text,

        parse_mode="HTML",

        reply_markup=admin_order_menu(order_id)
    )


    bot.send_photo(

        ADMIN_ID,

        order["receipt"],

        caption=f"📸 فیش پرداخت سفارش #{order_id}"
    )


    bot.send_message(

        chat_id,

        "✅ <b>سفارش شما ثبت شد.</b>\n\n"

        f"شماره سفارش: <b>#{order_id}</b>\n\n"

        "📨 اطلاعات سفارش و فیش پرداخت "
        "برای مدیریت ارسال شد.\n\n"

        "⏳ پرداخت شما پس از بررسی تأیید خواهد شد.",

        parse_mode="HTML",

        reply_markup=main_menu()
    )


    del user_orders[user_id]

create_tables()

print("🤖 Bot is running...")

bot.infinity_polling()