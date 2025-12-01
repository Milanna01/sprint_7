import requests
import allure
import sys
import os

# Добавляем корневую директорию в путь Python для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from urls import Urls


class TestOrderCreate:

    @allure.title('Проверка создания заказа с разными параметрами цвета')
    @allure.description('Согласно требованиям, система должна позволять указать в заказе один цвет самоката, выбрать '
                        'сразу оба или не указывать совсем. В тест по очереди передаются наборы данных с разными '
                        'параметрами: серый, черный, оба цвета, цвет не указан. Проверяются код и тело ответа.')
    def test_order_create_color_parametrize_success(self, order_data):
        with allure.step('Отправка POST запроса на создание заказа'):
            response = requests.post(Urls.URL_orders_create, json=order_data, timeout=5)
        
        # Проверка успешного создания заказа (код 201) и наличия track-номера
        assert response.status_code == 201
        assert 'track' in response.json()
        # Дополнительная проверка, что track является числом
        assert isinstance(response.json()['track'], int)