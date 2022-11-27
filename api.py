import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """API библиотека к веб приложению Pet Friends"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru"

    def get_api_key(self, email: str, password: str):
        """Метод делает запрос к API сервера и возвращает статус
        запроса и результат в формате JSON с уникальным ключем
        пользователя, найденного по указанным email и паролем"""
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + '/api/key', headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """Метод делает запрос к API сервера и возвращает статус
        запроса и результат в формате JSON со списком найденных
        питомцев, совпадающих с фильтром.
        На данный момент фильтр может иметь либо пустое значение -
        получить список всех питомцев, либо 'my_pets' -
        получить список собственных питомцев"""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url + '/api/pets', headers=headers, params=filter)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        """Метод отправляет POST запрос на сервер с данными
        о добавляемом питомце и возвращает статус запроса на сервер
        и результат в формате JSON с данными добавленного питомца"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + '/api/pets', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца
        по указанному ID и возвращает статус запроса и результат
        в формате JSON с текстом уведомления об успешном удалении.
        На сегодняшний день тут есть баг -
        в result приходит пустая строка, но status при этом = 200"""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + '/api/pets/' + pet_id, headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер об обновлении данных питомца
        по указанному ID и возвращает статус запроса и result
        в формате JSON с обновлённыи данными питомца"""
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }
        res = requests.put(self.base_url + '/api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_response_headers(self, auth_key: json, filter: str = "") -> json:
        """Метод делает запрос к API сервера и возвращает заголовки ответа"""

        api_key = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.head(self.base_url + '/api/pets', headers=api_key, params=filter)
        status = res.status_code
        try:
            result = res.headers.items()
        except ConnectionError:
            return False
        return status, result

    def get_methods_in_response_headers(self, auth_key: json, filter: str = "") -> json:
        """Метод делает запрос к API сервера и возвращает методы в заголовках ответа"""

        api_key = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.options(self.base_url + '/api/pets', headers=api_key, params=filter)
        status = res.status_code
        try:
            result = res.headers['Allow']
        except ConnectionError:
            return False
        return status, result
