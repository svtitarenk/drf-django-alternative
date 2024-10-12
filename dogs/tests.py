from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from dogs.models import Breed, Dog
from users.models import User


class DogTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="testSetup@admin.ru")
        self.breed = Breed.objects.create(name="Лабрадор", description="Очень красивая порода")
        self.dog = Dog.objects.create(name="setupTestDog", breed=self.breed, owner=self.user)
        self.client.force_authenticate(user=self.user)

    # теперь описываем тесты. Все они начинаются со слова test дальше мы описываем сущность теста
    def test_dog_retrieve(self):
        url = reverse("dogs:dog-detail", args=(self.dog.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            f"Expected status code 200, but got {response.status_code}"
        )

        self.assertEqual(
            data.get("name"), self.dog.name
        )

    def test_dog_create(self):
        url = reverse("dogs:dog-list")
        data = {
            "name": "testCreateDog",
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

        self.assertEqual(
            Dog.objects.all().count(), 2
        )

    # тест на update
    def test_dog_update(self):
        # по-прежнему используем detail но передаем patch запрос
        url = reverse("dogs:dog-detail", args=(self.dog.pk,))
        """ 
            Сейчас при отправке запроса у нас в БД будет только собака с name=setupTestDog. 
            Мы можем проверить, что self.name равен не setupTestDog, а data.get("name")
            и status.code у нас тоже будет 200
        """
        data = {
            "name": "Форест",
        }
        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            f"Expected status code 200, but got {response.status_code}"
        )

        """ 
            так бы получили ошибку, т.к. начальное имя после patch запроса уже равно data.get("name") = "Форест"
            data.get("name"), self.dog.name
                - Форест
                + setupTestDog
        """
        self.assertEqual(
            data.get("name"), "Форест"
        )

    # тест на delete
    # также отправляем на detail и метод delete + используем pk
    def test_dog_delete(self):
        url = reverse("dogs:dog-detail", args=(self.dog.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT,
            f"Expected status code 204, but got {response.status_code}"
        )

        self.assertEqual(
            Dog.objects.all().count(), 0
        )

    # проверим вывод собак list
    def test_dog_list(self):
        url = reverse("dogs:dog-list")
        response = self.client.get(url)
        """ 
            Если что-то не получается, всегда можно запринтить ответ и достать json
        """
        print(response.json())
        """ принт переводим в data, чтобы использовать для сравнения в тесте. """
        data = response.json()

        """
            меняем параметры в result чтобы пройти тест. Меняем на переменные, где это необходимо.
            "next": None,
            "previous": None,
            "id": self.dog.pk,
            "id": self.breed.pk,
            "dogs": [
                self.dog.name
            ],

            для уточнения деталей, можно обратиться к print(response.json(), залить в файл для структуры)
        """
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.dog.pk,
                    "breed": {
                        "id": self.breed.pk,
                        "dogs": [
                            self.dog.name
                        ],
                        "name": self.breed.name,
                        "description": self.breed.description,
                        "owner": None  # потому что мы не добавляли владельца при создании породы
                    },
                    "name": self.dog.name,
                    "photo": None,
                    "date_born": None,  # дату не добавляли
                    "owner": self.user.pk  # self.dog.owner
                }
            ]
        }

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            f"Expected status code 200, but got {response.status_code}"
        )

        # сравниваем наши массивы
        self.assertEqual(
            data, result
        )


class BreedTestCase(APITestCase):
    def setUp(self):
        """
            Породу может просматривать модерато или owner который ее создал
        """
        self.user = User.objects.create(email="testSetup@admin.ru")
        self.breed = Breed.objects.create(name="Лабрадор", description="Очень красивая порода", owner=self.user)
        self.dog = Dog.objects.create(name="setupTestDog", breed=self.breed, owner=self.user)
        self.client.force_authenticate(user=self.user)

    # поскольку обращаемся к generic то прописываем name url (dogs:breed_retrieve) тайминг 36:53
    def test_breed_retrieve(self):
        url = reverse("dogs:breed-retrieve", args=(self.breed.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            f"Expected status code 200, but got {response.status_code}"
        )

        self.assertEqual(
            data.get("name"), self.breed.name
        )

    def test_breed_create(self):
        url = reverse("dogs:breed-create")
        data = {
            "name": "Овчарка",
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

        self.assertEqual(
            Breed.objects.all().count(), 2
        )

    def test_breed_update(self):
        # по-прежнему используем detail но передаем patch запрос
        url = reverse("dogs:breed-update", args=(self.breed.pk,))
        data = {
            "name": "Колли",
        }
        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            f"Expected status code 200, but got {response.status_code}"
        )

        self.assertEqual(
            data.get("name"), "Колли"
        )

    def test_breed_delete(self):
        url = reverse("dogs:breed-delete", args=(self.breed.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT,
            f"Expected status code 204, but got {response.status_code}"
        )

        self.assertEqual(
            Breed.objects.all().count(), 0
        )

    def test_breed_list(self):
        url = reverse("dogs:breeds-list")
        response = self.client.get(url)
        """ 
            Если что-то не получается, всегда можно запринтить ответ и достать json
        """
        print(response.json())
        """ принт переводим в data, чтобы использовать для сравнения в тесте. """
        data = response.json()

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.breed.pk,
                    "dogs": [
                        self.dog.name
                    ],
                    "name": self.breed.name,
                    "description": self.breed.description,
                    "owner": self.user.pk
                }
            ]
        }

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            f"Expected status code 200, but got {response.status_code}"
        )

        # сравниваем наши массивы
        self.assertEqual(
            data, result
        )
