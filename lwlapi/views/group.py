from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from lwlapi.models import Group, User
from lwlapi.views import UserSerializer


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
        except group.DoesNotExist as ex:
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
        uid = User.objects.get(pk=request.data["user_id"])
        try:
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
            uid = User.objects.get(pk=request.data["user_id"])
            group.uid = uid
            group.name = request.data["name"]
            group.description = request.data["description"]
            group.type = request.data["type"]
            serializer = UserSerializer(uid, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except group.DoesNotExist as ex:
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
        except group.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GroupSerializer(serializers.ModelSerializer):
    """JSON serializer for groups"""
    class Meta:
        model = Group
        fields = ('id', 'uid', 'name' 'description', 'type')
