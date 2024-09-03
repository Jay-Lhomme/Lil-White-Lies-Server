from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker
from lwlapi.models import Individual, User
from .utils import create_data, refresh_data


class TestIndividuals(APITestCase):

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
        new_individual = {
            "name": self.faker.name(),
            "uid": user.id,
            "description": self.faker.sentence(nb_words=3),
            "type": self.faker.sentence(nb_words=3)
        }
        response = self.client.post("/individuals", new_individual)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data

        self.assertTrue("id" in data)
        self.assertTrue("name" in data)
        self.assertTrue("uid" in data)
        self.assertTrue("description" in data)
        self.assertTrue("type" in data)

        db_individual = Individual.objects.get(pk=data["id"])
        self.assertEqual(db_individual.name, new_individual["name"])
        self.assertEqual(db_individual.uid.id, new_individual["uid"])
        self.assertEqual(db_individual.description,
                         new_individual["description"])
        self.assertEqual(db_individual.type, new_individual["type"])

    def test_delete(self):
        individual_id = Individual.objects.all()[0].id
        response = self.client.delete(f"/individuals/{individual_id}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse("data" in response)

        individuals = Individual.objects.filter(id=individual_id)
        self.assertEqual(len(individuals), 0)

    def test_update(self):
        user = User.objects.create(
            name=self.faker.user_name(),
            uid=self.faker.random_int(min=1, max=3),
            bio=self.faker.sentence()
        )
        individual_id = Individual.objects.all()[0].id
        updated_individual = {
            "name": self.faker.name(),
            "uid": user.id,
            "description": self.faker.sentence(nb_words=3),
            "type": self.faker.sentence(nb_words=3)
        }
        response = self.client.put(
            f"/individuals/{individual_id}", updated_individual, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertTrue("id" in data)
        self.assertTrue("name" in data)
        self.assertTrue("uid" in data)
        self.assertTrue("description" in data)
        self.assertTrue("type" in data)

        db_individual = Individual.objects.get(pk=individual_id)
        self.assertEqual(db_individual.name, updated_individual["name"])
        self.assertEqual(db_individual.uid.id, updated_individual["uid"])
        self.assertEqual(db_individual.description,
                         updated_individual["description"])
        self.assertEqual(db_individual.type, updated_individual["type"])

    def test_list(self):
        response = self.client.get("/individuals")
        data = response.data

        self.assertEqual(len(data), len(self.individuals))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        first_individual = data[0]

        self.assertTrue("id" in first_individual)
        self.assertTrue("name" in first_individual)
        self.assertTrue("uid" in first_individual)
        self.assertTrue("description" in first_individual)
        self.assertTrue("type" in first_individual)

    def test_details(self):
        individual = Individual.objects.all()[0]
        response = self.client.get(f"/individuals/{individual.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data

        self.assertEqual(data["id"], individual.id)
        self.assertEqual(data["name"], individual.name)
        self.assertEqual(data["uid"], individual.uid.id)
        self.assertEqual(data["description"], individual.description)
        self.assertEqual(data["type"], individual.type)
        # self.assertEqual(len(data["storys"]), len(individual.storys.all()))

        # first_story = data["storys"][0]

        # self.assertTrue("id" in first_story)
        # self.assertTrue("name" in first_story)
        # self.assertTrue("uid" in first_story)
        # self.assertTrue("description" in first_story)
        # self.assertTrue("type" in first_story)
