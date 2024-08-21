from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from lwlapi.models import Story, User
from lwlapi.views import UserSerializer


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
        except story.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all StoryS

        Returns:
            Response -- JSON serialized list of StoryS
        """
        story = Story.objects.all()
        serializer = StorySerializer(story, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized story instance
        """
        uid = User.objects.get(pk=request.data["user_id"])
        try:
            story = Story.objects.create(
                name=request.data["name"],
                uid=uid,
                description=request.data["description"],
                type=request.data["type"],
            )
            serializer = StorySerializer(story)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        """Handle PUT requests for a story

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            story = Story.objects.get(pk=pk)
            uid = User.objects.get(pk=request.data["user_id"])
            story.uid = uid
            story.name = request.data["name"]
            story.description = request.data["description"]
            story.type = request.data["type"]
            serializer = UserSerializer(uid, data=request.data)
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
        except story.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StorySerializer(serializers.ModelSerializer):
    """JSON serializer for Storys"""
    class Meta:
        model = Story
        fields = ('id', 'uid', 'name' 'description', 'type')
