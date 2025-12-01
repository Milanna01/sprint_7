import requests
import allure
import pytest
import sys
import os

# Добавляем корневую директорию в путь Python для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from data import TestData
from urls import Urls


class TestCourierLogin:

    @allure.title('Проверка успешной аутентификации курьера при вводе валидных данных')
    @allure.description('Happy path. Проверяются код и тело ответа.')
    def test_courier_login_success(self, new_courier):
        with allure.step('Отправка POST запроса на авторизацию с валидными данными'):
            response = requests.post(Urls.URL_courier_login, data={
                'login': new_courier['data']['login'],
                'password': new_courier['data']['password']
            })
        
        # Проверка успешной авторизации (код 200) и наличия id в ответе
        assert response.status_code == 200
        assert 'id' in response.json()

    @allure.title('Проверка получения ошибки аутентификации при вводе невалидных данных')
    @allure.description('В тест по очереди передаются наборы данных с несуществующим логином или неверным паролем. '
                        'Проверяются код и тело ответа.')
    @pytest.mark.parametrize('nonexistent_credentials', [
        {'login': TestData.generate_random_login(), 'password': TestData.generate_random_password()},  # полностью случайные данные
        {'login': TestData.correct_login, 'password': TestData.generate_random_password()}        # существующий логин + случайный пароль
    ])
    def test_courier_login_nonexistent_data_not_found(self, nonexistent_credentials):
        with allure.step('Отправка POST запроса на авторизацию с невалидными данными'):
            response = requests.post(Urls.URL_courier_login, data=nonexistent_credentials)
        
        # Проверка ошибки "учетная запись не найдена" (код 404 и сообщение)
        assert response.status_code == 404
        assert response.json() == {'code': 404, 'message': 'Учетная запись не найдена'}

    @allure.title('Проверка получения ошибки аутентификации с пустым полем логина или пароля')
    @allure.description('В тест по очереди передаются наборы данных с пустым логином или паролем. '
                        'Проверяются код и тело ответа.')
    @pytest.mark.parametrize('empty_credentials', [
        {'login': '', 'password': TestData.generate_random_password()},  # пустой логин
        {'login': TestData.correct_login, 'password': ''}           # пустой пароль
    ])
    def test_courier_login_empty_credentials_bad_request(self, empty_credentials):
        with allure.step('Отправка POST запроса на авторизацию с пустыми полями'):
            response = requests.post(Urls.URL_courier_login, data=empty_credentials)
        
        # Проверка ошибки валидации (код 400 и сообщение)
        assert response.status_code == 400
        assert response.json() == {'code': 400, 'message': 'Недостаточно данных для входа'}

    @allure.title('Проверка возврата id при успешной авторизации')
    def test_courier_login_returns_id(self, new_courier):
        with allure.step('Отправка POST запроса на авторизацию'):
            response = requests.post(Urls.URL_courier_login, data={
                'login': new_courier['data']['login'],
                'password': new_courier['data']['password']
            })
        
        # Проверка успешной авторизации и наличия числового id в ответе
        assert response.status_code == 200
        assert 'id' in response.json()
        assert isinstance(response.json()['id'], int)