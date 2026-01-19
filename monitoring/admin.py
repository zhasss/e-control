from django.contrib import admin

from .models import (
    School,
    InspectionType,
    CriterionCategory,
    Criterion,
    Inspection,
    InspectionResult,
    MonitoringUser,
)


# ---------- School ----------

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "district", "is_private")
    list_filter = ("region", "district", "is_private")
    search_fields = ("name", "bin")


# ---------- InspectionType ----------

@admin.register(InspectionType)
class InspectionTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "name")


# ---------- CriterionCategory ----------

@admin.register(CriterionCategory)
class CriterionCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "inspection_type", "order")
    list_filter = ("inspection_type",)
    ordering = ("inspection_type", "order")
    search_fields = ("name",)


# ---------- Criterion (parent/children) ----------

class CriterionChildInline(admin.TabularInline):
    """
    Подкритерии (дети) внутри родительского критерия.
    """
    model = Criterion
    fk_name = "parent"
    extra = 0
    fields = ("name", "code", "excel_col", "value_type", "max_score", "order", "is_active")
    ordering = ("order",)
    show_change_link = True


@admin.register(Criterion)
class CriterionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "category",
        "parent",
        "excel_col",
        "value_type",
        "max_score",
        "order",
        "is_active",
    )
    list_filter = ("category", "value_type", "is_active")
    ordering = ("category", "parent_id", "order", "id")
    search_fields = ("name", "code")
    autocomplete_fields = ("parent", "category")
    inlines = [CriterionChildInline]


# ---------- Inspection + results inline ----------

class InspectionResultInline(admin.TabularInline):
    model = InspectionResult
    extra = 0
    autocomplete_fields = ("criterion",)
    fields = (
        "criterion",
        "value_bool",
        "value_int",
        "value_decimal",
        "value_text",
        "value_date",   # если добавил в модели
        "score",
        "has_violation",
        "violation_comment",
    )
    show_change_link = True


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = (
        "school",
        "inspection_type",
        "region",
        "district",
        "year",
        "date_visit",
        "status",
        "total_score",
    )
    list_filter = ("inspection_type", "region", "district", "year", "status")
    search_fields = ("school__name",)
    inlines = [InspectionResultInline]


# ---------- MonitoringUser ----------

@admin.register(MonitoringUser)
class MonitoringUserAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "region", "district")
    list_filter = ("role", "region", "district")
    search_fields = ("user__username", "user__last_name", "user__first_name")
