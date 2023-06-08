import telebot
from telebot import types

bot = telebot.TeleBot('6297456451:AAEDIIbHPOrweM35xKXIEk0fM0F_Qn8q_YA')


restaurants = {
'Грузинський хліб': {
'busyness': 5,
'owner_id': '476359498', 'location': 'вул. Степана Бандери, 45',
'menu': {
'Хачапурі': '60 UAH',
'Кава': '30 UAH',
'Хінкалі': '70 UAH',
'Кола': '35 UAH'
}
},
'I Love Kebab': {
'busyness': 0,
'owner_id': '476359498', 'location': 'вул. Політехнічна, 2',
'menu': {
'Кебаб': '90 UAH',
'Хот-дог': '55 UAH',
'Картопля Фрі': '50 UAH',
'Нагетси': '90 UAH'
}
},
'Паляниця': {
'busyness': 0,
'owner_id': '476359498', 'location': 'вул. Степана Бандери, 9',
'menu': {
'Чай': '25 UAH',
'Лате': '45 UAH',
'Паляниця': '70 UAH',
'Булка з маком': '30 UAH'
}
},
'Сім Поросят': {
'busyness': 0,
'owner_id': '476359498', 'location': 'вул. Архітекторська, 5',
'menu': {
'Борщ': '65 UAH',
'Піца': '190 UAH',
'Вареники': '80 UAH',
'Салат': '70 UAH'
}
},
'Хоккайдо': {
'busyness': 0,
'owner_id': '476359498', 'location': 'вул. Старицького, 2',
'menu': {
'Рамен': '80 UAH',
'Суші': '120 UAH',
'Боул': '130 UAH',
'Удон': '110 UAH'
}
},
'Шаурма': {
'busyness': 0,
'owner_id': '476359498', 'location': 'вул. Степана Бандери, 23',
'menu': {
'Шаурма з куркою': '50 UAH',
'Шаурма зі свининою': '60 UAH',
'Шаурма з яловичиною': '65 UAH',
'Шаурма вегетаріанська': '45 UAH'
}
},
'Львівські круасани': {
'busyness': 0,
'owner_id': '476359498', 'location': 'вул. Степана Бандери, 21',
'menu': {
'Круасан з шоколадом': '35 UAH',
'Круасан з маком': '30 UAH',
'Круасан з корицею': '32 UAH',
'Круасан з сиром': '28 UAH'
}
}
}


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data.split()[0] == 'get_menu':
        text = '🍜 Меню:\n\n'
        markup = types.InlineKeyboardMarkup(row_width=2)
        items = []
        for k, v in restaurants[call.data[9:]]['menu'].items():
            text+=f'{k}: {v}\n'
            items.append(types.InlineKeyboardButton(text=k, callback_data=f'order_{k}_{call.data[9::]}'))
        markup.add(*items)
        item1 = types.InlineKeyboardButton(text='◀️ Назад', callback_data=call.data[9::])
        markup.add(item1)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text, reply_markup=markup)
    elif call.data.split('_')[0] == 'order':
        bot.send_message(chat_id=call.message.chat.id, text=f'{call.data.split("_")[1]} було успішно замовлено!')
        bot.send_message(chat_id=restaurants[call.data.split("_")[2]]['owner_id'], text=f"{call.message.chat.id} замовив {call.data.split('_')[1]}")
    elif call.data.split()[0] == 'check_busyness':
        markup = types.InlineKeyboardMarkup(row_width=2)
        if restaurants[call.data[15:]]['owner_id'] == str(call.message.chat.id):
            item1 = types.InlineKeyboardButton(text='Встановити', callback_data=f'set_busyness {call.data[15:]}')
            markup.add(item1)
        item2 = types.InlineKeyboardButton(text='◀️ Назад', callback_data=call.data[15:])
        markup.add(item2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'📊 Рівень завантаженості закладу {call.data[15:]} дорівнює {restaurants[call.data[15:]]["busyness"]}%.', reply_markup=markup)
    elif call.data.split()[0] == 'set_busyness':
        bot.send_message(chat_id=call.message.chat.id, text='Введіть рівень завантаженості від 0 до 100:')
        bot.register_next_step_handler(call.message, set_busyness, call.data[13:])
    elif call.data == 'back_to_main_menu':
        markup = types.InlineKeyboardMarkup(row_width=2)
        buttons = []
        for restaurant in restaurants:
            buttons.append(types.InlineKeyboardButton(text=restaurant, callback_data=restaurant))
        markup.add(*buttons)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='👋 Привіт! Я бот, який допоможе тобі дізнатись про завантаженість закладів біля Львівської політехніки, переглядати меню та замовляти їжу. 🍽️📋🛵',
                         reply_markup=markup)
    elif call.data in restaurants:
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(text='📋 Меню ', callback_data=f'get_menu {call.data}')
        item2 = types.InlineKeyboardButton(text='👥 Завантаженість', callback_data=f'check_busyness {call.data}')
        item3 = types.InlineKeyboardButton(text='◀️ Назад', callback_data=f'back_to_main_menu')
        markup.add(item1, item2, item3)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f"Розташування: {restaurants[call.data]['location']}", reply_markup=markup)

def set_busyness(message, restaurant):
    try:
        if int(message.text)>=0 and int(message.text)<=100:
            restaurants[restaurant]['busyness']=message.text
            bot.send_message(message.chat.id, f'Рівень завантаженості для {restaurant} було встановлено.')
        else:
            bot.send_message(message.chat.id, 'Рівень завантаженості має бути числом від 0 до 100!')
    except Exception:
        bot.send_message(message.chat.id, 'Рівень завантаженості має бути числом!')


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == '/start':
        markup = types.InlineKeyboardMarkup(row_width=2)
        buttons = []
        for restaurant in restaurants:
            buttons.append(types.InlineKeyboardButton(text=restaurant, callback_data=restaurant))
        markup.add(*buttons)
        bot.send_message(message.chat.id,
                         '👋 Привіт! Я бот, який допоможе тобі дізнатись про завантаженість закладів біля Львівської політехніки, переглядати меню та замовляти їжу. 🍽️📋🛵',
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Я тебе не розумію!')

bot.polling()
