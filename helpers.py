from faker import Faker

fake_en = Faker()
fake_ru = Faker('ru_RU')

def create_random_login():
    return fake_en.user_name() + str(fake_en.random_int(0, 999))

def create_random_password():
    return fake_en.password(length=10)

def create_random_firstname():
    return fake_ru.first_name()

def create_random_courier_data():
    return {
        'login': create_random_login(),
        'password': create_random_password(),
        'firstName': create_random_firstname()
    }