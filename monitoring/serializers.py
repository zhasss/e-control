from rest_framework import serializers
from django.contrib.auth import get_user_model

from geo.models import Region, District
from .models import (
    School,
    InspectionType,
    CriterionCategory,
    Criterion,
    Inspection,
    InspectionResult,
    MonitoringUser,
)

User = get_user_model()


# ---------- Справочники: регионы / районы / школы ----------

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "name"]


class DistrictSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = District
        fields = ["id", "name", "region"]


class SchoolSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    district = DistrictSerializer(read_only=True)

    class Meta:
        model = School
        fields = [
            "id",
            "os_id",
            "bin",
            "name",
            "name_kz",
            "name_kz_full",
            "name_ru_full",
            "region",
            "district",
            "locality",
            "license_date",
            "is_private",
        ]


# ---------- Критерии / категории / виды проверок ----------

class CriterionChildSerializer(serializers.ModelSerializer):
    """
    Подкритерий (листовой или нет). Обычно это "подколонка" из Excel.
    """
    class Meta:
        model = Criterion
        fields = [
            "id",
            "category",
            "parent",
            "code",
            "name",
            "value_type",
            "max_score",
            "order",
            "is_active",
            "excel_col",
        ]


class CriterionSerializer(serializers.ModelSerializer):
    """
    Критерий с детьми. Если parent=None — это группа/шапка,
    дети — реальные поля (подкритерии).
    """
    children = CriterionChildSerializer(many=True, read_only=True)

    class Meta:
        model = Criterion
        fields = [
            "id",
            "category",
            "parent",
            "code",
            "name",
            "value_type",
            "max_score",
            "order",
            "is_active",
            "excel_col",
            "children",
        ]


class CriterionCategorySerializer(serializers.ModelSerializer):
    """
    Категория (раздел) с древовидными критериями:
    отдаём только parent=None, внутри children будут подкритерии.
    """
    criterias = serializers.SerializerMethodField()

    class Meta:
        model = CriterionCategory
        fields = [
            "id",
            "inspection_type",
            "name",
            "order",
            "criterias",
        ]

    def get_criterias(self, obj: CriterionCategory):
        qs = obj.criterias.filter(parent__isnull=True).order_by("order", "id")
        return CriterionSerializer(qs, many=True).data


class InspectionTypeSerializer(serializers.ModelSerializer):
    categories = CriterionCategorySerializer(many=True, read_only=True)

    class Meta:
        model = InspectionType
        fields = [
            "id",
            "code",
            "name",
            "description",
            "is_active",
            "categories",
        ]


# ---------- Результаты по критериям ----------

class InspectionResultSerializer(serializers.ModelSerializer):
    """
    Значение по одному критерию в рамках проверки.
    """
    criterion = CriterionChildSerializer(read_only=True)

    # писать можно через criterion_id (как у тебя)
    criterion_id = serializers.PrimaryKeyRelatedField(
        queryset=Criterion.objects.all(),
        source="criterion",
        write_only=True,
    )

    class Meta:
        model = InspectionResult
        fields = [
            "id",
            "inspection",
            "criterion",
            "criterion_id",
            "value_bool",
            "value_int",
            "value_decimal",
            "value_text",
            "value_date",          # ✅ добавили
            "score",
            "has_violation",
            "violation_comment",
        ]
        read_only_fields = ["inspection"]

    def validate(self, attrs):
        """
        Защита от мусора:
        - нельзя писать значение в 'не тот' тип
        """
        criterion = attrs.get("criterion") or getattr(self.instance, "criterion", None)
        if not criterion:
            return attrs

        v_bool = attrs.get("value_bool")
        v_int = attrs.get("value_int")
        v_dec = attrs.get("value_decimal")
        v_text = attrs.get("value_text")
        v_date = attrs.get("value_date")

        # сколько полей заполнено
        filled = sum([
            v_bool is not None,
            v_int is not None,
            v_dec is not None,
            bool(v_text),
            v_date is not None,
        ])

        # разрешаем 0/1 как int в BOOLEAN если фронт так шлёт — но лучше bool
        if criterion.value_type == Criterion.ValueType.BOOLEAN:
            if v_int is not None and v_bool is None and v_int in (0, 1):
                attrs["value_bool"] = bool(v_int)
                attrs["value_int"] = None
                filled = sum([
                    attrs.get("value_bool") is not None,
                    attrs.get("value_int") is not None,
                    attrs.get("value_decimal") is not None,
                    bool(attrs.get("value_text")),
                    attrs.get("value_date") is not None,
                ])

        # если заполнили несколько типов одновременно — ошибка
        if filled > 1:
            raise serializers.ValidationError("Заполните только одно поле значения (по типу критерия).")

        # если не заполнили ничего — ок (черновик)
        if filled == 0:
            return attrs

        # проверка по value_type
        vt = criterion.value_type
        if vt == Criterion.ValueType.BOOLEAN and attrs.get("value_bool") is None:
            raise serializers.ValidationError("Для этого критерия нужно value_bool.")
        if vt == Criterion.ValueType.INTEGER and attrs.get("value_int") is None:
            raise serializers.ValidationError("Для этого критерия нужно value_int.")
        if vt == Criterion.ValueType.DECIMAL and attrs.get("value_decimal") is None:
            raise serializers.ValidationError("Для этого критерия нужно value_decimal.")
        if vt == Criterion.ValueType.DATE and attrs.get("value_date") is None:
            raise serializers.ValidationError("Для этого критерия нужно value_date.")
        if vt == Criterion.ValueType.TEXT and not attrs.get("value_text"):
            raise serializers.ValidationError("Для этого критерия нужно value_text.")

        return attrs


# ---------- Акт проверки (Inspection) ----------

class InspectionSerializer(serializers.ModelSerializer):
    """
    Акт проверки.

    На запись:
      - inspection_type_id
      - school_id
      - year
      - date_visit
      - comment

    Регион и район подставляются из школы (в модели Inspection),
    инспектор = текущий пользователь (в perform_create),
    статус/итог/даты отправки и утверждения контролируются бэком.
    """

    # вложенные объекты только для чтения
    school = SchoolSerializer(read_only=True)
    region = RegionSerializer(read_only=True)
    district = DistrictSerializer(read_only=True)
    inspection_type = InspectionTypeSerializer(read_only=True)

    # поля для записи
    school_id = serializers.PrimaryKeyRelatedField(
        queryset=School.objects.all(),
        source="school",
        write_only=True,
    )
    inspection_type_id = serializers.PrimaryKeyRelatedField(
        queryset=InspectionType.objects.filter(is_active=True),
        source="inspection_type",
        write_only=True,
    )

    inspector = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Inspection
        fields = [
            "id",

            "inspection_type",
            "inspection_type_id",

            "school",
            "school_id",

            "region",
            "district",

            "year",
            "date_visit",

            "inspector",
            "status",
            "total_score",
            "comment",

            # ✅ NEW: даты отправки/утверждения
            "submitted_at",
            "approved_at",

            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "inspection_type",
            "school",
            "region",
            "district",
            "inspector",
            "status",
            "total_score",

            # ✅ NEW: read-only
            "submitted_at",
            "approved_at",

            "created_at",
            "updated_at",
        ]

# ---------- /me и профиль мониторинга ----------

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "is_superuser"]


class MonitoringUserSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    region = RegionSerializer(read_only=True)
    district = DistrictSerializer(read_only=True)
    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = MonitoringUser
        fields = [
            "id",
            "user",
            "role",
            "role_display",
            "region",
            "district",
        ]
