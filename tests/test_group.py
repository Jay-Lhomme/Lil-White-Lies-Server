from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker
from lwlapi.models import Group, User
from .utils import create_data, refresh_data


class TestGroups(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        create_data(cls)

    def setUp(self):
        refresh_data(self)

    def test_create(self):
        user = User.objects.create(
            name=self.faker.user_name(),
            uid=self.faker.random_int(min=1, max=3),
            bio=self.faker.sentence()
        )

        new_group = {
            "name": self.faker.name(),
            "uid": user.id,
            "description": self.faker.sentence(nb_words=3),
            "type": self.faker.sentence(nb_words=3)
        }
        response = self.client.post("/groups", new_group)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data

        self.assertTrue("id" in data)
        self.assertTrue("name" in data)
        self.assertTrue("uid" in data)
        self.assertTrue("description" in data)
        self.assertTrue("type" in data)

        db_group = Group.objects.get(pk=data["id"])
        self.assertEqual(db_group.name, new_group["name"])
        self.assertEqual(db_group.uid.id, new_group["uid"])
        self.assertEqual(db_group.description, new_group["description"])
        self.assertEqual(db_group.type, new_group["type"])

    def test_delete(self):
        group_id = Group.objects.all()[0].id
        response = self.client.delete(f"/groups/{group_id}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse("data" in response)

        groups = Group.objects.filter(id=group_id)
        self.assertEqual(len(groups), 0)

    def test_update(self):
        user = User.objects.create(
            name=self.faker.user_name(),
            uid=self.faker.random_int(min=1, max=3),
            bio=self.faker.sentence()
        )
        group_id = Group.objects.all()[0].id
        updated_group = {
            "name": self.faker.name(),
            "uid": user.id,
            "description": self.faker.sentence(nb_words=3),
            "type": self.faker.sentence(nb_words=3)
        }
        response = self.client.put(
            f"/groups/{group_id}", updated_group, format='json')

        print(response.status_code)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertTrue("id" in data)
        self.assertTrue("name" in data)
        self.assertTrue("uid" in data)
        self.assertTrue("description" in data)
        self.assertTrue("type" in data)

        db_group = Group.objects.get(pk=group_id)
        self.assertEqual(db_group.name, updated_group["name"])
        self.assertEqual(db_group.uid.id, updated_group["uid"])
        self.assertEqual(db_group.description, updated_group["description"])
        self.assertEqual(db_group.type, updated_group["type"])

    def test_list(self):
        response = self.client.get("/groups")
        data = response.data

        self.assertEqual(len(data), len(self.groups))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        first_group = data[0]

        self.assertTrue("id" in first_group)
        self.assertTrue("name" in first_group)
        self.assertTrue("uid" in first_group)
        self.assertTrue("description" in first_group)
        self.assertTrue("type" in first_group)

    def test_details(self):
        group = Group.objects.all()[0]
        response = self.client.get(f"/groups/{group.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data

        self.assertEqual(data["id"], group.id)
        self.assertEqual(data["name"], group.name)
        self.assertEqual(data["uid"], group.uid.id)
        self.assertEqual(data["description"], group.description)
        self.assertEqual(data["type"], group.type)
        # self.assertEqual(len(data["storys"]), len(group.storys.all()))

        # first_story = data["storys"][0]

        # self.assertTrue("id" in first_story)
        # self.assertTrue("name" in first_story)
        # self.assertTrue("uid" in first_story)
        # self.assertTrue("description" in first_story)
        # self.assertTrue("type" in first_story)
