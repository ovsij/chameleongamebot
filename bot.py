from aiogram.utils.callback_data import CallbackData
import aiogram.utils.markdown as md
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
import emoji
import random
from basis import Cards, rules, welcome_stickers

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    players_num = State() 
    theme = State()
    card_list_data = State()
    player1_ready = State()
    player1_word = State()
    player2_ready = State()
    player2_word = State()
    player3_ready = State()
    player3_word = State()
    player4_ready = State()
    player4_word = State()
    player5_ready = State()
    player5_word = State()
    player6_ready = State()
    player6_word = State()
    player7_ready = State()
    player7_word = State()
    player8_ready = State()
    player8_word = State()
    player9_ready = State()
    player9_word = State()
    player10_ready = State()
    player10_word = State()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    #keyboard_markup = types.InlineKeyboardMarkup()
    #press_btn = types.InlineKeyboardButton(emoji.emojize('Погнали!', use_aliases=True), callback_data= 'press')
    #keyboard_markup.row(press_btn)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row('Начать')
    markup.row('Правила')
    
    await bot.send_message(
        chat_id=message.chat.id,
        reply_markup=markup,
        text="Начать новую игру?")
    await message.answer_sticker(random.choice(welcome_stickers))

# получаем количество игроков
@dp.message_handler()
async def process_players_num(message: types.Message):
    if message.text == 'Правила':
        await bot.send_message(message.from_user.id, rules)
    elif message.text == 'Начать':
        await Form.players_num.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add('3', '4', '5', '6', '7', '8', '9', '10')
        await bot.send_message(message.from_user.id, "Введите количество игроков:", reply_markup=markup)

#проверяем количество игроков
@dp.message_handler(lambda message: message.text not in ['3', '4', '5', '6', '7', '8', '9', '10'], state=Form.players_num)
async def process_num_invalid(message: types.Message):
    return await message.reply("Выбери количество игроков кнопкой")

# получаем тему
@dp.message_handler(state=Form.players_num)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['players_num'] = int(message.text)
    await Form.next()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Еда", "Кино", "Страны", "Футбол", "Театр", "Космос", "География", "Россия", "Хардкор", "Всё")
    

    await message.reply("Выбери тему:", reply_markup=markup)

#проверяем тему
@dp.message_handler(lambda message: message.text not in ["Еда", "Кино", "Страны", "Футбол", "Театр", "Космос", "География", "Россия", "Хардкор", "Всё"], state=Form.theme)
async def process_theme_invalid(message: types.Message):
    return await message.reply("Выбери тему кнопкой")


# Сохраняем тему, выводим проверочную инфу
@dp.message_handler(state=Form.theme)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['theme'] = message.text
        await Form.next()
        #markup = types.ReplyKeyboardRemove()
        # записываем лист
        cards = Cards(data['players_num'], data['theme'])       
        card_list = cards.get_random_list()
        data['card_list'] = card_list
        await Form.next()
        

        # выводим ответы в чат
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Количество игроков:', md.bold(data['players_num'])),
                md.text('Тема:', md.code(data['theme'])),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN,
        )

# Проверяем готовность 1 игрока

        markup = types.ReplyKeyboardMarkup()
        markup.add("Да")
        await bot.send_message(
            message.chat.id, 'Игрок 1 готов?', reply_markup=markup
        )
