from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    EmailField,
    HyperlinkedModelSerializer,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)

User = get_user_model()

class UserCreateSerializer(ModelSerializer):
    email_2 = EmailField(label='Confirm Email')
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'email_2',
        ]
        extra_kwargs = {
            'password':{'write_only': True}
        }

    def validate_email(self, value):

        user_qs = User.objects.filter(email=value)
        if user_qs.exists():
            raise ValidationError('This email is already attach to an account.')

    def validate_email_2(self, value):

        data = self.get_initial()
        email_1 = data.get("email")
        email_2 = value

        if email_1 != email_2:
            raise ValidationError('Email must match.')

        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username = username,
            email = email,
        )
        user_obj.set_password(password)
        user_obj.save()

        return validated_data
