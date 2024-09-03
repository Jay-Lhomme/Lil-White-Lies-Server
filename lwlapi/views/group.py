from django.http import HttpResponseServerError
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from lwlapi.models import Group, User, Story, GroupStory
from rest_framework.decorators import action


class GroupView(ViewSet):
    """lwl group view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single group

        Returns:
            Response -- JSON serialized group
        """
        try:
            group = Group.objects.get(pk=pk)
            serializer = GroupSerializer(group)
            return Response(serializer.data)
        except Group.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all groupS

        Returns:
            Response -- JSON serialized list of groups
        """
        group = Group.objects.all()
        serializer = GroupSerializer(group, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized group instance
        """
        try:
            uid = User.objects.get(pk=request.data["uid"])
            group = Group.objects.create(
                name=request.data["name"],
                uid=uid,
                description=request.data["description"],
                type=request.data["type"],
            )
            serializer = GroupSerializer(group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        """Handle PUT requests for a group

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            group = Group.objects.get(pk=pk)
            uid = User.objects.get(pk=request.data["uid"])
            group.uid = uid
            group.name = request.data["name"]
            group.description = request.data["description"]
            group.type = request.data["type"]
            serializer = GroupSerializer(group, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Group.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk):
        """Handle DELETE requests for a group

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            group = Group.objects.get(pk=pk)
            group.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Group.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], detail=True)
    def add_story_to_group(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        story_ids = request.data.get('storyIds', [])

        if not story_ids:
            return Response({'message': 'No story IDs provided.'}, status=status.HTTP_400_BAD_REQUEST)

        added_stories = []
        existing_stories = []

        try:
            with transaction.atomic():
                # Fetch all stories at once to reduce the number of database queries
                stories = Story.objects.filter(id__in=story_ids)
                existing_story_ids = GroupStory.objects.filter(
                    group=group, story__in=stories).values_list('story_id', flat=True)

                # Determine which stories are new and which already exist
                for story in stories:
                    if story.id not in existing_story_ids:
                        GroupStory.objects.create(
                            group=group, story=story)
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

    @action(methods=['delete'], detail=True)
    def remove_story_from_group(self, request, pk):
        group = Group.objects.get(pk=pk)
        groupstory = GroupStory.objects.get(
            group=group, story=request.data['storyId'])
        groupstory.delete()

        return Response(None, status=status.HTTP_200_OK)


class GroupSerializer(serializers.ModelSerializer):
    """JSON serializer for groups"""
    class Meta:
        model = Group
        fields = ('id', 'uid', 'name', 'description', 'type')


class GroupStorySerializer(serializers.ModelSerializer):
    """JSON serializer for groups"""
    class Meta:
        model = GroupStory
        fields = ('id', 'group', 'story')
        depth = 1
