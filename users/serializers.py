from rest_framework import serializers

from users.models import UserProfile,UserHistory,UserCollection


class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
        model = UserProfile
        fields =  ('id','password','username','email','birthday','gender','address','image','phone','create_time')


class UserHistorySerializer(serializers.ModelSerializer):
  class Meta:
        model = UserHistory
        fields =  '__all__'


class UserCollectionSerializer(serializers.ModelSerializer):
  class Meta:
        model = UserCollection
        fields = '__all__'
