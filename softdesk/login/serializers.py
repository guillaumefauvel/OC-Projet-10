from django.db.models import Q

from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    ValidationError,
)

from .models import User

class UserCreateSerializer(ModelSerializer):

    email_2 = EmailField(label='Confirm Email')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
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
        return value

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
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        user_obj = User(
            username = username,
            email = email,
            first_name = first_name,
            last_name = last_name
        )
        user_obj.set_password(password)
        user_obj.save()

        return validated_data


class UserLoginSerializer(ModelSerializer):

    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True)
    email = EmailField(label='Email Adress', required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',
        ]

        extra_kwargs = {'password':
                            {'write_only': True}
                        }

    def validate(self, data):
        user_obj = None
        email = data.get('email', None)
        username = data.get('username', None)
        password = data['password']

        if not email and not username:
            raise ValidationError('A username or an email is required to login')

        user = User.objects.filter(
            Q(email=email) |
            Q(username=username)
        ).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError('This username/email is not valid')

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError('Incorrect password, pleade try again')
        else:
            raise ValidationError('Plase insert a correct login')

        data['token'] = "SOME RANDOM TOKEN"

        return data