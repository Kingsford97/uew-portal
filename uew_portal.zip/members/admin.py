from django.contrib import admin
from .models import MemberProfile, PaymentAccount, DuesSettings

admin.site.register(MemberProfile)
admin.site.register(PaymentAccount)
admin.site.register(DuesSettings)