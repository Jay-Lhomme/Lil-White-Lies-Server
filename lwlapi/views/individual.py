from django.http import HttpResponseServerError
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from lwlapi.models import Individual, User, Story, IndividualStory
from rest_framework.decorators import action


class IndividualView(ViewSet):
    """lwl individual view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single individual

        Returns:
            Response -- JSON serialized individual
        """
        try:
            individual = Individual.objects.get(pk=pk)
            serializer = IndividualSerializer(individual)
            return Response(serializer.data)
        except Individual.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all individualS

        Returns:
            Response -- JSON serialized list of individualS
        """
        individual = Individual.objects.all()
        serializer = IndividualSerializer(individual, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized individual instance
        """
        try:
            uid = User.objects.get(pk=request.data["uid"])
            individual = Individual.objects.create(
                name=request.data["name"],
                uid=uid,
                description=request.data["description"],
                type=request.data["type"],
            )
            serializer = IndividualSerializer(individual)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        """Handle PUT requests for a individual

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            individual = Individual.objects.get(pk=pk)
            uid = User.objects.get(pk=request.data["uid"])
            individual.uid = uid
            individual.name = request.data["name"]
            individual.description = request.data["description"]
            individual.type = request.data["type"]
            serializer = IndividualSerializer(individual, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Individual.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk):
        """Handle DELETE requests for a individual

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            individual = Individual.objects.get(pk=pk)
            individual.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Individual.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], detail=True)
    def add_story_to_individual(self, request, pk):
        individual = get_object_or_404(Individual, pk=pk)
        story_ids = request.data.get('storyIds', [])

        if not story_ids:
            return Response({'message': 'No story IDs provided.'}, status=status.HTTP_400_BAD_REQUEST)

        added_stories = []
        existing_stories = []

        try:
            with transaction.atomic():
                # Fetch all stories at once to reduce the number of database queries
                stories = Story.objects.filter(id__in=story_ids)
                existing_story_ids = IndividualStory.objects.filter(
                    individual=individual, story__in=stories).values_list('story_id', flat=True)

                # Determine which stories are new and which already exist
                for story in stories:
                    if story.id not in existing_story_ids:
                        IndividualStory.objects.create(
                            individual=individual, story=story)
                        added_stories.append(story.id)
                    else:
                        existing_stories.append(story.id)

            response_data = {
                'added_stories': added_stories,
                'existing_stories': existing_stories
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Story.DoesNotExist:
            return Response({'message': 'One or more stories do not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @action(methods=['post'], detail=True)
    # def add_story_to_individual(self, request, pk):
    #     individual = Individual.objects.get(pk=pk)
    #     story = Story.objects.get(id=request.data['storyId'])
    #     try:
    #         IndividualStory.objects.get(individual=individual, story=story)
    #         return Response({'message': 'This individual already has this story.'})
    #     except IndividualStory.DoesNotExist:
    #         IndividualStory.objects.create(
    #             individual=individual,
    #             story=story
    #         )
    #         return Response(None, status=status.HTTP_200_OK)

    # @action(methods=['post'], detail=True)
    # def add_story_to_individual(self, request, pk):

    #     individual = get_object_or_404(Individual, pk=pk)
        # stories = request.data.get('storyIds', [])

        # # if not stories:
        # #     return Response({'message': 'stories list is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # added_stories = []
        # existing_stories = []

        # try:
        #     with transaction.atomic():
        #         for storie in stories:
        #             story = get_object_or_404(Story, id=storie)

        #             individual_story, created = IndividualStory.objects.get_or_create(
        #                 individual=individual,
        #                 story=story
        #             )

        #             if created:
        #                 added_stories.append(storie)
        #             else:
        #                 existing_stories.append(storie)

        #     response_data = {
        #         'added_stories': added_stories,
        #         'existing_stories': existing_stories
        #     }

        #     return Response(response_data, status=status.HTTP_200_OK)

        # except Exception as e:
        #     return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['delete'], detail=True)
    def remove_story_from_individual(self, request, pk):
        individual = Individual.objects.get(pk=pk)
        individualstory = IndividualStory.objects.get(
            individual=individual, story=request.data['storyId'])
        individualstory.delete()

        return Response(None, status=status.HTTP_200_OK)


class IndividualSerializer(serializers.ModelSerializer):
    """JSON serializer for individuals"""
    class Meta:
        model = Individual
        fields = ('id', 'uid', 'name', 'description', 'type')


class IndividualStorySerializer(serializers.ModelSerializer):
    """JSON serializer for individuals"""
    class Meta:
        model = IndividualStory
        fields = ('id', 'individual', 'story')
        depth = 1
