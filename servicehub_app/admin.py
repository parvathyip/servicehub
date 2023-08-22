from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Login)
admin.site.register(Brand)
admin.site.register(ServicehubReg)
admin.site.register(Faq)
admin.site.register(Serviceproducts)
admin.site.register(UserReg)
admin.site.register(Troubleshoot)
admin.site.register(Complaint)
admin.site.register(ComplaintRequire)
# admin.site.register(Feedback)