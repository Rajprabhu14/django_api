from rest_framework import serializers
from django.contrib.auth.admin import User
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
            max_length=32,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    first_name = serializers.CharField(
            max_length=32
            )
    last_name = serializers.CharField(
            max_length=32
            )
    # testcase response hiding of password field
    password = serializers.CharField(min_length=8, write_only=True)
# EmailField & usernameField  that it is required and should be unique amongst all User objects in our database.
#  the regular create method wont't work, so we have to use the create_uer method while using Sjango built-in authentication system

    def create(self, validated_data):
        user = User.objects.create_user(
                validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                is_active=False)
        return user

    class Meta:
        model = User
        fields = ('email', 'username', 'email', 'password', 'first_name', 'last_name')