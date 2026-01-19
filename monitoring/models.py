from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.core.exceptions import ValidationError

from geo.models import Region, District

User = get_user_model()


class School(models.Model):
    """
    Организация образования из ОСО (лист 'Сеть').
    """

    os_id = models.PositiveIntegerField("ID из ОСО", unique=True, null=True, blank=True)
    bin = models.CharField("БИН", max_length=12, blank=True)

    kato_ar = models.CharField("kato_ar", max_length=20, blank=True)
    kato_reg = models.CharField("kato_reg", max_length=20, blank=True)
    kato_np = models.CharField("kato_np", max_length=20, blank=True)

    region = models.ForeignKey(Region, on_delete=models.PROTECT, verbose_name="Область")
    district = models.ForeignKey(District, on_delete=models.PROTECT, verbose_name="Район")
    locality = models.CharField("Населенный пункт", max_length=255, blank=True)

    name = models.CharField("Наименование организации (кратко)", max_length=255)
    name_kz = models.CharField("Наименование организации каз", max_length=255, blank=True)
    name_kz_full = models.TextField("Наименование организации каз полное", blank=True)
    name_ru_full = models.TextField("Наименование организации рус полное", blank=True)

    edu_org_type = models.CharField("Тип организации образования", max_length=255, blank=True)
    org_kinds = models.CharField("Виды организации", max_length=255, blank=True)
    ownership_form = models.CharField("Форма собственности", max_length=255, blank=True)
    department = models.CharField("Ведомственная принадлежность", max_length=255, blank=True)
    territory = models.CharField("Территориальная принадлежность", max_length=255, blank=True)
    education_levels = models.CharField("По уровням образования", max_length=255, blank=True)
    founders = models.CharField("Основные учредители", max_length=255, blank=True)
    teaching_language = models.CharField("Язык обучения", max_length=255, blank=True)
    education_form = models.CharField("Форма обучения", max_length=255, blank=True)

    legal_address_kz = models.TextField("Адрес юридический на казахском", blank=True)
    legal_address_ru = models.TextField("Адрес юридический на русском", blank=True)

    np_part_type = models.CharField("Тип составной части населенного пункта", max_length=255, blank=True)
    np_part_name = models.CharField("Наименование составной части населенного пункта", max_length=255, blank=True)
    house_number = models.CharField("№ дома", max_length=50, blank=True)

    head_full_name = models.CharField("ФИО руководителя", max_length=255, blank=True)
    acting_head_full_name = models.CharField("ФИО и.о. руководителя", max_length=255, blank=True)
    acting_head_position = models.CharField("Должность и.о. руководителя", max_length=255, blank=True)

    phone_work = models.CharField("Рабочий телефон", max_length=100, blank=True)
    phone_mobile = models.CharField("Сотовый телефон", max_length=100, blank=True)
    fax = models.CharField("Факс", max_length=100, blank=True)
    email = models.CharField("E-mail организации образования", max_length=255, blank=True)
    website = models.CharField("Сайт", max_length=255, blank=True)
    postal_index = models.CharField("Почтовый индекс", max_length=20, blank=True)

    study_week = models.CharField("Учебная неделя", max_length=50, blank=True)
    open_date = models.DateField("Дата открытия", null=True, blank=True)
    status = models.CharField("Статус", max_length=255, blank=True)
    location = models.CharField("Расположен", max_length=255, blank=True)
    legal_form = models.CharField("Организационно-правовая форма", max_length=255, blank=True)

    license_authority = models.CharField(
        "Кем выдана лицензия на право образовательной деятельности",
        max_length=255,
        blank=True,
    )
    license_number = models.CharField("Номер лицензии", max_length=100, blank=True)
    license_date = models.DateField("Дата выдачи лицензии", null=True, blank=True)

    complex_school_kindergarten = models.CharField("Комплекс «школа-ясли-сад»", max_length=50, blank=True)
    complex_special_school_kindergarten = models.CharField(
        "Специальный комплекс «школа-ясли-сад»", max_length=50, blank=True
    )
    shifts_count = models.PositiveIntegerField("Количество смен", null=True, blank=True)
    special_classes_count = models.PositiveIntegerField("Количество спец классов", null=True, blank=True)

    # ⚠️ строка, но в Excel нам 1/0.
    # Экспорт идёт из InspectionResult, поэтому можно оставить как есть.
    has_state_order = models.CharField("Наличие государственного заказа", max_length=50, blank=True)

    start_grade = models.CharField("С какого класса ведется обучение", max_length=50, blank=True)
    education_duration = models.CharField("Продолжительность обучения", max_length=50, blank=True)
    afterschool_groups_count = models.PositiveIntegerField("Количество групп продленного дня", null=True, blank=True)

    cont_1_11_total = models.PositiveIntegerField("Контингент 1-11/13 кл.", null=True, blank=True)

    cont_1_4_total = models.PositiveIntegerField("Контингент 1-4 кл.", null=True, blank=True)
    cont_1_4_shift1 = models.PositiveIntegerField("1-4: в 1 смену", null=True, blank=True)
    cont_1_4_fulltime = models.PositiveIntegerField("1-4: очно обучаются", null=True, blank=True)
    cont_1_4_external = models.PositiveIntegerField("1-4: экстернат", null=True, blank=True)
    cont_1_4_distance = models.PositiveIntegerField("1-4: дистанционно", null=True, blank=True)
    cont_1_4_oop = models.PositiveIntegerField("1-4: с ООП (с перв.нар)", null=True, blank=True)
    cont_1_4_home = models.PositiveIntegerField("1-4: обучаются на дому", null=True, blank=True)
    cont_1_4_evening = models.PositiveIntegerField("1-4: вечерний класс", null=True, blank=True)

    cont_5_9_total = models.PositiveIntegerField("Контингент 5-9 кл.", null=True, blank=True)
    cont_5_9_shift1 = models.PositiveIntegerField("5-9: в 1 смену", null=True, blank=True)
    cont_5_9_fulltime = models.PositiveIntegerField("5-9: очно обучаются", null=True, blank=True)
    cont_5_9_external = models.PositiveIntegerField("5-9: экстернат", null=True, blank=True)
    cont_5_9_distance = models.PositiveIntegerField("5-9: дистанционно", null=True, blank=True)
    cont_5_9_oop = models.PositiveIntegerField("5-9: с ООП (с перв.нар)", null=True, blank=True)
    cont_5_9_home = models.PositiveIntegerField("5-9: обучаются на дому", null=True, blank=True)
    cont_5_9_evening = models.PositiveIntegerField("5-9: вечерний класс", null=True, blank=True)

    cont_10_11_total = models.PositiveIntegerField("Контингент 10-11/13 кл.", null=True, blank=True)
    cont_10_11_shift1 = models.PositiveIntegerField("10-11/13: в 1 смену", null=True, blank=True)
    cont_10_11_fulltime = models.PositiveIntegerField("10-11/13: очно обучаются", null=True, blank=True)
    cont_10_11_external = models.PositiveIntegerField("10-11/13: экстернат", null=True, blank=True)
    cont_10_11_distance = models.PositiveIntegerField("10-11/13: дистанционно", null=True, blank=True)
    cont_10_11_oop = models.PositiveIntegerField("10-11/13: с ООП (с перв.нар)", null=True, blank=True)
    cont_10_11_home = models.PositiveIntegerField("10-11/13: обучаются на дому", null=True, blank=True)
    cont_10_11_evening = models.PositiveIntegerField("10-11/13: вечерний класс", null=True, blank=True)

    classrooms_count = models.PositiveIntegerField("Количество кабинетов", null=True, blank=True)

    is_private = models.BooleanField("Частная школа", default=False)

    class Meta:
        verbose_name = "Организация образования"
        verbose_name_plural = "Организации образования"

    def __str__(self):
        return self.name


