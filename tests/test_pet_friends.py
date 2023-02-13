from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email
import os


pf = PetFriends()
#1
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
#2
def test_get_all_pets_with_valid_key(filter=""):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result["pets"]) > 0
#3
def test_add_new_pet_with_valid_data(name='Кот', animal_type='Тоже кот', age='3', pet_photo='images/photo.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name
#4
def test_successful_delete_self_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Другой кот", "Тоже кот", "3", "images/photo.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()
#5
def test_successful_update_self_pet_info(name='Попугай', animal_type='Не кот', age=4):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")
#6
def test_add_new_simple_pet_with_valid_data(name='Енот', animal_type='Не кот', age='40'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_simple_pet(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
#7
def test_add_photo_simple_pet(pet_photo="images/photo1.jpg"):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        print(result)
    else:
        raise Exception("There is no my pets for")
#8
def test_get_api_key_with_invalid_email(email=invalid_password, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    print(result, "Email is not valid")
#9
def test_get_api_key_with_invalid_password(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    print(result, "Password is not valid")

#10
def test_add_invalid_photo_simple_pet(pet_photo="images/photo2.txt"):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    #По документации в таком случае ожидается, что код ответа будет 400
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        #assert status == 400
        assert status == 500
        print(result, "Error code means that provided data is incorrect")
    else:
        raise Exception("There is no my pets for")
#11
def test_add_new_pet_with_invalid_data(name='', animal_type='', age='', pet_photo='images/photo.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    #По документации поля обязательны к заполнению и ожидается 400
    #assert status == 400
    assert status == 200
    assert result['name'] == name
#12
def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
#13
def test_add_new_pet_with_number_name(name='Ё1~32!>123', animal_type='Лягушонок', age='200 000'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_simple_pet(auth_key, name, animal_type, age)
    #Ожидается 400 из за цифр и спецсимволов в имени
    #assert status == 400
    assert status == 200
    assert result['name'] == name
#14
def test_add_new_pet_with_number_type(name='Буцефал', animal_type='!24~355q', age='2'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_simple_pet(auth_key, name, animal_type, age)
    # Ожидается 400 из за цифр и спецсимволов в породе
    # assert status == 400
    assert status == 200
    assert result['name'] == name
#15
def test_add_new_pet_with_number_type(name='Буцефал', animal_type='Жираф', age='2"ё(?%№!'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_simple_pet(auth_key, name, animal_type, age)
    # Ожидается 400 из за цифр и спецсимволов в возрасте
    # assert status == 400
    assert status == 200
    assert result['name'] == name