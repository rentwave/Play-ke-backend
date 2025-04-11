from django.urls import re_path
from user_manager.models import CustomUser, UserWallet
from django.db.models import Q
from django.http import JsonResponse


class UserManagement(object):
    """This method is responsible for creation, update and deletion of user registration"""


    def __init__(self):
        pass


    def create_user(self, **kwargs):
        """
        This method creates a user with the given kwargs.
        After creating the user, the user billing account is created as well,
        and password is set for the user
        :param kwargs: key=>value methods to pass to the create method.
        :return: Created object or None on error.
        """
        try:
            full_name = kwargs.get("full_name")
            if not full_name:
                return JsonResponse({"status": "failed", "message": "Missing full name"})
            email = kwargs.get("email")
            if not email:
                return JsonResponse({"status": "failed", "message": "Missing email"})
            phone_number = kwargs.get("phone_number")
            if not phone_number:
                return JsonResponse({"status": "failed", "message": "Missing phone number"})
            password = kwargs.get("password")
            if not password:
                return JsonResponse({"status": "failed", "message": "Missing password"})
            # Create user first
            user = CustomUser.objects.get(phone_number=phone_number)
            if user:
                return JsonResponse({"status": "failed", "message": "User already exists"})
            user = CustomUser.objects.create(
                full_name=full_name, email=email, phone_number=phone_number, password=password
            )
            if not user:
                return JsonResponse({"status": "failed", "message": "Failed creating user"})
            # Set user password
            user.set_password(password)
            # Create user wallet
            user_wallet = UserWallet.objects.get(user=user)
            if user_wallet:
                return JsonResponse({"status": "failed", "message": "User wallet already exists"})
            user_wallet = UserWallet.objects.create(
                user=user, wallet_balance=0.0, wallet_currency="KES", account_number=phone_number
            )
            if not user_wallet:
                return JsonResponse({"status": "failed", "message": "Failed creating user wallet"})
            return JsonResponse({"code": "100.000.000", "status": "success", "context": "User created successfully"})
        except Exception as e:
            pass  # lgr.exception('%s Service create exception: %s' % (self.manager.model.__name__, e))
        return JsonResponse({"code": "500.001.012", "status": "failed", "context": "Failed creating user"})

    def authenticate_user(self, **kwargs):
        """
        This method authenticates the user with the given kwargs.
        :param kwargs: key=>value methods to pass to the create method.
        :return: Created object or None on error.
        """
        try:
            phone_number = kwargs.get("phone_number", "")
            email = kwargs.get("email", "")
            password = kwargs.get("password")
            if not password:
                return {"status": "failed", "message": "Missing password"}
            # Authenticate user
            user = CustomUser.objects.get(Q(phone_number=phone_number) | Q(email=email))
            if not user:
                return {"status": "failed", "message": "User does not exist"}
            if not user.check_password(password):
                return {"status": "failed", "message": "Invalid password"}
            return {"code": "100.000.000", "status": "success", "context": "User authenticated successfully"}
        except Exception as e:
            pass


urlpatterns = [
    re_path(r'^onboard/$', UserManagement.create_user),
    re_path(r'^authenticate/$', UserManagement.authenticate_user),
]
