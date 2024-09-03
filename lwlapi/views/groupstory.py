from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from lwlapi.models import Group, GroupStory
from rest_framework.decorators import action


class GroupStorySerializer(serializers.ModelSerializer):
    """JSON serializer for groups"""
    class Meta:
        model = GroupStory
        fields = ('id', 'group', 'story')
        depth = 1


class GroupStoryView(ViewSet):
    """lwl group view"""
    queryset = GroupStory.objects.all()
    serializer_class = GroupStorySerializer

    def retrieve(self, request, pk):
        """Handle GET requests for single group

        Returns:
            Response -- JSON serialized group
        """
        try:
            groupstory = GroupStory.objects.get(pk=pk)
            serializer = GroupStorySerializer(groupstory)
            return Response(serializer.data)
        except Group.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all groupS

        Returns:
            Response -- JSON serialized list of groups
        """
        groupstory = GroupStory.objects.all()
        serializer = GroupStorySerializer(groupstory, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def stories_by_group(self, request):

        # Get the group ID from query parameters
        group_id = request.query_params.get('group_id')
        if not group_id:
            return Response({'error': 'group_id query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter GroupStorys by a group_id
        group_stories = GroupStory.objects.filter(
            group_id=group_id)
        if not group_stories.exists():
            return Response(
                {'error': 'No stories found for the given group ID.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the filtered data
        serializer = GroupStorySerializer(group_stories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def groups_by_stories(self, request):

        # Get the group ID from query parameters
        story_id = request.query_params.get('story_id')
        if not story_id:
            return Response({'error': 'story_id query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter GroupStorys by a group_id
        group_stories = GroupStory.objects.filter(
            story_id=story_id)
        if not group_stories.exists():
            return Response(
                {'error': 'No stories found for the given group ID.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the filtered data
        serializer = GroupStorySerializer(group_stories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
