from django.contrib import admin
from .models import EquipmentIssue, EquipmentIssueTag, OtherUsers, Tag
from django.utils.html import format_html


# Register your models here.

class EquipmentIssueAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'equipment_category', 'is_issued', 'status', 'serial_number')
    list_filter = ('active', 'is_issued', 'date_of_issue')
    list_editable = ('is_issued',)
    search_fields = ('name', 'department')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(EquipmentIssue, EquipmentIssueAdmin)


class EquipmentIssueTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('active',)
    search_fields = ('name',)
    prepolated_fields = {'slug': ('name',)}
    autocomplete_fields = ('equipmentIssues',)


admin.site.register(EquipmentIssueTag, EquipmentIssueTagAdmin)
admin.site.register(OtherUsers)
admin.site.register(Tag)
