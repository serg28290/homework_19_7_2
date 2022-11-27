from api import PetFriends
from settings import *
import os


pf = PetFriends()


def test_allowed_request_to_any_resource():
    """ Проверяем что разрешены запросы к любому ресурсу"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_response_headers(auth_key, "my_pets")

    assert status == 200
    assert header in result


def test_use_credentials():
    """ Проверяем используются ли учетные данные"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_response_headers(auth_key, "my_pets")

    assert status == 200
    assert ('Access-Control-Allow-Credentials', 'true') not in result


def test_methods_in_headers_are_set_correctly():
    """ Проверяем что методы в заголовках установлены верно"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_methods_in_response_headers(auth_key, "my_pets")

    assert status == 200
    assert methods == result


def test_method_patch_not_allowed_in_headers():
    """ Проверяем что метод PATCH не разрешен в заголовках"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_methods_in_response_headers(auth_key, "my_pets")

    assert 'PATCH' not in result


def test_authorization_with_invalid_key():
    """ Проверяем что при запросе c неверным ключем авторизации
        получаем ответ о запрещении в доступе к указанному ресурсу"""

    # Присваиваем auth_key неверное значение ключа авторизации
    status, _ = pf.get_list_of_pets(invalid_key, "my_pets")

    assert status == 403


def test_successful_delete_any_pet():
    """Проверяем баг, что можно удалить чужого питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    pet_id = all_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    assert status == 200
    for value in all_pets.values():
        result = value[0].values()
        assert pet_id not in result


def test_add_new_pet_with_null_data(name="", animal_type="", age="", pet_photo="images/zero.jpg"):
    """Проверяем что можно добавить питомца с пустыми данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_negative_age(name="", animal_type="", age="-5", pet_photo="images/zero.jpg"):
    """Проверяем баг, что можно добавить питомца с отрицательным значением возраста"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_max_values(name=max_name, animal_type="", age=max_age, pet_photo="images/zero.jpg"):
    """Проверяем баг, что можно добавить питомца с, ошибочно введенными, большими значениями"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_successful_update_any_pet_info(name='', animal_type='', age=0):
    """Проверяем баг, что можно обновить информацию о любом питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, filter='')
    pet_id = all_pets['pets'][0]['id']
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
    _, all_pets = pf.get_list_of_pets(auth_key, filter='')
    name = all_pets['pets'][0]['name']

    assert status == 200
    assert result['name'] == name
