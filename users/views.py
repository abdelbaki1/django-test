from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, GenericAPIView, UpdateAPIView, CreateAPIView
from rest_framework.generics import DestroyAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from testproject.pagination import CustomPagination
from .auth import generate_access_token, JWTAuthentication
from .models import User, Permission, Role, User_activity, token
from .Signals import user_activity_signal
from .auth import JWTAuthentication
# from .permission import ViewPermissions
from .serializers import UserSerializer, PermissionSerializer, RoleSerializer, User_activity_serializer


@api_view(['POST'])
def register(request):
    data = request.data
    print(data)
    if data['password'] != data['password_confirm']:
        raise exceptions.APIException('Passwords do not match!')

    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user_activity_signal.send(sender=serializer.save(),activity=' just registered')
    return Response(serializer.data)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = User.objects.filter(email=email).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found!')
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Incorrect Password!')
    response = Response()
    token = generate_access_token(user)
    res=user_activity_signal.send(sender=user, activity='have logged in !!')
    print(res)
    response.set_cookie(key='jwt', value=token, httponly=True, samesite='none', secure=True)
    response.data = {
        'jwt': token
    }
    return response


@api_view(['POST'])
# @login_required(redirect_field_name='login_view')
def logout(request):
    response = Response()
    t=request.COOKIES.get('jwt')
    response.delete_cookie(key='jwt')
    request.user=JWTAuthentication().authenticate(request)[0]
    if(request.user):
        user_activity_signal.send(sender=request.user, activity='have logged out from his account')
    


    response.data = {
        'message': 'Success'
    }
    # user_activity_signal.send(sender=,activity='user has just logout frm the system')
    return response


class AuthenticatedUser(APIView):
    '''return the current user along with it's permission'''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = UserSerializer(request.user).data
        # print(data)
        if data['role']:
            data['permissions'] = [p['name'] for p in data['role']['permissions']]
        return Response(data)


class PermissionAPIView(ListAPIView):
    '''
    return all the permission in a list
    '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class genericroleview(GenericAPIView):
    '''
    generic api config for the role model
    '''
    authentication_classes = [JWTAuthentication]
    serializer_class = RoleSerializer
    queryset = Role.objects.all()


class listroleview(genericroleview, ListAPIView):
    '''
    return list of role
    '''
    # permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class RoleViewSet(genericroleview, RetrieveUpdateDestroyAPIView, CreateAPIView):
    '''return a role,create,update,delete'''

    permission_classes = [IsAuthenticated]
    permission_object = 'roles'
    lookup_field = "id"
    lookup_url_kwarg = "pk"


    def post(self, request, *args, **kwargs):
        user_activity_signal.send(sender=request.user, activity='have created a role')
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        user_activity_signal.send(sender=request.user, activity='have updated a role')
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        user_activity_signal.send(sender=request.user,activity='have deleted a role')
        return self.destroy(request, *args, **kwargs)


class UserGenericAPIView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserlistAPI(UserGenericAPIView, ListAPIView):
    '''
    return a list of all users
    '''
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class UserAPIView(UserGenericAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView):
    '''retrieve ,update,delete create a user'''
    permission_classes = [IsAuthenticated]
    permission_object = 'users'
    lookup_field = "id"
    lookup_url_kwarg = 'pk'
    

    def perform_create(self, serializer):
        serializer.save(role_id=self.request.data.get('role_id'))

    def update(self, request, *args, **kwargs):
        # print("update has been hit***********************************")
        # partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user = User.objects.get(id=instance.id)
        user.email = request.data.get('email')
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        roles = Role.objects.get(id=request.data.get('role_id'))
        user.role = roles
        user.save()
        return Response(UserSerializer(user).data)


class ProfileInfoAPIView(UpdateAPIView):
    '''
    updateuserinfo
    '''
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        print("update has been hitttz")
        # partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user = User.objects.get(id=instance.id)
        user.email = request.data.get('email')
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user.user_image=request.data.get('user_image')
        
        user.save(update_fields=request.data.keys())
        user_activity_signal.send(user,activity='have updated his profile')
        return Response(UserSerializer(user).data)


class ProfilePasswordAPIView(APIView):
    '''
    update the password
    '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        if request.data['password'] != request.data['password_confirm']:
            raise exceptions.ValidationError('Passwords do not match')
        user.set_password(request.data['password'])
        user.save()
        serializer = UserSerializer(user)
        user_activity_signal.send(sender=user,activity='has changed his password')
        return Response(serializer.data)
class UserActivityView(ListAPIView):
    serializer_class = User_activity_serializer
    queryset = User_activity.objects.all()
    pagination_class = CustomPagination
    
