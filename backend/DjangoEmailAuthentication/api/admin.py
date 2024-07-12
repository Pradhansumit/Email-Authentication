from django.contrib import admin

from api.models import CustomUser, TokenModel


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    class Meta:
        fields = "__all__"


@admin.register(TokenModel)
class TokenModelAdmin(admin.ModelAdmin):
    class Meta:
        fields = "__all__"
