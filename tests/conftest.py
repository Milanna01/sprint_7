import pytest
import requests
import json
import allure
import sys
import os

# Добавляем корневую директорию в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from urls import Urls
from data import TestOrderData, TestData


@pytest.fixture
def new_courier():
    """Универсальная фикстура для создания и удаления курьера"""
    # Используем метод из TestData для генерации случайных данных
    courier_data = TestData.generate_random_courier_data()
    
    courier_id = None
    
    with allure.step('Создание курьера для теста'):
        create_response = requests.post(Urls.URL_courier_create, data=courier_data)
        assert create_response.status_code == 201
    
    with allure.step('Авторизация курьера для получения id'):
        login_response = requests.post(Urls.URL_courier_login, data={
            'login': courier_data['login'],
            'password': courier_data['password']
        })
        courier_id = login_response.json()["id"]
    
    yield {
        'data': courier_data,
        'id': courier_id
    }
    
    # Cleanup - удаление курьера после теста
    with allure.step('Удаление тестового курьера'):
        if courier_id:
            requests.delete(f"{Urls.URL_courier_delete}/{courier_id}")


@pytest.fixture
def new_order():
    """Универсальная фикстура для создания заказа"""
    # Используем случайные данные заказа вместо статических
    order_payload = TestOrderData.generate_random_order_data()
    headers = {'Content-Type': 'application/json'}
    
    with allure.step('Создание заказа'):
        create_response = requests.post(Urls.URL_orders_create, json=order_payload)
        track_id = create_response.json()["track"]
    
    with allure.step('Получение id заказа по track номеру'):
        get_response = requests.get(f"{Urls.URL_orders_get}?t={track_id}")
        order_id = get_response.json()['order']['id']
    
    return {
        'track_id': track_id,
        'order_id': order_id,
        'payload': order_payload  # Добавляем payload для отладки
    }


@pytest.fixture
def courier_and_order(new_courier, new_order):
    """Универсальная фикстура для создания курьера и заказа"""
    return {
        'courier': new_courier,
        'order': new_order
    }


@pytest.fixture(params=[
    TestOrderData.order_data_grey,
    TestOrderData.order_data_black, 
    TestOrderData.order_data_two_colors,
    TestOrderData.order_data_no_colors
])
def order_data(request):
    """Фикстура для параметризации данных заказа"""
    return request.param


@pytest.fixture
def authenticated_courier():
    """Фикстура для уже существующего курьера (статические данные)"""
    return {
        'login': TestData.correct_login,
        'password': TestData.correct_password,
        'id': None
    }


@pytest.fixture
def static_order():
    """Фикстура для статического заказа (без создания в БД)"""
    return TestOrderData.order_data_grey