# Проверяем готовность 1 игрока
@dp.message_handler(state=Form.player1_ready)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player1_ready'] = message.text
        await Form.next()
        

        await message.bot.delete_message(message.from_user.id, message.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(f"{data['card_list'][0]}")
        await bot.send_message(
            message.chat.id, 'Игрок 1 запоминает слово', reply_markup=markup)
        


@dp.message_handler(state=Form.player1_word)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player1_word'] = message.text
        await Form.next()
# добавить удаление последнего сообщения
        
        await message.bot.delete_message(message.from_user.id, message.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Да")
        await bot.send_message(
            message.chat.id, 'Игрок 2 готов?', reply_markup=markup)
        
        

# Выводим карточку 2 игрока
@dp.message_handler(state=Form.player2_ready)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player2_ready'] = message.text
        await Form.next()

        await message.bot.delete_message(message.from_user.id, message.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(f"{data['card_list'][1]}")
        await bot.send_message(
            message.chat.id, 'Игрок 2 запоминает слово', reply_markup=markup)

@dp.message_handler(state=Form.player2_word)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player2_word'] = message.text
        await Form.next()

        await message.bot.delete_message(message.from_user.id, message.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Да")
        await bot.send_message(
            message.chat.id, 'Игрок 3 готов?', reply_markup=markup
        )

# Выводим карточку 3 игрока
@dp.message_handler(state=Form.player3_ready)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player3_ready'] = message.text
        await Form.next()

        await message.bot.delete_message(message.from_user.id, message.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(f"{data['card_list'][2]}")
        await bot.send_message(
            message.chat.id, 'Игрок 3 запоминает слово', reply_markup=markup)


@dp.message_handler(state=Form.player3_word)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player3_word'] = message.text
        await Form.next()

        await message.bot.delete_message(message.from_user.id, message.message_id)

        if data['players_num'] >= 4:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Да")
            await bot.send_message(
                message.chat.id, 'Игрок 4 готов?', reply_markup=markup)
        else:
            await state.finish()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('Начать')
            markup.row('Правила')
            await bot.send_message(chat_id=message.chat.id, reply_markup=markup, text="Начать новую игру?")
            await message.answer_sticker(random.choice(welcome_stickers))
# Выводим карточку 4 игрока
@dp.message_handler(state=Form.player4_ready)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player4_ready'] = message.text
        await Form.next()
        await message.bot.delete_message(message.from_user.id, message.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(f"{data['card_list'][3]}")
        await bot.send_message(message.chat.id, 'Игрок 4 запоминает слово', reply_markup=markup)
        

@dp.message_handler(state=Form.player4_word)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player4_word'] = message.text
        await Form.next()

        await message.bot.delete_message(message.from_user.id, message.message_id)

        if data['players_num'] >= 5:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Да")
            await bot.send_message(
                message.chat.id, 'Игрок 5 готов?', reply_markup=markup)
        else:
            await state.finish()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('Начать')
            markup.row('Правила')
            await bot.send_message(chat_id=message.chat.id, reply_markup=markup, text="Начать новую игру?")
            await message.answer_sticker(random.choice(welcome_stickers))

# Выводим карточку 5 игрока
@dp.message_handler(state=Form.player5_ready)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player5_ready'] = message.text
        await Form.next()
        await message.bot.delete_message(message.from_user.id, message.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(f"{data['card_list'][4]}")
        await bot.send_message(message.chat.id, 'Игрок 5 запоминает слово', reply_markup=markup)
        

@dp.message_handler(state=Form.player5_word)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player5_word'] = message.text
        await Form.next()

        await message.bot.delete_message(message.from_user.id, message.message_id)

        if data['players_num'] >= 6:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Да")
            await bot.send_message(
                message.chat.id, 'Игрок 6 готов?', reply_markup=markup)
        else:
            await state.finish()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('Начать')
            markup.row('Правила')
            await bot.send_message(chat_id=message.chat.id, reply_markup=markup, text="Начать новую игру?")
            await message.answer_sticker(random.choice(welcome_stickers))
# Выводим карточку 6 игрока
@dp.message_handler(state=Form.player6_ready)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player6_ready'] = message.text
        await Form.next()
        await message.bot.delete_message(message.from_user.id, message.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(f"{data['card_list'][5]}")
        await bot.send_message(message.chat.id, 'Игрок 6 запоминает слово', reply_markup=markup)
        

@dp.message_handler(state=Form.player6_word)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player6_word'] = message.text
        await Form.next()

        await message.bot.delete_message(message.from_user.id, message.message_id)

        if data['players_num'] >= 7:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Да")
            await bot.send_message(
                message.chat.id, 'Игрок 7 готов?', reply_markup=markup)
        else:
            await state.finish()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('Начать')
            markup.row('Правила')
            await bot.send_message(chat_id=message.chat.id, reply_markup=markup, text="Начать новую игру?")
            await message.answer_sticker(random.choice(welcome_stickers))
# Выводим карточку 7 игрока
@dp.message_handler(state=Form.player7_ready)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player7_ready'] = message.text
        await Form.next()
        await message.bot.delete_message(message.from_user.id, message.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(f"{data['card_list'][6]}")
        await bot.send_message(message.chat.id, 'Игрок 7 запоминает слово', reply_markup=markup)
        

@dp.message_handler(state=Form.player7_word)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player7_word'] = message.text
        await Form.next()

        await message.bot.delete_message(message.from_user.id, message.message_id)

        if data['players_num'] >= 8:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Да")
            await bot.send_message(
                message.chat.id, 'Игрок 8 готов?', reply_markup=markup)
        else:
            await state.finish()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('Начать')
            markup.row('Правила')
            await bot.send_message(chat_id=message.chat.id, reply_markup=markup, text="Начать новую игру?")
            await message.answer_sticker(random.choice(welcome_stickers))
# Выводим карточку 8 игрока
@dp.message_handler(state=Form.player8_ready)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player8_ready'] = message.text
        await Form.next()
        await message.bot.delete_message(message.from_user.id, message.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(f"{data['card_list'][7]}")
        await bot.send_message(message.chat.id, 'Игрок 8 запоминает слово', reply_markup=markup)
        

@dp.message_handler(state=Form.player8_word)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player8_word'] = message.text
        await Form.next()

        await message.bot.delete_message(message.from_user.id, message.message_id)

        if data['players_num'] >= 9:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Да")
            await bot.send_message(
                message.chat.id, 'Игрок 9 готов?', reply_markup=markup)
        else:
            await state.finish()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('Начать')
            markup.row('Правила')
            await bot.send_message(chat_id=message.chat.id, reply_markup=markup, text="Начать новую игру?")
            await message.answer_sticker(random.choice(welcome_stickers))
# Выводим карточку 9 игрока
@dp.message_handler(state=Form.player9_ready)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player9_ready'] = message.text
        await Form.next()
        await message.bot.delete_message(message.from_user.id, message.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(f"{data['card_list'][8]}")
        await bot.send_message(message.chat.id, 'Игрок 9 запоминает слово', reply_markup=markup)
        

@dp.message_handler(state=Form.player9_word)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player9_word'] = message.text
        await Form.next()

        await message.bot.delete_message(message.from_user.id, message.message_id)

        if data['players_num'] >= 10:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Да")
            await bot.send_message(
                message.chat.id, 'Игрок 10 готов?', reply_markup=markup)
        else:
            await state.finish()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('Начать')
            markup.row('Правила')
            await bot.send_message(chat_id=message.chat.id, reply_markup=markup, text="Начать новую игру?")
            await message.answer_sticker(random.choice(welcome_stickers))
# Выводим карточку 10 игрока
@dp.message_handler(state=Form.player10_ready)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player10_ready'] = message.text
        await Form.next()
        await message.bot.delete_message(message.from_user.id, message.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(f"{data['card_list'][9]}")
        await bot.send_message(message.chat.id, 'Игрок 10 запоминает слово', reply_markup=markup)
        

@dp.message_handler(state=Form.player10_word)
async def process_start_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player10_word'] = message.text
        await Form.next()

        await message.bot.delete_message(message.from_user.id, message.message_id)

        await state.finish()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add('Начать')
        markup.row('Правила')
        await bot.send_message(chat_id=message.chat.id, reply_markup=markup, text="Начать новую игру?")
        await message.answer_sticker(random.choice(welcome_stickers))



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

