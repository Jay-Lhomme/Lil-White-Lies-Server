from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from lwlapi.models import User


class UserView(ViewSet):
    """Tuna API users view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single User

        Returns:
            Response -- JSON serialized User
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all Users

        Returns:
            Response -- JSON serialized list of users
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized User instance
        """
        try:
            uid = request.data["uid"]
            user = User.objects.get(uid=uid)
            user = User.objects.create(
                name=request.data["name"],
                uid=user,
                bio=request.data["bio"],
            )
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        """Handle PUT requests for an User

        Returns:
            Response -- Empty body with 204 status code
        """

        try:
            user = User.objects.get(pk=pk)
            user.name = request.data["name"]
            user.uid = request.data["uid"]
            user.bio = request.data["bio"]
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk):
        """Handle DELETE requests for a user

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for Users"""

    class Meta:
        model = User
        fields = ('id', 'name', 'uid', 'bio')
        depth = 1
