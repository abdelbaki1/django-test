from django.contrib import admin
from .models import Permission, Role, User, User_activity, token

admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(User_activity)
admin.site.register(token)

# Register your models here.
