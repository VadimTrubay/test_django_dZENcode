from rest_framework_simplejwt.tokens import AccessToken
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers

from .models import CustomUser


class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise exceptions.AuthenticationFailed(_("Invalid email or password"))

            if not user.check_password(password):
                raise exceptions.AuthenticationFailed(_("Invalid email or password"))

            access_token = AccessToken.for_user(user)
            return {
                "access_token": str(access_token),
            }
        else:
            raise exceptions.AuthenticationFailed(
                _("Must include 'email' and 'password'.")
            )


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password", "home_page")

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            home_page=validated_data.get("home_page", None),
        )

        access_token = AccessToken.for_user(user)

        return {"access_token": str(access_token)}


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "home_page")
