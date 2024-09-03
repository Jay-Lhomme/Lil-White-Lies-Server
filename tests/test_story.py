from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker
from lwlapi.models import Story, User
from .utils import create_data, refresh_data


class TestStorys(APITestCase):

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
        new_story = {
            "name": self.faker.name(),
            "uid": user.id,
            "description": self.faker.sentence(nb_words=3),
            "type": self.faker.sentence(nb_words=3)
        }
        response = self.client.post("/storys", new_story, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data

        self.assertTrue("id" in data)
        self.assertTrue("name" in data)
        self.assertTrue("uid" in data)
        self.assertTrue("description" in data)
        self.assertTrue("type" in data)

        db_story = Story.objects.get(pk=data["id"])
        self.assertEqual(db_story.name, new_story["name"])
        self.assertEqual(db_story.uid.id, new_story["uid"])
        self.assertEqual(db_story.description, new_story["description"])
        self.assertEqual(db_story.type, new_story["type"])

    def test_delete(self):
        story_id = Story.objects.all()[0].id
        response = self.client.delete(f"/storys/{story_id}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse("data" in response)

        storys = Story.objects.filter(id=story_id)
        self.assertEqual(len(storys), 0)

    def test_update(self):
        user = User.objects.create(
            name=self.faker.user_name(),
            uid=self.faker.random_int(min=1, max=3),
            bio=self.faker.sentence()
        )
        story_id = Story.objects.all()[0].id
        updated_story = {
            "name": self.faker.name(),
            "uid": user.id,
            "description": self.faker.sentence(nb_words=3),
            "type": self.faker.sentence(nb_words=3)
        }
        response = self.client.put(
            f"/storys/{story_id}", updated_story, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertTrue("id" in data)
        self.assertTrue("name" in data)
        self.assertTrue("uid" in data)
        self.assertTrue("description" in data)
        self.assertTrue("type" in data)

        db_story = Story.objects.get(pk=story_id)
        self.assertEqual(db_story.name, updated_story["name"])
        self.assertEqual(db_story.uid.id, updated_story["uid"])
        self.assertEqual(db_story.description, updated_story["description"])
        self.assertEqual(db_story.type, updated_story["type"])

    def test_list(self):
        response = self.client.get("/storys")
        data = response.data

        self.assertEqual(len(data), len(self.storys))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        first_story = data[0]

        self.assertTrue("id" in first_story)
        self.assertTrue("name" in first_story)
        self.assertTrue("uid" in first_story)
        self.assertTrue("description" in first_story)
        self.assertTrue("type" in first_story)

    def test_details(self):
        story = Story.objects.all()[0]
        response = self.client.get(f"/storys/{story.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data

        self.assertEqual(data["id"], story.id)
        self.assertEqual(data["name"], story.name)
        self.assertEqual(data["uid"], story.uid.id)
        self.assertEqual(data["description"], story.description)
        self.assertEqual(data["type"], story.type)
        # group_storys = GroupStory.objects.filter(story=story)
        # individual_storys = IndividualStory.objects.filter(story=story)
        # self.assertEqual(len(data["groups"]), len(group_storys))
        # self.assertEqual(len(data["individuals"]), len(individual_storys))

        # first_group = data["groups"][0]

        # self.assertTrue("id" in first_group)
        # self.assertTrue("name" in first_group)
        # self.assertTrue("uid" in first_group)
        # self.assertTrue("description" in first_group)
        # self.assertTrue("type" in first_group)

        # first_individual = data["individuals"][0]

        # self.assertTrue("id" in first_individual)
        # self.assertTrue("name" in first_individual)
        # self.assertTrue("uid" in first_individual)
        # self.assertTrue("description" in first_individual)
        # self.assertTrue("type" in first_individual)