class InspectionType(models.Model):
    code = models.CharField("Код вида", max_length=50, unique=True)
    name = models.CharField("Наименование вида проверки", max_length=255)
    description = models.TextField("Описание", blank=True)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Вид проверки"
        verbose_name_plural = "Виды проверок"

    def __str__(self):
        return self.name


class CriterionCategory(models.Model):
    inspection_type = models.ForeignKey(
        InspectionType,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Вид проверки",
    )
    name = models.CharField("Раздел/блок", max_length=255)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Раздел критериев"
        verbose_name_plural = "Разделы критериев"
        ordering = ["inspection_type", "order", "id"]

    def __str__(self):
        return f"{self.inspection_type} – {self.name}"


class Criterion(models.Model):
    """
    Критерии + подкритерии (как в Excel):
    - объединённые шапки = parent=None (группа)
    - подколонки = parent=<группа>, excel_col заполнен
    """
    class ValueType(models.TextChoices):
        BOOLEAN = "bool", "Да/Нет"
        INTEGER = "int", "Целое число"
        DECIMAL = "decimal", "Число с точкой"
        TEXT = "text", "Текст"
        DATE = "date", "Дата"

    category = models.ForeignKey(
        CriterionCategory,
        on_delete=models.CASCADE,
        related_name="criterias",
        verbose_name="Раздел",
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родительский критерий",
    )

    code = models.CharField("Код критерия", max_length=80, blank=True)
    name = models.CharField("Формулировка критерия", max_length=500)

    value_type = models.CharField(
        "Тип значения",
        max_length=10,
        choices=ValueType.choices,
        default=ValueType.BOOLEAN,
    )

    max_score = models.DecimalField("Максимальный балл", max_digits=6, decimal_places=2, null=True, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)

    excel_col = models.PositiveIntegerField("Колонка Excel (1..39)", null=True, blank=True)

    class Meta:
        verbose_name = "Критерий"
        verbose_name_plural = "Критерии"
        ordering = ["category", "parent_id", "order", "id"]
        unique_together = ("category", "code")

    def clean(self):
        if self.parent and self.parent.category_id != self.category_id:
            raise ValidationError("Подкритерий должен быть в том же разделе, что и родитель.")

    def __str__(self):
        return f"{self.code or ''} {self.name}".strip()

    @property
    def is_leaf(self) -> bool:
        return not self.children.exists()


