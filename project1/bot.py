import telebot
from telebot import types
from dotenv import load_dotenv
import os
from Functions import get_balance, add_income ,add_expense ,add_user,get_plan_name,get_category_ids,get_user_plan_id,get_category_name, reset_user_data
from Matplotlib import basic_plans, month_expenses, get_daily_spend, income_day, planned_actual
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from decimal import Decimal
from pan import get_monthly_savings_summary


# Load environment variables from .env file
load_dotenv()

# Access the Telegram token from the environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

#dictionary in format chat id - key; object of class User - value
users = {}

#a class to store info about usser


bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = bot.reply_to(message, "Welcome to our financial tracker bot! Thank you for joining us. Please enter your current balance to start tracking your finances.")
    bot.register_next_step_handler(msg, process_balance)
    

@bot.message_handler(func=lambda message: message.text == "My finances")
def handle_finances(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Add income"))
    markup.add(types.KeyboardButton("Add expenses"))
    markup.add(types.KeyboardButton("Show current balance"))
    markup.add(types.KeyboardButton("Back to main menu"))
    bot.send_message(message.chat.id, "Please choose an option: ", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Get statistics")
def handle_statistics(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Show incomes graph"))
    markup.add(types.KeyboardButton("Show expenses graph"))
    markup.add(types.KeyboardButton("Show current budget situation"))
    markup.add(types.KeyboardButton("Comparison(plan & actual)"))
    markup.add(types.KeyboardButton("Back to main menu"))
    bot.send_message(message.chat.id, "Please choose an option: ", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Show incomes graph")
def show_incomes(message):
    income_image = income_day(message.chat.id)
    bot.send_photo(message.chat.id, photo=income_image)

@bot.message_handler(func=lambda message: message.text == "Show expenses graph")
def show_incomes(message):
    expense_image = get_daily_spend(message.chat.id)
    bot.send_photo(message.chat.id, photo=expense_image)

@bot.message_handler(func=lambda message: message.text == "Show current budget situation")
def show_incomes(message):
    try:
        month_expense_image = month_expenses(message.chat.id)
        bot.send_photo(message.chat.id, photo=month_expense_image)
    except:
        bot.send_message(message.chat.id, "You dont have any data to visualize")

@bot.message_handler(func=lambda message: message.text == "Comparison(plan & actual)")
def show_incomes(message):
    comparison_image = planned_actual(message.chat.id)
    bot.send_photo(message.chat.id, photo=comparison_image)

@bot.message_handler(func=lambda message: message.text == "Back to main menu")
def go_back(message):
    show_main_menu(message.chat.id)

@bot.message_handler(func=lambda message: message.text == "Add income")
def handle_income(message):
    msg = bot.reply_to(message, "Please enter your new income")
    bot.register_next_step_handler(msg, process_income)

@bot.message_handler(func=lambda message: message.text == "Add expenses")
def handle_expense(message):
    msg = bot.reply_to(message, "Please enter your new expense")
    bot.register_next_step_handler(msg, process_expense)

@bot.message_handler(func=lambda message: message.text == "Show current balance")
def show_balance(message):
    bot.reply_to(message, f"You current balance: {get_balance(message.chat.id)}")

@bot.message_handler(func=lambda message: message.text == "Reset bot")
def reset_bot(message):
    reset_user_data(message.chat.id)
    bot.reply_to(message, f"Data cleared successfully, to start over press /start")


@bot.message_handler(func=lambda message: message.text == "Advanced statistics")
def reset_bot(message):
    statistics_message = get_monthly_savings_summary(message.chat.id)
    bot.reply_to(message, f"{statistics_message}")

def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("My finances"))
    markup.add(types.KeyboardButton("Get statistics"))
    markup.add(types.KeyboardButton("Advanced statistics"))
    markup.add(types.KeyboardButton("Reset bot"))

    bot.send_message(chat_id, "Please choose an option: ", reply_markup=markup)


def send_plan_options(chat_id, user_balance):

    for i in range(1,5):
        plan_image = basic_plans(i)
        plan_name = get_plan_name(i)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(plan_name, callback_data=f"plan_{i}_{user_balance}"))
        bot.send_photo(chat_id, photo=plan_image, reply_markup=markup)
        
@bot.callback_query_handler(func=lambda call: call.data.startswith("plan_"))
def handle_plan_choice(call):
    plan_number, user_balance = call.data.split("_")[1:]
    user, created =add_user(call.message.chat.id, user_balance, int(plan_number))
    if created:
        bot.send_message(call.message.chat.id, f"Your plan choice (plan {get_plan_name(plan_number)}) has been recorded. You can now start tracking your finances.")
    else:
        bot.send_message(call.message.chat.id, f'Sorry, you are already registered in our bot, to start over, use "Reset bot" button')
    show_main_menu(call.message.chat.id)


def process_balance(message):
    try:
        user_balance = Decimal(message.text) 
        if user_balance < 0:
            raise ValueError("Negative value")
        bot.reply_to(message, f"Your current balance ({user_balance}) has been recorded. Now you can choose your budget plan.")
        send_plan_options(message.chat.id, user_balance)
    except ValueError:
        bot.reply_to(message, "Please enter a valid number for your current balance.")
        bot.register_next_step_handler(message, process_balance)

def process_income(message):
    try:
        user_income = Decimal(message.text)
        if user_income < 0:
            raise ValueError("Negative value")
        add_income(message.chat.id, user_income) 
        bot.reply_to(message, f"Your new income ({user_income}) has been recorded. You can now continue tracking your finances.")
    except ValueError:
        bot.reply_to(message, "Please enter a valid number for your new income.")
        bot.register_next_step_handler(message, process_income)


def process_expense(message):
    try:
        user_expense = float(message.text) 
        if user_expense < 0:
            raise ValueError("Negative value")
        bot.reply_to(message, f"Your new expense ({user_expense}) has been recorded. Now choose the category of your expense:")
        send_category_options(message.chat.id, user_expense)
    except ValueError:
        bot.reply_to(message, "Please enter a valid number for your new expense.")
        bot.register_next_step_handler(message, process_expense)

def send_category_options(chat_id, expense_amount):
    Categories = get_category_ids(get_user_plan_id(chat_id))
    markup = InlineKeyboardMarkup()
    categories_names = Categories.keys()
    for category in categories_names:
        markup.add(InlineKeyboardButton(category, callback_data=f"category_{expense_amount}_{Categories[category]}"))
    message = bot.send_message(chat_id, "Please choose the category of your expense:", reply_markup=markup)
    return message.message_id

@bot.callback_query_handler(func=lambda call: call.data.startswith("category_"))
def callback_query(call):
    expense_amount, category_id = call.data.split("_")[1:]
    add_expense(call.message.chat.id, Decimal(expense_amount), category_id)
    bot.send_message(call.message.chat.id, f'Your expense of {expense_amount} in the category {get_category_name(category_id)} was recorded.')
    original_message_id = call.message.message_id
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=original_message_id, reply_markup=None)
bot.infinity_polling()


