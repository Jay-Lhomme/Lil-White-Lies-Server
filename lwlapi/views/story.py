from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from lwlapi.models import Story, User, Individual, IndividualStory, Group, GroupStory
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action


class StoryView(ViewSet):
    """lwl story view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single story

        Returns:
            Response -- JSON serialized story
        """
        try:
            story = Story.objects.get(pk=pk)
            serializer = StorySerializer(story)
            return Response(serializer.data)
        except Story.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all StoryS

        Returns:
            Response -- JSON serialized list of StoryS
        """
        stories = Story.objects.all()

        uid = request.query_params.get('uid', None)
        if uid is not None:
            stories = stories.filter(uid=uid)

        serializer = StorySerializer(stories, many=True)
        return Response(serializer.data)

    def create(self, request, format=None):
        """Handle POST operations

        Returns:
            Response -- JSON serialized story instance
        """
        uid = request.data.get("uid")
        if not uid:
            return Response({'message': 'UID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(uid=uid)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            story = Story.objects.create(
                name=request.data["name"],
                uid=user,
                description=request.data["description"],
                type=request.data["type"],
            )
            serializer = StorySerializer(story)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # uid = request.data.get("uid")
        # if not uid:
        #     return Response({'message': 'UID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     user = User.objects.get(uid=uid)
        # except User.DoesNotExist:
        #     return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # try:
        #     story = Story.objects.create(
        #         name=request.data["name"],
        #         uid=user,
        #         description=request.data["description"],
        #         type=request.data["type"],
        #     )
        #     serializer = StorySerializer(story)
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # except User.DoesNotExist:
        #     return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        # except Exception as ex:
        #     return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        """Handle PUT requests for a story

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            story = Story.objects.get(pk=pk)
            uid = User.objects.get(pk=request.data["uid"])
            story.uid = uid
            story.name = request.data["name"]
            story.description = request.data["description"]
            story.type = request.data["type"]
            serializer = StorySerializer(story, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Story.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk):
        """Handle DELETE requests for a story

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            story = Story.objects.get(pk=pk)
            story.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Story.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], detail=True)
    def add_individual_to_story(self, request, pk):
        story = get_object_or_404(Story, pk=pk)
        individual_ids = request.data.get('individualIds', [])

        if not individual_ids:
            return Response({'message': 'No individual IDs provided.'}, status=status.HTTP_400_BAD_REQUEST)

        added_individuals = []
        existing_individuals = []

        try:
            with transaction.atomic():
                # Fetch all individuals at once to reduce the number of database queries
                individuals = Individual.objects.filter(id__in=individual_ids)
                existing_individual_ids = IndividualStory.objects.filter(
                    story=story, individual__in=individuals).values_list('individual_id', flat=True)

                # Determine which individuals are new and which already exist
                for individual in individuals:
                    if individual.id not in existing_individual_ids:
                        IndividualStory.objects.create(
                            story=story, individual=individual)
                        added_individuals.append(individual.id)
                    else:
                        existing_individuals.append(individual.id)

            response_data = {
                'added_individuals': added_individuals,
                'existing_individuals': existing_individuals
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Individual.DoesNotExist:
            return Response({'message': 'One or more individuals do not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], detail=True)
    def add_group_to_story(self, request, pk):
        story = get_object_or_404(Story, pk=pk)
        group_ids = request.data.get('groupIds', [])

        if not group_ids:
            return Response({'message': 'No group IDs provided.'}, status=status.HTTP_400_BAD_REQUEST)

        added_groups = []
        existing_groups = []

        try:
            with transaction.atomic():
                # Fetch all groups at once to reduce the number of database queries
                groups = Group.objects.filter(id__in=group_ids)
                existing_group_ids = GroupStory.objects.filter(
                    story=story, group__in=groups).values_list('group_id', flat=True)

                # Determine which groups are new and which already exist
                for group in groups:
                    if group.id not in existing_group_ids:
                        GroupStory.objects.create(
                            story=story, group=group)
                        added_groups.append(group.id)
                    else:
                        existing_groups.append(group.id)

            response_data = {
                'added_groups': added_groups,
                'existing_groups': existing_groups
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Group.DoesNotExist:
            return Response({'message': 'One or more groups do not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['delete'], detail=True)
    def remove_individual_from_story(self, request, pk):
        try:
            story = Story.objects.get(pk=pk)
            individualstory = IndividualStory.objects.get(
                story=story, individual=request.data['individualId'])
            individualstory.delete()

            return Response(None, status=status.HTTP_200_OK)
        except IndividualStory.DoesNotExist:
            return Response({'message': 'Relationship not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['delete'], detail=True)
    def remove_group_from_story(self, request, pk):
        try:
            story = Story.objects.get(pk=pk)
            groupstory = GroupStory.objects.get(
                story=story, group=request.data['groupId'])
            groupstory.delete()

            return Response(None, status=status.HTTP_200_OK)
        except IndividualStory.DoesNotExist:
            return Response({'message': 'Relationship not found'}, status=status.HTTP_404_NOT_FOUND)


class StorySerializer(serializers.ModelSerializer):
    """JSON serializer for Storys"""
    class Meta:
        model = Story
        fields = ('id', 'uid', 'name', 'description', 'type')
        # depth = 1
