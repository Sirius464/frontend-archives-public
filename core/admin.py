from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change and obj.poste:
            # Sauvegarder l'ancien poste avant la modification
            old_obj = User.objects.get(pk=obj.pk)
            obj._old_poste = old_obj.poste
        super().save_model(request, obj, form, change)


admin.site.register(ValidationHistory)
admin.site.register(Direction)
admin.site.register(Service)
admin.site.register(Poste)
admin.site.register(FolderType)
admin.site.register(PieceType)
admin.site.register(Keyword)
admin.site.register(Folder)
admin.site.register(Piece)
admin.site.register(PieceHistory)
admin.site.register(FolderHistory)
admin.site.register(FolderPermission)
admin.site.register(PiecePermission)
admin.site.register(TrashItem)
admin.site.register(FolderKeyword)
admin.site.register(PieceKeyword)
