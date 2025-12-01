from faker import Faker
import random  # Добавляем импорт random

fake_ru = Faker('ru_RU')
fake_en = Faker()

class TestData:
    # Статические данные для тестов
    correct_login = "Milanna01"
    correct_password = "Mila.2002" 
    correct_first_name = "Milanna"
    valid_courier_credentials = {"login": "Milanna01", "password": "Mila.2002", "firstName": "Milanna"}
    courier_without_firstname = {"login": "Milanna01", "password": "1234"}
    courier_wrong_password = {"login": "Milanna01", "password": "invalid"}
    
    # Методы для генерации случайных данных
    @staticmethod
    def generate_random_login():
        return fake_en.user_name() + str(fake_en.random_int(0, 999))
    
    @staticmethod
    def generate_random_password():
        return fake_en.password(length=10)
    
    @staticmethod
    def generate_random_firstname():
        return fake_ru.first_name()
    
    @staticmethod
    def generate_random_courier_data():
        return {
            'login': TestData.generate_random_login(),
            'password': TestData.generate_random_password(),
            'firstName': TestData.generate_random_firstname()
        }


class TestOrderData:
    # Статические данные заказов с обновленными именами и фамилиями
    order_data_grey = {
        "firstName": "Анна",
        "lastName": "Смирнова",
        "address": "Шолоховский проспект, 17",
        "metroStation": 7,
        "phone": "+7 908 333 56 99",
        "rentTime": 2,
        "deliveryDate": "2025-10-26",
        "comment": "Ну-с..прокатимся наконец-то?!",
        "color": ["GREY"]
    }

    order_data_black = {
        "firstName": "Милана",
        "lastName": "Иванова",
        "address": "Москва, улица Колотушкина, 67",
        "metroStation": 10,
        "phone": "+7 988 888 67 90",
        "rentTime": 4,
        "deliveryDate": "2025-10-23",
        "comment": "Маэстро,быстрей вези мой байк.",
        "color": ["BLACK"]
    }

    order_data_two_colors = {
        "firstName": "София",
        "lastName": "Петрова",
        "address": "Москва, ул.Бульвар Комарова, 99",
        "metroStation": 25,
        "phone": "+7 900 333 33 33",
        "rentTime": 1,
        "deliveryDate": "2025-10-31",
        'comment': "Давай мне в двух цветах и тыкву для Хэллоуина!",
        "color": ["BLACK", "GREY"]
    }

    order_data_no_colors = {
        "firstName": "Екатерина",
        "lastName": "Кузнецова",
        "address": "Москва, ул. Центральная, 15",
        "metroStation": 20,
        "phone": "+7 670 567 89 10",
        "rentTime": 3,
        "deliveryDate": "2025-10-18",
        "comment": "Оо,мама мия..жду не дождусь!",
        "color": []
    }
    
    # Методы для генерации случайных заказов
    @staticmethod
    def generate_random_order_data(color=None):
        if color is None:
            color = random.choice([["BLACK"], ["GREY"], ["BLACK", "GREY"], []])  # ИСПРАВЛЕНО
            
        return {
            "firstName": fake_ru.first_name(),
            "lastName": fake_ru.last_name(),
            "address": fake_ru.address().replace('\n', ', '),
            "metroStation": fake_ru.random_int(1, 30),
            "phone": fake_ru.phone_number(),
            "rentTime": fake_ru.random_int(1, 7),
            "deliveryDate": fake_ru.future_date().strftime("%Y-%m-%d"),
            "comment": fake_ru.text(max_nb_chars=50),
            "color": color
        }