from django.contrib import admin

from .models import (
    School,
    InspectionType,
    CriterionCategory,
    Criterion,
    Inspection,
    InspectionResult,
)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "district", "is_private")
    list_filter = ("region", "district", "is_private")
    search_fields = ("name", "bin")


@admin.register(InspectionType)
class InspectionTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "name")


@admin.register(CriterionCategory)
class CriterionCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "inspection_type", "order")
    list_filter = ("inspection_type",)
    ordering = ("inspection_type", "order")
    search_fields = ("name",)


@admin.register(Criterion)
class CriterionAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "value_type", "max_score", "order", "is_active")
    list_filter = ("category", "value_type", "is_active")
    ordering = ("category", "order")
    search_fields = ("name", "code")


class InspectionResultInline(admin.TabularInline):
    model = InspectionResult
    extra = 0


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ("school", "inspection_type", "region", "district", "year", "date_visit", "status", "total_score")
    list_filter = ("inspection_type", "region", "district", "year", "status")
    search_fields = ("school__name",)
    inlines = [InspectionResultInline]
