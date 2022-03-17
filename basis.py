import random
import emoji

db = {
    "Еда": ["Картофель", "Клубника", "Дуриан", "Мороженое", "Черная икра", "Стейк", "Морковь", "Сало", "Огурец", "Банан"],
    "Кино": ["Ужасы", "Комедия", "Документальный", "Фантастика", "Вестерн", "Боливуд", "Мелодрама", "Драма", "Триллер", "Мюзикл"],
    "Страны": ["Норвегия", "Япония", "Израиль", "Канада", "Бразилия", "Италия", "Монголия", "Эфиопия", "Эстония", "Австралия"],
    "Футбол": ["Легионер", "Команда", "Тайм", "Пенальти", "Плей-офф", "Месси", "Тренер", "Штрафной", "Реал Мадрид", "Стадион"],
    "Театр": ["Сцена", "Акт", "Гримм", "Пьеса", "Опера", "Оркестровая яма", "Режиссёр", "Актёр", "Буфет", "Антракт"],
    "Космос": ["МКС", "Ракета", "Звезда", "Юпитер", "Невесомость", "Илон Маск", "Астронавт", "НАСА", "Юрий Гагарин", "Марс"],
    "География": ["Атлас", "Континент", "Эльбрус", "Океан", "Европа", "Байкал", "Лондон", "Курильские острова", "Компас", "Навигация"],
    "Россия": ["Балалайка", "Пушкин", "Сибирь", "Водка", "Квас", "Береза", "Волга", "Калашников", "Менделеев", "Медведь"],
    "Хардкор": ["Дедукция", "Парадигма", "Инфляция", "Ротация", "Прокрастинация", "Гипотеза", "Диаграмма", "Цензура", "Биссектриса", "Пифагор"]
}
db['Всё'] = db["Еда"] + db["Кино"] + db["Страны"]  + db["Футбол"]  + db["Театр"]  + db["Космос"]  + db["География"]  + db["Россия"]  + db["Хардкор"]


class Cards:
    def __init__(self, players_num, theme):
        self.players_num = players_num
        self.theme = theme

    def get_random_list(self):
        num = random.randint(0, len(db[self.theme]))
        non_sorted = [emoji.emojize('Ты хамелеон:frog:', use_aliases=True)]
        for i in range(1, self.players_num):
            non_sorted.append(db[self.theme][num])
        sorted_list = sorted(non_sorted, key=lambda x: random.random()) 
        return sorted_list



rules = '''
Привет! Это игра Хамелеон для компании от 3 до 10 человек.
Выбери количество игроков и тему.
Смысл игры очень прост - по очереди говорить ассоциацию на слово, которое выпало всем, кроме хамелеона.
Задача хамелеона подстроиться под ассоциации и угадать слово.
Чтобы выгнать хамелеона против него нужно проголосовать. Если выгнали не того - хамелеон победил.
* * * 
Если что-то пошло не так перезапусти бота командой /start
Если слово уже было - открой все карточки и начни заново или перезапусти бота.
'''

#рандомайзер стикера перед началом игры
welcome_stickers = [
    'CAACAgIAAxkBAAEDDbVhYveTBXm8991OWj4sKhOnGAPMmQACQAEAAgeGFQdgWD3qHy3oWSEE', 
    'CAACAgIAAxkBAAEDDbdhYveVh9xSoLsseHfEK0Xy0mxIhAACRwEAAgeGFQc3WWz3c039kSEE',
    'CAACAgIAAxkBAAEDDblhYvehh-mSDaz4ejEoxuZ-V54KCgACPwEAAgeGFQfDX2jhjQ9IlSEE',
    'CAACAgIAAxkBAAEDDbthYveo5zMpSsYyushhtAbUMIZ_OQACSAEAAgeGFQf64l9XsXRNpSEE',
    'CAACAgIAAxkBAAEDDb1hYve1ltxl7w5K4YKTaOIuETAVuQACYwEAAgeGFQe4cOjjvQtkgSEE',
    'CAACAgIAAxkBAAEDDb9hYve6kUjvM7CCFnRlhJ_OTqYeVQACZAEAAgeGFQe_RYlTAtdOQiEE',
    'CAACAgIAAxkBAAEDDcFhYve_AY3uiJLNQRGAe3sTISq1SgACZgEAAgeGFQdf_2IsbPDpsyEE',
    'CAACAgIAAxkBAAEDDcNhYvfEmE148vdS1puyc3_vMsgo1QACZwEAAgeGFQdosVEl7ia2iyEE',
    ]