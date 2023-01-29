from api import PetFriends
from settings import valid_email, valid_password, neg_password, neg_email


class TestPetFriends:
    def setup(self):
        self.pf = PetFriends()

    '''-----Тест получения ключа пользователя c неверным паролем-----'''
    def test_get_api_for_user(self, email=valid_email, password=neg_password):
        status, result = self.pf.get_API_key(email, password)
        assert status == 403
        assert 'key' is not result

    '''-----Тест получения ключа пользователя с пустым E-mail-----'''
    def test_get_api_for_user_neg_email(self,email='', password=valid_password):
        status, result = self.pf.get_API_key(email, password)
        assert status == 403
        assert 'key' is not result

    '''-----Тест создания нового жЫвотного без фото без имени и типа -----'''
    '''---Тут БАГ , т.к. питомец без имени и типа создается, а в документации 
                     - это обязательные данные для создания нового питомца'''
    def test_add_pet_bez_foto(self,name='', animal_type='', age=3.5):
        _, auth_key = self.pf.get_API_key(valid_email,valid_password)
        status, result = self.pf.add_pet_without_foto(auth_key, name, animal_type, age)
        assert status == 200
        assert result['name'] == name


    '''-----Тест создания нового жЫвотного c фото,но  фото в папке нет-----'''
    def test_add_pet(self,name='Флинт', animal_type='шотландец', age='8',
                                    pet_photo='imaje/1Шоггот.jpg'):
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name
        assert FileNotFoundError in result

    '''-----Тест создания нового жЫвотного c фото,  без  фото -----'''
    def test_add_pet(self, name='Флинт', animal_type='шотландец', age='8',
                     pet_photo=''):
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 400
        assert result['name'] == name
        assert FileNotFoundError in result


    '''-----Тест обновления информации жЫвотного не в списке-----'''
    def test_update_pet_NotmyPets(self,name='Изменен', animal_type='Изменен', age=3.6):
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(myPets['pets']) > 0:
            status, result = self.pf.update_pet_info(auth_key, myPets['pets'][59]['id'], name, animal_type, age)
            assert status == 400
            assert result['name'] == name
        else:
            raise Exception("There is no my pets")
            assert IndexError in result


    '''-----Тест удаления жЫвотного не в списке-----'''
    def test_delete_pet(self):
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_mypets(auth_key, "my_pets")

        if len(myPets['pets']) > 0:
            pet_id = myPets['pets'][53]['id']
            status, _ = pf.delete_pet(auth_key, pet_id)

            _, myPets = pf.get_list_mypets(auth_key, "my_pets")

        # Проверяем что статус ответа = 400
        assert status == 400
        # если список питомцев пустой,то выкидываем исключение с текстом об от-сутствии своих питомцев
        if len(myPets['pets']) == 0:
            raise Exception("There is no my pets!")

        #     assert pet_id not in my_pets.values()
        # else:
        #     raise Exception("There is no my pets")




    '''-----Тест создания нового жЫвотного с фото без имени,типа и возраста(обязательные поля в документации Swagger-----'''
    '''Животное создается, без обязательных полей-это БАГ'''
    def test_add_New_PetWithValidData(self, name='', animal_type='', age='',
                                    pet_photo='imaje/1628812614_59-p-foto-visloukhikh-kotyat-britantsev-62.jpg'):

        _, auth_key = self.pf.get_API_key(valid_email, valid_password)

        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name



    '''-----Тест создания нового жЫвотного в параметре age длинное число с дробью например 3.123456789 -----'''
    def test_add_pet_bez_foto(self, name='Маша', animal_type='Котик', age=3.123456789):
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        status, result = self.pf.add_pet_without_foto(auth_key, name, animal_type, age)
        '''---- Проверяем, если статус ответа = 200 и длину возраста более 3 цифр принимает,
         значит тест проходит с очень большим значением, чего быть не должно:---'''
        assert status == 200
        assert len(result['age']) > 3
        assert result['name'] == name


    '''-----Тест обновления информации жЫвотного с не верным айди-----'''
    def test_update_pet(self, name='Изменен', animal_type='Изменен', age=3.6):
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        # Если список не пустой, то пробуем обновить его имя, тип и возраст, изменив id первого питомца:
        if len(myPets['pets']) > 0:
            status, result = self.pf.update_pet_info(auth_key, myPets['pets'][0]['id']+ "2d3r", name, animal_type, age)

        print(f"\n Неверный id: {myPets['pets'][0]['id'] + '2d3r'}")
        # Проверяем что статус ответа = 400
        assert status == 400
        # если список питомцев пустой,то выкидываем исключение с текстом об от-сутствии своих питомцев
        if  len(myPets['pets']) == 0:
            raise Exception("There is no my pets!")



