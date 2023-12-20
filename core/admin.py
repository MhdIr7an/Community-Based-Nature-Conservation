from django.contrib import admin
from .models import Base_User, Base_Events, Base_Volunteer, Base_Issue, Base_Items, Base_Order, Base_Resources, Base_Donations, Base_Discussions

admin.site.register(Base_User)
admin.site.register(Base_Events)
admin.site.register(Base_Volunteer)
admin.site.register(Base_Issue)
admin.site.register(Base_Items)
admin.site.register(Base_Order)
admin.site.register(Base_Resources)
admin.site.register(Base_Donations)
# admin.site.register(Base_DonatorDetails)
admin.site.register(Base_Discussions)