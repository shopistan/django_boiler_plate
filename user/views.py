"""
user views
"""
from collections import OrderedDict

from django.contrib.auth.models import Group, Permission, ContentType
from django.db.models import Q
from rest_auth.registration.views import RegisterView, VerifyEmailView
from rest_auth.views import PasswordResetView, PasswordResetConfirmView
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import User
# Also add these imports
from .permissions import IsAdminUser, IsLoggedInUserOrAdmin
from .serializers import GroupSerializer, UserSerializer, PermissionSerializer
import traceback
import logging
logger = logging.getLogger('user')

class UserViewSet(viewsets.ModelViewSet):
    """
    user view sets
    """
    # queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination



    def create(self, request, **kwargs):
        """

        Args:
            **kwargs:
            request:

        Returns:

        """
        user = UserSerializer(data=request.data)
        groups = request.data.get("groups")
        user.is_valid(raise_exception=True)
        user.save(groups=groups)
        if user.data:
            user_id = user.data["id"]
            action_data = {
                "message_type" : "User Created",
                "message" : f"UserId : {user_id}",
                "user_id" : request.user.id,
                "model_name" : "User",
                "data" : user.data
            }
            UserActionsHistory(action_data)
        return Response(user.data, status.HTTP_200_OK)

    def update(self, request, pk=None, **kwargs):
        """

        Args:
            **kwargs:
            request:
            pk:

        Returns:

        """
        instance = self.get_object()
        groups = request.data.get("groups")
        if request.data['password'] == '':
            request.data['password'] = 'null'
        user = UserSerializer(instance, data=request.data)
        user.is_valid(raise_exception=True)
        user.save(groups=groups)
        if user.data:
            user_id = user.data["id"]
            action_data = {
                "message_type" : "User Updated",
                "message" : f"UserId : {user_id}",
                "user_id" : request.user.id,
                "model_name" : "User",
                "data" : user.data
            }
            UserActionsHistory(action_data)
        return Response(user.data, status.HTTP_200_OK)

    def destroy(self, request, pk=None, **kwargs):
        """

        Args:
            **kwargs:
            request:
            pk:

        Returns:

        """
        try:
            user = User.objects.get(id = pk)
            user.delete()
        except User.DoesNotExist:
            Response({"error": "User doesn't exist!"}, status.HTTP_400_BAD_REQUEST)
        except Exception as e: 
            Response({"error": e}, status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "User deleted successfully"}, status.HTTP_200_OK)



    def list(self, request):
        """get users list
        
        Args:
            request ([type]): [description]
        
        Returns:
            [type]: [description]
        """
        if self.request.user.is_superuser:
            search = request.query_params.get('search', None)
            if search is not None:
                query = Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search)
                if search.lower() == "yes":
                    search = True
                    query = query | Q(is_verified__icontains=search) | Q(is_active__icontains=search)
                elif search.lower() == "no":
                    search = False
                    query = query | Q(is_verified__icontains=search) | Q(is_active__icontains=search)

                elif search.lower() == "admin":
                    search = True
                    query = query | Q(is_staff__icontains=search)
                elif search.lower() == "staff":
                    search = False
                    query = query | Q(is_staff__icontains=search)
                queryset=User.objects.filter(query).order_by('id').reverse().values()
            else:
                queryset = User.objects.all().order_by('id').reverse().values()
            if request is not None:
                paginator = LimitOffsetPagination()
                paginator.max_limit = 100
                paginator.default_limit = 20
                user= paginator.paginate_queryset(queryset, request)
                limit = paginator.limit
                if isinstance(limit, list):
                    limit = limit[0]
                offset = paginator.offset
                count = paginator.count
            res = {"Success": True,  "ExceptionString":"Record Found.", "results":user, "count": count, "limit":limit, "offset": offset}
            return Response(res, status.HTTP_200_OK)
        else:
            res = {"Success": False, "results": []}
            return Response(res, status.HTTP_401_UNAUTHORIZED)
        
        
        
    def get_queryset(self):
        """

        Returns:

        """
        queryset = User.objects.filter()
        search = self.request.query_params.get('search')
        sort_field = self.request.query_params.get('sort')
        q = Q()
        if search is not None:
            q |= Q(email__contains=search) | Q(username__contains=search) | Q(first_name__contains=search) | Q(
                last_name__contains=search) | Q(groups__name__contains=search)
        if self.request.user.is_superuser:
            if q:
                queryset = queryset.filter(q).distinct('id')
        if sort_field:
            queryset = queryset.order_by(sort_field)
        else:
            queryset = queryset.order_by('id')

        return queryset

    def get_permissions(self):
        """

        Returns:

        """
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminUser, ]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list':
            permission_classes = [IsAdminUser, ]
        return [permission() for permission in permission_classes]


