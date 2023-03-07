from rest_framework import serializers

from .models import *


class AuthorizationSerializer(serializers.ModelSerializer):
    """ Authorization serializer """

    token = serializers.CharField(max_length=255, read_only=True)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50, write_only=True)

    def create(self, validated_data):
        is_signup = self.context['signup']
        user, created = User.objects.get_or_create(username=validated_data.get('username'))
        if created:
            if not is_signup:
                user.delete()
                raise serializers.ValidationError({'info': 'Bad username/password'})
            user.set_password(validated_data.get('password'))
            user.save()
        else:
            if is_signup:
                raise serializers.ValidationError({'info': f'User with username {validated_data.get("username")} already exists'})
            if not user.check_password(validated_data.get('password')):
                raise serializers.ValidationError({'info': 'Bad username/password'})
        return user

    class Meta:
        model = User
        fields = ["token", "username", "password"]


class UserDetailSerializer(serializers.ModelSerializer):
    """
    User detail serializer
    """

    class Meta:
        model = User
        fields = ['username',]


class NoteSerializer(serializers.ModelSerializer):
    """
    Note serializer
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        note = Note.objects.create(
            title=validated_data.get('title'), 
            description=validated_data.get('description'), 
            user=self.context.get('request').user
        )
        note.save()
        return note
    
    def update(self, instance: Note, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    class Meta:
        model = Note
        fields = '__all__'


class NoteListSerializer(serializers.ModelSerializer):
    avg = serializers.ReadOnlyField()
    cnt = serializers.ReadOnlyField()
    rating = serializers.ReadOnlyField()
    anno = serializers.ReadOnlyField()
    group = serializers.ReadOnlyField()
    post = serializers.ReadOnlyField()

    class Meta:
        model = Note
        exclude = ('text',)
