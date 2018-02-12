from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from nomadgram.notifications import views as notification_views
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

class ExploreUsers (APIView):

    def get(self, request, format=None):

        last_five = models.User.objects.all().order_by('-date_joined')[:5]

        serializer = serializers.ListUsersSerializer(last_five, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FollowUser(APIView):

    def post(self, request, user_id, format=None):

        user = request.user

        try:
            user_to_follow = models.User.objects.get(id=user_id)

        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.add(user_to_follow)

        user.save()

        notification_views.create_notification(user, user_to_follow, 'follow')

        return Response(status=status.HTTP_200_OK)
        

class UnFollowUser(APIView):

    def post(self, request, user_id, format=None):

        user = request.user

        try:
            user_to_follow = models.User.objects.get(id=user_id)

        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.remove(user_to_follow)

        user.save()

        return Response(status=status.HTTP_200_OK)


class UserProfile(APIView):

        def get_user(self, username):

            try:
                found_user = models.User.objects.get(username=username)
                return found_user

            except models.User.DoesNotExist:

                return None

        def get(self, request, username, format=None):

            found_user = self.get_user(username)

            if found_user is None:
                
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = serializers.UserProfileSerializer(found_user)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        def put(self, request, username, format=None):

            found_user = self.get_user(username)

            if found_user is None:

                return Response(status=status.HTTP_404_NOT_FOUND)

            if found_user.username != request.user.username:

                return Response(status=status.HTTP_401_UNAUTHORIZED)

            serializer = serializers.UserProfileSerializer(found_user, data=request.data, partial=True)

            if serializer.is_valid():

                serializer.save()

                return Response(data=serializer.data, status=status.HTTP_200_OK)

            return Response(data=serializer.error, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):

    def put(self, request, username, format=None):

        user = request.user

        if user.username != username:

            print(user.username)
            print(username)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        current_password = request.data.get('current_password', None)

        if current_password is not None:

            password_match = user.check_password(current_password)

            if password_match:

                new_password = request.data.get('new_password', None)

                if new_password is not None:

                    user.set_password(new_password)

                    user.save()

                    return Response(status=status.HTTP_200_OK)

                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(status=status.HTTP_404_NOT_FOUND)


class UserFollowers(APIView):

    def get(self, request, username, format=None):

        try:
            found_user = models.User.objects.get(username=username)

        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_followers = found_user.followers.all()

        serializer = serializers.ListUsersSerializer(user_followers, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserFollowing(APIView):

    def get(self, request, username, format=None):

        try:
            found_user = models.User.objects.get(username=username)

        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_followings = found_user.following.all()

        serializer = serializers.ListUsersSerializer(
            user_followings, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class Search(APIView):

    def get(self, request, format=None):

        username = request.query_params.get('username', None)

        if username is not None and len(username) >= 2:

            users = models.User.objects.filter(username__icontains=username)

            if users.count() < 1:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = serializers.ListUsersSerializer(users, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else :

            return Response(status=status.HTTP_400_BAD_REQUEST)


class FacebookLogin(SocialLoginView):
    
    adapter_class = FacebookOAuth2Adapter
