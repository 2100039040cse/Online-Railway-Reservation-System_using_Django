
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined', 'get_aadhar', 'get_dob', 'get_address', 'get_phoneno', 'get_mailid')

    def get_aadhar(self, instance):
        return instance.userprofile.aadhar

    def get_dob(self, instance):
        return instance.userprofile.dob

    def get_address(self, instance):
        return instance.userprofile.address

    def get_phoneno(self, instance):
        return instance.userprofile.phoneno

    def get_mailid(self, instance):
        return instance.userprofile.mailid

    get_aadhar.short_description = 'Aadhar'
    get_dob.short_description = 'D.O.B'
    get_address.short_description = 'Address'
    get_phoneno.short_description = 'Phone No'
    get_mailid.short_description = 'Email Id'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
