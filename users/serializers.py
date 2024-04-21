from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserReferralSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['phone',]


class UserRetrieveSerializer(serializers.ModelSerializer):
    referral_list = serializers.SerializerMethodField()

    def get_referral_list(self, object):
        return [UserReferralSerializer(item).data for item in User.objects.filter(refer=object.id)]

    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name', 'referral_code', 'referral_code_refer', 'refer', 'referral_list']


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
