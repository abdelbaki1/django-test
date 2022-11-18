from django.dispatch import Signal
from .models import User_activity
from  django.db.models.signals import post_migrate
from django.contrib.auth.models import Group,Permission


# ************defining signals*********************
user_activity_signal=Signal(providing_args=["activity"])
# logout_signal=Signal(providing_args=[''])
# create_signal
# update_signal
# delete_signal
# regiter_signal

# ***************************************************
patient_permission_dict={
            'products':
                {'Product':['change','add','view','delete']},
            'orders':
                {'OrderItem':['change','add','view','delete']},
        }
docter_permission_dict = {
            'products':
                {'Product':['view']},
            'orders':
                {'OrderItem':['view']},
        }
def get_permission(model_name,perm):
    codename :str = perm+'_'+model_name
    return Permission.objects.get(codename=codename.lower())

def __get_group(name_group:str,perms:dict):
    admin_group,Created=Group.objects.get_or_create(name='admin')
    if Created:
        admin_group.permissions.set(Permission.objects.all())
    group_obj,created=Group.objects.get_or_create(name=name_group)
    if created:
        for app_name,app_models in perms.items():
            for model_name,permissions in app_models.items():
                for permission in permissions:
                    # print(app_name, model_name, permission)
                    group_obj.permissions.add(get_permission(model_name, permission))
        group_obj.save()
    return group_obj


# ********************receivers function*********************
def print_user_connected(sender,activity,**kwargs):
    user_instance = User_activity.objects.create(user=sender)
    user_instance.activity=activity
    user_instance.save()
    # print(user_instance.date.ctime())
def create_instance(sender,**kwargs):
    print('postmigrations detected!!!!!')
    group_names=['doctor','patient']
    __get_group('doctor', docter_permission_dict)
    __get_group('patient', patient_permission_dict)





# ******************************Signals Connections*********************
user_activity_signal.connect(print_user_connected,weak=False)
post_migrate.connect(create_instance)
