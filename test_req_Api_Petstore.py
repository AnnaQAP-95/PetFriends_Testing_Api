import requests
import pytest
import json


# Ctrl + Alt + L,реформат файла

def test_get_pet():
    status = 'available'
    res = requests.get(f'https://petstore.swagger.io/v2/pet/findByStatus?status={status}',
                       headers={'accept': 'application/json'})
    if 'application/json' in res.headers['content-type']:
        print(res.json())
    else:
        print(res.text)

        print(res.status_code)
        # print(res.text)
        # print(res.json())
        print(type(res.json()))


def test_post_pet():
    body = {
        "id": 1,
        "category": {
            "id": 1,
            "name": "cat"
        },
        "name": "RRRRRRRRRRRRR",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 0,
                "name": "cat"
            }
        ],
        "status": "available"
    }
    heder = {'accept': 'application/json', 'Content-Type': 'application/json'}
    res_post = requests.post(f'https://petstore.swagger.io/v2/pet',
                             headers=heder, data=json.dumps(body))
    print(res_post.status_code)
    print(res_post.json())
    assert res_post.status_code == 200

    # Проверим GET/pet/{petId} запросом, действительно ли там лежит наш добавленный пэт
    res_get = requests.get(url=f'https://petstore.swagger.io/v2/pet/{body["id"]}')
    assert res_get.status_code == 200
    print(res_get.json())

    # DELETE удаляем нашего питомца
    res_delete = requests.delete(url=f'https://petstore.swagger.io/v2/pet/{body["id"]}')
    assert res_delete.status_code == 200

    print(res_delete.status_code)
    print(res_delete.json())

    out_del = {
        "code": 200,
        "type": "unknown",
        "message": "1"
    }
    assert json.loads(res_delete.text) == out_del

    # Проверим действительно ли удалился.
    # сделав GET запрос,
    ##мы должныполучить статус код 404 . т.к такого питомца нет в базе
    res_get = requests.get(url=f'https://petstore.swagger.io/v2/pet/{body["id"]}')

    assert res_get.status_code == 404
    print(res_get.status_code)


# GET/pet/findByStatus
# Проверим что наш питомец в available листе (проверяем статус)
def test_get_available_status():
    input_pet = {
        "id": 12345,
        "category": {
            "id": 123,
            "name": "New"
        },
        "name": "doggie",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 22,
                "name": "dog"
            }
        ],
        "status": "available"
    }
    header = {'accept': 'application/json', 'Content-Type': 'application/json'}
    res_post = requests.post(url='https://petstore.swagger.io/v2/pet', data=json.dumps(input_pet), headers=header)
    print(res_post.json())

    res_get = requests.get(url=f'https://petstore.swagger.io/v2/pet/findByStatus?status=available',
                           headers={'accept': 'application/json'})
    print(res_get.status_code)
    assert res_get.status_code == 200
    assert input_pet in list(json.loads(res_get.text))  # проверяем что наш пэт находится в листе со статусом avilable
    print(list(json.loads(res_get.text)))


# POST/pet/{petId}
def test_update_nume_post():
    header = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    name = {'name': 'Anna'}
    res_post = requests.post(url='https://petstore.swagger.io/v2/pet/12345', headers=header, data=name)

    print(res_post.text)
    print(res_post.status_code)
    assert res_post.status_code == 200
    print(json.loads(res_post.text))
    assert res_post.json() == {
        'code': 200,
        'type': 'unknown',
        'message': '12345'
    }


# PUT/pet изменение у уже имеющегося питомца
def test_update_put():
    input_pet = {
        "id": 12345,
        "category": {
            "id": 0,
            "name": "Anna_2"
        },
        "name": "doggie",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "available"
    }
    header ={'accept': 'application/json','Content-Type': 'application/json' }
    res_put= requests.put(url='https://petstore.swagger.io/v2/pet',headers=header,data=json.dumps(input_pet))

    print(res_put.status_code)
    print(res_put.json())
    assert res_put.status_code==200
    assert res_put.json()==input_pet
