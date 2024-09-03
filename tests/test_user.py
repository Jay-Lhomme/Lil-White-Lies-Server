from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker
from lwlapi.models import User
from .utils import create_data, refresh_data


class TestUsers(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        create_data(cls)

    def setUp(self):
        refresh_data(self)

    def test_create(self):
        new_user = {
            "name": self.faker.name(),
            "bio": self.faker.sentence(nb_words=3),
            "uid": self.faker.sentence(nb_words=3)
        }
        response = self.client.post("/users", new_user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data

        self.assertTrue("id" in data)
        self.assertTrue("name" in data)
        self.assertTrue("bio" in data)
        self.assertTrue("uid" in data)

        db_user = User.objects.get(pk=data["id"])
        self.assertEqual(db_user.name, new_user["name"])
        self.assertEqual(db_user.bio, new_user["bio"])
        self.assertEqual(db_user.uid, new_user["uid"])

    def test_delete(self):
        user_id = User.objects.all()[0].id
        response = self.client.delete(f"/users/{user_id}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse("data" in response)

        users = User.objects.filter(id=user_id)
        self.assertEqual(len(users), 0)

    def test_update(self):
        user_id = User.objects.all()[0].id
        updated_user = {
            "name": self.faker.name(),
            "bio": self.faker.sentence(nb_words=3),
            "uid": self.faker.sentence(nb_words=3)
        }
        response = self.client.put(
            f"/users/{user_id}", updated_user, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertTrue("id" in data)
        self.assertTrue("name" in data)
        self.assertTrue("bio" in data)
        self.assertTrue("uid" in data)

        db_user = User.objects.get(pk=user_id)
        self.assertEqual(db_user.name, updated_user["name"])
        self.assertEqual(db_user.bio, updated_user["bio"])
        self.assertEqual(db_user.uid, updated_user["uid"])

    def test_list(self):
        response = self.client.get("/users")
        data = response.data

        self.assertEqual(len(data), len(self.users))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        first_user = data[0]

        self.assertTrue("id" in first_user)
        self.assertTrue("name" in first_user)
        self.assertTrue("bio" in first_user)
        self.assertTrue("uid" in first_user)
