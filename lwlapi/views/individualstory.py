from django.http import HttpResponseServerError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from lwlapi.models import Individual, IndividualStory
from rest_framework.decorators import action


class IndividualStorySerializer(serializers.ModelSerializer):
    """JSON serializer for individuals"""
    class Meta:
        model = IndividualStory
        fields = ('id', 'individual', 'story')
        depth = 1


class IndividualStoryView(ModelViewSet):
    """lwl individual view"""
    queryset = IndividualStory.objects.all()
    serializer_class = IndividualStorySerializer

    def retrieve(self, request, pk):
        """Handle GET requests for single individual

        Returns:
            Response -- JSON serialized individual
        """
        try:
            individualstory = IndividualStory.objects.get(pk=pk)
            serializer = IndividualStorySerializer(individualstory)
            return Response(serializer.data)
        except IndividualStory.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all individuals

        Returns:
            Response -- JSON serialized list of individuals
        """

        individualstory = IndividualStory.objects.all()

        # individual_id = request.query_params.get('individual_id', None)
        # if uid is not None:
        #     individualstory = individualstory.filter(
        #         individual_id=individual_id)
        # uid = request.query_params.get('individual_id', None)
        # if uid is not None:
        #     individualstory = individualstory.filter(uid=uid)

        serializer = IndividualStorySerializer(individualstory, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def stories_by_individual(self, request):

        # print("Accessed stories_by_individual action")
        # Get the individual ID from query parameters
        individual_id = request.query_params.get('individual_id')
        if not individual_id:
            return Response({'error': 'individual_id query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter IndividualStorys by an individual_id
        individual_stories = IndividualStory.objects.filter(
            individual_id=individual_id)
        if not individual_stories.exists():
            return Response(
                {'error': 'No stories found for the given individual ID.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the filtered data
        serializer = IndividualStorySerializer(individual_stories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def individuals_by_stories(self, request):

        # Get the group ID from query parameters
        story_id = request.query_params.get('story_id')
        if not story_id:
            return Response({'error': 'story_id query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter GroupStorys by a group_id
        individual_stories = IndividualStory.objects.filter(
            story_id=story_id)
        if not individual_stories.exists():
            return Response(
                {'error': 'No stories found for the given individual ID.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the filtered data
        serializer = IndividualStorySerializer(individual_stories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
