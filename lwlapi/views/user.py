from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from lwlapi.models import User


class UserView(ViewSet):
    """Tuna API users view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single user

        Returns:
            Response -- JSON serialized user
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except user.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all users

        Returns:
            Response -- JSON serialized list of users
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized user instance
        """

        user = User.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"],
        )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for an user

        Returns:
            Response -- Empty body with 204 status code
        """

        try:
            user = user.objects.get(pk=pk)
            user.name = request.data["name"]
            user.age = request.data["age"]
            user.bio = request.data["bio"]
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk):
        """Handle DELETE requests for an user

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""

    class Meta:
        model = User
        fields = ('id', 'name', 'uid', 'bio')
        depth = 1
