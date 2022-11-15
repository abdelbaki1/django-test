from rest_framework import serializers
from .models import User, Permission, Role, User_activity


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class PermissionRelatedField(serializers.StringRelatedField):
    def to_representation(self, value):
        return PermissionSerializer(value).data

    def to_internal_value(self, data):
        return data


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionRelatedField(many=True)

    class Meta:
        model = Role
        fields = '__all__'

    def create(self, validated_data):
        permissions = validated_data.pop('permissions', None)
        instance = self.Meta.model(**validated_data)
        instance.save()
        instance.permissions.add(*permissions)
        instance.save()
        return instance


class RoleRelatedField(serializers.RelatedField):
    def to_representation(self, instance):
        return RoleSerializer(instance).data

    def to_internal_value(self, data):
        return self.queryset.get(pk=data)


class UserSerializer(serializers.ModelSerializer):
    # add required=false to allow setting it null in the input
    role = RoleRelatedField(many=False, required=False, queryset=Role.objects.all())

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'role', 'user_image']
        extra_kwargs = {
            # prevent password from been sent back
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop('password', None)

        roles = Role.objects.get(id=validated_data.get('role_id', 3))
        instance = self.Meta.model(
            **validated_data, role=roles,
            username=validated_data.get('last_name') + validated_data.get('first_name')
        )
        print(instance.role, "********************")
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    # def to_representation(self, instance):
    #     """Convert `username` to lowercase."""
    #     server_url="http://localhost:8000"
    #     ret = super().to_representation(instance)
    #     if(ret.get('user_image')):
    #         ret['user_image'] = str(server_url + ret['user_image'])
    #     return ret
class User_activity_serializer(serializers.ModelSerializer):
    class Meta:
        model = User_activity
        fields = '__all__'
    
    def to_representation(self,instance):
        obj=super().to_representation(instance)
        obj['user']=instance.user.email
        obj['date']=instance.date.ctime()
        return obj

