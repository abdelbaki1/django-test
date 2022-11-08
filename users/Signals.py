from django.dispatch import Signal
from .models import User_activity
from  django.db.models.signals import post_save


# ************defining signals*********************
user_activity_signal=Signal(providing_args=["activity"])
# logout_signal=Signal(providing_args=[''])
# create_signal
# update_signal
# delete_signal
# regiter_signal

# ***************************************************


# ********************receivers function*********************
def print_user_connected(sender,activity,**kwargs):
    user_instance = User_activity.objects.create(user=sender)
    user_instance.activity=activity
    user_instance.save()
    # print(user_instance.date.ctime())




# ******************************Signals Connections*********************
user_activity_signal.connect(print_user_connected,weak=False)
