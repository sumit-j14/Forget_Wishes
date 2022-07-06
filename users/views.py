# importing celery tasks
import json
from core.settings import free_trials
# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from celery_tasks.tasks import store_in_db
from limit_access.models import UsagePerUser


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        # authorization as per knox user model
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        # after login is successful

        # getting user data in request
        date = str(request.data.get('date'))
        month = str(print(request.data.get('month')))
        wish_who = str((request.data.get('wish_who')))
        custom_wish = str(print(request.data.get('custom_wish')))
        recipient_email = str((request.data.get('recipient_email')))
        entry = [str(user), date, month, wish_who, custom_wish, recipient_email]

        # checking user per limit
        can_avail_service = True  # boolean checker

        current_user = UsagePerUser.objects.get(user_name=str(user))
        # if a new user found
        if current_user is None:
            print("current user none")
            new_user = UsagePerUser(user_name=str(user), times_used=1)
            new_user.save()
        else:
            if current_user.times_used > free_trials:
                print("no more free trials available")
                can_avail_service = False
            else:
                # used service one more time
                past = current_user.times_used
                current_user.times_used = past+1
                current_user.save()

        if can_avail_service is True:
            # once usage limit per user is checked
            # this will spinup celery task of creating database entries
            store_in_db.apply_async(args=entry)
        return super(LoginAPI, self).post(request, format=None)