class Inspection(models.Model):
    STATUS_CHOICES = [
        ("draft", "Черновик"),
        ("in_progress", "В процессе"),
        ("completed", "Завершён ДОКСО"),
        ("approved", "Утверждён центром"),
    ]

    inspection_type = models.ForeignKey(
        InspectionType,
        on_delete=models.PROTECT,
        related_name="inspections",
        verbose_name="Вид проверки",
    )
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name="inspections",
        verbose_name="Школа",
    )
    region = models.ForeignKey(Region, on_delete=models.PROTECT, verbose_name="Регион")
    district = models.ForeignKey(District, on_delete=models.PROTECT, verbose_name="Район/город")
    submitted_at = models.DateTimeField("Отправлен в центр (время)", null=True, blank=True)
    approved_at = models.DateTimeField("Утвержден центром (время)", null=True, blank=True)
    year = models.PositiveIntegerField("Год проверки", null=True, blank=True)
    date_visit = models.DateField("Дата выезда", null=True, blank=True)

    inspector = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Инспектор (ДОКСО)",
        null=True,
        blank=True,
    )

    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="draft")

    total_score = models.DecimalField("Итоговый балл", max_digits=8, decimal_places=2, null=True, blank=True)
    comment = models.TextField("Общий комментарий/вывод", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Проверка (акт)"
        verbose_name_plural = "Проверки (акты)"
        ordering = ["-year", "-date_visit", "-created_at"]
        unique_together = ("inspection_type", "school", "year")

    def __str__(self):
        return f"{self.school} – {self.year or ''} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if self.school_id:
            if not self.region_id:
                self.region = self.school.region
            if not self.district_id:
                self.district = self.school.district
        super().save(*args, **kwargs)

    def recalc_total_score(self):
        total = self.results.aggregate(total=Sum("score"))["total"] or 0
        self.total_score = total
        self.save(update_fields=["total_score"])


class InspectionResult(models.Model):
    inspection = models.ForeignKey(
        Inspection,
        on_delete=models.CASCADE,
        related_name="results",
        verbose_name="Проверка",
    )
    criterion = models.ForeignKey(
        Criterion,
        on_delete=models.PROTECT,
        related_name="results",
        verbose_name="Критерий",
    )

    value_bool = models.BooleanField("Да/Нет", null=True, blank=True)
    value_int = models.IntegerField("Целое значение", null=True, blank=True)
    value_decimal = models.DecimalField("Числовое значение", max_digits=10, decimal_places=2, null=True, blank=True)
    value_text = models.TextField("Текстовое значение / пояснение", blank=True)
    value_date = models.DateField("Дата", null=True, blank=True)

    score = models.DecimalField("Баллы по критерию", max_digits=8, decimal_places=2, null=True, blank=True)
    has_violation = models.BooleanField("Есть нарушение", default=False)
    violation_comment = models.TextField("Замечания / описание нарушения", blank=True)

    class Meta:
        verbose_name = "Результат по критерию"
        verbose_name_plural = "Результаты по критериям"
        unique_together = ("inspection", "criterion")

    def get_value(self):
        t = self.criterion.value_type
        if t == Criterion.ValueType.BOOLEAN:
            return self.value_bool
        if t == Criterion.ValueType.INTEGER:
            return self.value_int
        if t == Criterion.ValueType.DECIMAL:
            return self.value_decimal
        if t == Criterion.ValueType.DATE:
            return self.value_date
        return self.value_text


class MonitoringUser(models.Model):
    ROLE_CENTER = "center"
    ROLE_INSPECTOR = "inspector"

    ROLE_CHOICES = [
        (ROLE_CENTER, "Республиканский центр"),
        (ROLE_INSPECTOR, "Региональный ДОКСО"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="monitoring_profile",
        verbose_name="Пользователь",
    )
    role = models.CharField("Роль", max_length=20, choices=ROLE_CHOICES, default=ROLE_INSPECTOR)

    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Регион")
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Район/город")

    class Meta:
        verbose_name = "Пользователь мониторинга"
        verbose_name_plural = "Пользователи мониторинга"

    def __str__(self):
        return f"{self.user.username} — {self.get_role_display()}"

    @property
    def is_center(self) -> bool:
        return self.role == self.ROLE_CENTER

    @property
    def is_inspector(self) -> bool:
        return self.role == self.ROLE_INSPECTOR
