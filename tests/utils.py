import random

from faker import Faker

from lwlapi.models import Group, GroupStory, Individual, IndividualStory, Story, User


def create_data(cls):
    cls.faker = Faker()
    cls.storys = []
    cls.users = []
    cls.groups = []
    cls.individuals = []
    cls.group_storys = []
    cls.individual_storys = []

    # for _ in range(0, 10):
    #     story = Story.objects.create(
    #         name=cls.faker.name(),
    #         uid=cls.faker.pyint(
    #             min_value=18,
    #             max_value=100
    #         ),
    #         description=cls.faker.sentence(),
    #         type=cls.faker.sentence()
    #     )
    #     cls.storys.append(story)

    #     user = User.objects.create(
    #         description=cls.faker.sentence()
    #     )
    #     cls.users.append(user)

    for _ in range(10):
        user = User.objects.create(
            name=cls.faker.sentence(),
            bio=cls.faker.sentence(),
            uid=cls.faker.sentence()
        )
        cls.users.append(user)

    if not cls.users:
        raise ValueError("No users were created.")

    for _ in range(10):
        user = random.choice(cls.users)  # Select a random user for each story
        story = Story.objects.create(
            name=cls.faker.name(),
            uid=user,  # Assign a User instance instead of an integer
            description=cls.faker.sentence(),
            type=cls.faker.sentence()  # Fixed missing comma here
        )
        cls.storys.append(story)

    for _ in range(0, random.randint(1, 3)):
        group = Group.objects.create(
            name=cls.faker.sentence(nb_words=5),
            uid=user,
            description=cls.faker.sentence(nb_words=2),
            type=cls.faker.pyint(
                min_value=15,
                max_value=180
            )
        )
        cls.groups.append(group)

        group_story = GroupStory.objects.create(
            group=group,
            story=story
        )
        cls.group_storys.append(group_story)

    for _ in range(0, random.randint(1, 3)):
        individual = Individual.objects.create(
            name=cls.faker.sentence(nb_words=5),
            uid=user,
            description=cls.faker.sentence(nb_words=2),
            type=cls.faker.pyint(
                min_value=15,
                max_value=180
            )
        )
        cls.individuals.append(individual)

        individual_story = IndividualStory.objects.create(
            individual=individual,
            story=story
        )
        cls.individual_storys.append(individual_story)


def refresh_data(self):
    for story in self.storys:
        story.refresh_from_db()
    for user in self.users:
        user.refresh_from_db()
    for group in self.groups:
        group.refresh_from_db()
    for individual in self.individuals:
        individual.refresh_from_db()
    for group_story in self.group_storys:
        group_story.refresh_from_db()
    for individual_story in self.individual_storys:
        individual_story.refresh_from_db()
