from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)
from django_reverse_admin import ReverseModelAdmin
from nested_admin.nested import NestedStackedInline
from .models import (
    Apartment,
    MetroStation,
    District,
    City,
    Region,
    House,
    User, Image
)


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('phone',)


class CustomUserAdmin(UserAdmin):
    add_form_template = "admin/auth/user/add_form.html"
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ["phone", "email", "first_name", "last_name"]}),
    )
    add_fieldsets = (
        (None, {'fields': ["phone", "email", "password1", "password2"]}),
    )
    list_display = ("phone", "email", "first_name", "last_name")
    list_filter = ("is_superuser",)
    search_fields = ("phone", "first_name", "last_name", "email")
    ordering = ("last_name",)
    add_form = CustomUserCreationForm
    form = CustomUserCreationForm


class ImageInline(NestedStackedInline):
    model = Image
    max_num = 3


class ApartmentAdmin(ReverseModelAdmin):
    inline_type = 'tabular'
    inline_reverse = ['metro_station', 'house'
                      ]
    inlines = [ImageInline]


admin.site.register(Apartment, ApartmentAdmin)



# class MetroStationInline(NestedStackedInline):
#     model = MetroStation
#     max_num = 1
#
# class ApartmentAdmin(admin.ModelAdmin):
#     inlines = [MetroStationInline]


admin.site.register(User, CustomUserAdmin)
admin.site.register(House)
admin.site.register(MetroStation)
admin.site.register(District)
admin.site.register(City)
admin.site.register(Region)





