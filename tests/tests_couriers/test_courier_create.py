import requests
import allure
import pytest
import sys
import os

# Добавляем корневую директорию в путь Python для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from urls import Urls
from data import TestData


class TestCourierCreate:

    @allure.title('Проверка создания аккаунта курьера с валидными данными')
    @allure.description('Happy path. Проверяются код и тело ответа.')
    def test_create_courier_account(self):
        """Тест создания курьера с валидными данными"""
        courier_data = TestData.generate_random_courier_data()
        courier_id = None
        
        try:
            with allure.step('Создание курьера'):
                create_response = requests.post(Urls.URL_courier_create, data=courier_data)
                
                # Проверка успешного создания
                assert create_response.status_code == 201
                assert create_response.json() == TestData.SUCCESS_RESPONSE
            
            with allure.step('Авторизация курьера для получения id'):
                login_response = requests.post(Urls.URL_courier_login, data={
                    'login': courier_data['login'],
                    'password': courier_data['password']
                })
                
                # Проверка успешной авторизации и получение id
                assert login_response.status_code == 200
                courier_id = login_response.json()["id"]
                assert isinstance(courier_id, int)
                
        finally:
            # Очистка: удаление созданного курьера
            if courier_id:
                with allure.step('Удаление тестового курьера'):
                    delete_response = requests.delete(f"{Urls.URL_courier_delete}/{courier_id}")
                    
                    # Проверка успешного удаления
                    if delete_response.status_code == 200:
                        assert delete_response.json() == TestData.SUCCESS_RESPONSE
                    else:
                        print(f"⚠️ Не удалось удалить курьера с id {courier_id}. Код ответа: {delete_response.status_code}")

    @allure.title('Проверка получения ошибки при повторном использовании логина для создания курьера')
    @allure.description('Проверяются код и тело ответа.')
    def test_create_courier_account_login_conflict(self, new_courier):
        # Пытаемся создать второго курьера с тем же логином
        payload_conflict = {
            'login': new_courier['data']['login'],
            'password': TestData.generate_random_password(),
            'firstName': TestData.generate_random_firstname()
        }
        
        with allure.step('Попытка создания второго курьера с тем же логином'):
            response = requests.post(Urls.URL_courier_create, data=payload_conflict)
        
        # Проверка конфликта (код 409) и сообщения об ошибке
        assert response.status_code == 409
        assert response.json()["message"] == TestData.ERROR_LOGIN_ALREADY_EXISTS

    @allure.title('Проверка невозможности создания двух одинаковых курьеров')
    def test_impossibility_create_two_similar(self):
        # Используем метод из TestData для генерации данных курьера
        payload = TestData.generate_random_courier_data()
        created_courier_id = None
        
        try:
            with allure.step('Первое создание курьера (должно быть успешным)'):
                first_response = requests.post(Urls.URL_courier_create, data=payload)
                assert first_response.status_code == 201
                assert first_response.json() == TestData.SUCCESS_RESPONSE
            
            with allure.step('Авторизация для получения id созданного курьера'):
                login_response = requests.post(Urls.URL_courier_login, data={
                    'login': payload['login'],
                    'password': payload['password']
                })
                if login_response.status_code == 200:
                    created_courier_id = login_response.json()["id"]
        
            with allure.step('Второе создание курьера с теми же данными (должно вызвать ошибку)'):
                second_response = requests.post(Urls.URL_courier_create, data=payload)
                
                # Проверка: первый успешен, второй возвращает ошибку конфликта
                assert second_response.status_code == 409
                assert second_response.json()["message"] == TestData.ERROR_LOGIN_ALREADY_EXISTS
                
        finally:
            # Очистка: удаление созданного курьера
            if created_courier_id:
                requests.delete(f"{Urls.URL_courier_delete}/{created_courier_id}")

    @allure.title('Проверка получения ошибки при создании курьера с незаполненными обязательными полями')
    @allure.description('В тест по очереди передаются наборы данных с пустым логином или паролем. '
                        'Проверяются код и тело ответа.')
    @pytest.mark.parametrize('empty_credentials', [
        TestData.get_empty_login_credentials(),
        TestData.get_empty_password_credentials()
    ])
    def test_create_courier_account_with_empty_required_fields(self, empty_credentials):
        with allure.step('Отправка запроса с незаполненными обязательными полями'):
            response = requests.post(Urls.URL_courier_create, data=empty_credentials)
        
        # Проверка ошибки валидации (код 400) и сообщения
        assert response.status_code == 400
        assert response.json()["message"] == TestData.ERROR_NOT_ENOUGH_DATA_FOR_ACCOUNT