@permission_classes([IsAdminUser])
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request, **kwargs):
        """

        Args:
            **kwargs:
            request:

        Returns:

        """
        group = GroupSerializer(data=request.data)
        group.is_valid(raise_exception=True)
        group.save(permissions=request.data["permissions"])
        return Response(group.data, status.HTTP_200_OK)

    def update(self, request, pk=None, **kwargs):
        """

        Args:
            **kwargs:
            request:
            pk:

        Returns:

        """
        instance = self.get_object()
        group = GroupSerializer(instance, data=request.data)
        group.is_valid(raise_exception=True)
        group.save(permissions=request.data["permissions"])
        return Response(group.data, status.HTTP_200_OK)

    def list(self, request):
        """get groups list
        
        Args:
            request ([type]): [description]
        
        Returns:
            [type]: [description]
        """
        try:
            groups = Group.objects.all().order_by('id').values()
            res = {"Success": True, "data":groups}
            return Response(res, status.HTTP_200_OK)
        except Exception as e:
            print("EXCEPTION list GroupViewSet: ", e)
            return Response({"Success": False, "data":[]}, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getPermissions(request):
    """

    Args:
        request:

    Returns:

    """
    response = None
    custom_content_type = ContentType.objects.filter(app_label='custom').first()
    if custom_content_type:
        response = Permission.objects.filter(content_type=custom_content_type).order_by('id')
        response = PermissionSerializer(response, many=True).data
    return Response(response, status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getallRolesPermissions(request):
    """

    Args:
        request:

    Returns:

    """
    try:
        response = None
        custom_content_type = ContentType.objects.filter(app_label='custom').first()
        group_permissions = []
        if custom_content_type:
            groups =  Group.objects.all()
            for group in groups:
                group_data = GroupSerializer(group, many=False).data
                print(group_data)
                group_permission = group.permissions.all()
                group_permission = group_permission.filter(content_type=custom_content_type)
                group_permission = PermissionSerializer(group_permission,many=True).data
                dict_obj = {
                    'id' : group_data['id'],
                    'name' : group_data['name'],
                    'permissions' : group_permission
                }
                group_permissions.append(dict_obj)
            response = Permission.objects.filter(content_type=custom_content_type)
            response = PermissionSerializer(response, many=True).data
            super_user = {
                'name' : "Super Admin",
                'permissions' : response
            }
            group_permissions.append(super_user)
        return Response(group_permissions, status.HTTP_200_OK)
    except Exception as e:
        trace_back = traceback.format_exc()
        message = "EXCEPTION: " + str(e)+ " " + str(trace_back)
        return Response(message, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserPermissions(request):
    """

    Args:
        request:

    Returns:

    """
    try:
        response = None
        custom_content_type = ContentType.objects.filter(app_label='custom').first()
        if custom_content_type:
            user_groups = request.user.groups.filter().order_by('id')
            response = Permission.objects.filter(content_type=custom_content_type)
            if not request.user.is_superuser:
                q = Q(user=request.user) | Q(group__in=user_groups.values_list("id", flat=True))
                response = response.filter(q)
            response = PermissionSerializer(response, many=True).data
        return Response(response, status.HTTP_200_OK)
    except Exception as e:
        trace_back = traceback.format_exc()
        message = "EXCEPTION: " + str(e)+ " " + str(trace_back)
        return Response(message, status.HTTP_200_OK)