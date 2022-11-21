import telebot
import randomframe
import datetime
import google_sheets_api
import staticontenthelper
import suggestions
import uptime

from telebot import types

TOKEN = "5290966510:AAF6jpJfmtdwLMIpIv0a7zkD7QQU858pVcM"
bot = telebot.TeleBot(TOKEN)

"""
Conditions: 
	0 - default condition (start point) 
	1 - Wheel dialog
	2 - Suggestion dialog
Default value of script_condition
"""
script_condition = 0

def start():
	global MainBoard

	global WheelBoard

	MainBoard = prepare_MainBoard()

	WheelBoard = prepare_WheelBoard()

	bot.infinity_polling()

def get_frame() -> str:
	return randomframe.construct_frame()

def get_HelloMessage() -> str:
	return staticontenthelper.get_hello_message()

def get_HelpMessage() -> str:
	return staticontenthelper.get_help_message()

def get_WheelPic() -> any:
	return staticontenthelper.get_wheel_pic()

def get_WheelFramebyId(id) -> str:
	return google_sheets_api.get_random_line(id)

def prepare_MainBoard() -> telebot.types.ReplyKeyboardMarkup:
	MainBoard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	MainBoard.add("Случайный фрейм", "Компас фреймов", "Предложить свой фрейм", "Помощь", row_width=1)
	return MainBoard

def prepare_WheelBoard() -> telebot.types.ReplyKeyboardMarkup:
	WheelBoard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	WheelBoard.add("1", "2", "3", "4", "5", "6","Главное меню", row_width=3)
	return WheelBoard


@bot.message_handler(commands=['start'])
def send_welcome(message):
	cid = message.chat.id
	helloMessage = get_HelloMessage()
	if (helloMessage):
		bot.send_message(cid, helloMessage, reply_markup=MainBoard)
	else:
		bot.send_message(cid, "Привет!\nTes")
		bot.send_message(cid, "Я - Генератор случайных фреймов.")
		bot.send_message(cid, "Нажимай кнопку и получи случайный фрейм.", reply_markup=MainBoard)

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#------------------------Commands for developers----------------------------------------------

"""
Time since last update
"""
@bot.message_handler(commands=['alltables'])
def send_tables_info(message):
	cid = message.chat.id
	for item in google_sheets_api._tables.keys():
		time = google_sheets_api.get_last_updated_time(item)
		bot.send_message(cid,"С последнего обновления таблицы "
						 + item
						 + " прошло " + f'\r{datetime.datetime.now() - time}')

"""
Time since startup
"""
@bot.message_handler(commands=['getuptime'])
def send_uptime(message):
	cid = message.chat.id
	bot.send_message(cid, str(uptime.uptime()))

"""
Time since startup
"""
@bot.message_handler(commands=['getframesbot'])
def send_suggest(message):
	cid = message.chat.id
	out_string = ""
	suggestions_list = suggestions.get_suggestions()
	if len(suggestions_list) == 0:
		out_string = "Пусто"
		bot.send_message(cid, out_string)
		return
	for item in suggestions_list:
		out_string += item + '\n'
	bot.send_message(cid, "Пользователями добавлен(о) \n" + str(len(suggestions_list)) + " фрейм(а/ов):")
	bot.send_message(cid, out_string)

"""
Time since startup
"""
@bot.message_handler(commands=['clear'])
def clear_suggest(message):
	cid = message.chat.id
	suggestions.clear()
	bot.send_message(cid, "Предложенные фреймы удалены")

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

def suggest_dialog(message):
	cid = message.chat.id
	if message.text == "Выйти":
		goto_main(message)
		return
	elif message.text == "/getsuggestions":
		send_suggest(message)
		bot.register_next_step_handler(message, suggest_dialog)
		return
	elif message.text == "/clear":
		clear_suggest(message)
		bot.register_next_step_handler(message, suggest_dialog)
		return
	elif message.text == "/start":
		send_welcome(message)
		return
	suggestions.suggest(message.text)
	bot.send_message(cid, "Ваш фрейм добавлен в предложенные")
	msg = bot.send_message(cid, "Введите ваш фрейм или напишите «Выйти» для выхода в основное меню")
	bot.register_next_step_handler(msg, suggest_dialog)

def wheel_dialog(message):
	cid = message.chat.id
	if message.text == "Главное меню":
		goto_main(message)
		return
	elif message.text == "/getsuggestions":
		send_suggest(message)
		bot.register_next_step_handler(message, wheel_dialog)
		return
	elif message.text == "/clear":
		clear_suggest(message)
		bot.register_next_step_handler(message, wheel_dialog)
		return
	elif message.text == "/start":
		send_welcome(message)
		return
	if message.text not in ["1", "2", "3", "4", "5", "6"]:
		msg = bot.send_message(cid, "Что-что?")
		bot.register_next_step_handler(msg, wheel_dialog)
		return

	frame = get_WheelFramebyId(message.text)

	if frame == '':
		msg = bot.send_message(cid, "Кажется этот сектор недоступен :/ \nПопробуйте другой")
		bot.register_next_step_handler(msg, wheel_dialog)
		return
	else:
		msg = bot.send_message(cid, frame)
		bot.register_next_step_handler(msg, wheel_dialog)


@bot.message_handler(regexp="Главное меню|Выйти")
def goto_main(message):
	cid = message.chat.id
	bot.send_message(cid, "Получите случайный фрейм \nили воспользуйтесь Компасом фреймов", reply_markup=MainBoard)

@bot.message_handler(regexp="Случайный фрейм")
def send_frame(message):
	cid = message.chat.id
	newframe = get_frame()
	bot.send_message(cid, newframe)

@bot.message_handler(regexp="Компас фреймов")
def send_frame(message):
	cid = message.chat.id
	global photo_msg
	if photo_msg == None:
		photo = get_WheelPic()
		if photo == None:
			bot.send_message(cid, "Кажется эта функция временно недоступна")
			return
		msg = bot.send_photo(cid, photo)
		photo_msg = msg
	else:
		bot.forward_message(cid, photo_msg.chat.id, photo_msg.id)
	msg = bot.send_message(cid, "Выбирай сектор", reply_markup=WheelBoard)
	bot.register_next_step_handler(msg, wheel_dialog)


@bot.message_handler(regexp="Предложить свой фрейм")
def send_frame(message):
	cid = message.chat.id
	rem = telebot.types.ReplyKeyboardRemove()
	msg = bot.send_message(cid, "Введите ваш фрейм или напишите «Выйти» для выхода в основное меню", reply_markup=rem)
	bot.register_next_step_handler(msg, suggest_dialog)

@bot.message_handler(regexp="Помощь")
def send_frame(message):
	cid = message.chat.id
	help_message = get_HelpMessage()
	msg = bot.send_message(cid, help_message)

@bot.message_handler()
def send_frame(message):
	cid = message.chat.id
	bot.send_message(cid, "Не понимаю :(\nПопробуй перезагрузить бота с помощью команды из Меню.")


bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

photo_msg = None