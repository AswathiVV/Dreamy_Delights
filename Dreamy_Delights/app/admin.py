from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Cake)
admin.site.register(Cart)
admin.site.register(Buy)
admin.site.register(Address)