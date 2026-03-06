import random
import string
from faker import Faker
import datetime

faker = Faker('ru_RU')
class DataGenerator:

 @staticmethod
 def generate_random_email():
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"kek{random_string}@gmail.com"
 @staticmethod
 def generate_random_int(x):
     return faker.random_int(x)
 @staticmethod
 def generate_random_name():
    return f"{faker.first_name()} {faker.last_name()}"

 @staticmethod
 def generate_random_password():
    """
    Генерация пароля, соответствующего требованиям:
    - Минимум 1 буква.
    - Минимум 1 цифра.
    - Допустимые символы.
    - Длина от 8 до 20 символов.
    """
    # Гарантируем наличие хотя бы одной буквы и одной цифры
    letters = random.choice(string.ascii_letters)  # Одна буква
    digits = random.choice(string.digits)  # Одна цифра

    # Дополняем пароль случайными символами из допустимого набора
    special_chars = "?@#$%^&*|:"
    all_chars = string.ascii_letters + string.digits + special_chars
    remaining_length = random.randint(6, 18)  # Остальная длина пароля
    remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

    # Перемешиваем пароль для рандомизации
    password = list(letters + digits + remaining_chars)
    random.shuffle(password)

    return ''.join(password)
 @staticmethod
 def generate_user_data() -> dict:
     from uuid import uuid4

     return {
          "id":f"{uuid4()}",
          "email":DataGenerator.generate_random_email(),
          "full_name":DataGenerator.generate_random_name(),
          "password":DataGenerator.generate_random_password(),
          "created_at":datetime.datetime.now(),
          "updated_at":datetime.datetime.now(),
          "verified":False,
         "banned": False,
         "roles":"{USER}"
     }

 @staticmethod
 def generate_movies_data() -> dict:
     from uuid import uuid4
     cities = ["MSK", "SPB"]

     return {
            "id":faker.random_int(min=18000,max=49999),
            "name":faker.word(),
            "price":faker.random_int(),
            "description":faker.sentence(),
            "image_url":faker.image_url(),
            "location":faker.random_element(cities),
            "published":faker.pybool(),
            "rating":faker.latitude(),
            "genre_id":faker.random_int(min=1,max=10),
            "created_at":datetime.datetime.now()
        }

print(DataGenerator.generate_movies_data()["id"])

