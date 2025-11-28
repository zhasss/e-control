from django.db import models
from django.contrib.auth import get_user_model

from geo.models import Region, District

User = get_user_model()

class School(models.Model):
    """
    Организация образования из ОСО (лист 'Сеть').
    """

    # 1–5: ID, БИН, KATO
    os_id = models.PositiveIntegerField("ID из ОСО", unique=True, null=True, blank=True)
    bin = models.CharField("БИН", max_length=12, blank=True)

    kato_ar = models.CharField("kato_ar", max_length=20, blank=True)
    kato_reg = models.CharField("kato_reg", max_length=20, blank=True)
    kato_np = models.CharField("kato_np", max_length=20, blank=True)

    # 6–8: регион, район, населённый пункт
    region = models.ForeignKey(Region, on_delete=models.PROTECT, verbose_name="Область")
    district = models.ForeignKey(District, on_delete=models.PROTECT, verbose_name="Район")
    locality = models.CharField("Населенный пункт", max_length=255, blank=True)

    # 9–12: названия
    name = models.CharField("Наименование организации (кратко)", max_length=255)
    name_kz = models.CharField("Наименование организации каз", max_length=255, blank=True)
    name_kz_full = models.TextField("Наименование организации каз полное", blank=True)
    name_ru_full = models.TextField("Наименование организации рус полное", blank=True)

    # 13–21: типы/виды, уровни, язык, форма обуч.
    edu_org_type = models.CharField("Тип организации образования", max_length=255, blank=True)
    org_kinds = models.CharField("Виды организации", max_length=255, blank=True)
    ownership_form = models.CharField("Форма собственности", max_length=255, blank=True)
    department = models.CharField("Ведомственная принадлежность", max_length=255, blank=True)
    territory = models.CharField("Территориальная принадлежность", max_length=255, blank=True)
    education_levels = models.CharField("По уровням образования", max_length=255, blank=True)
    founders = models.CharField("Основные учредители", max_length=255, blank=True)
    teaching_language = models.CharField("Язык обучения", max_length=255, blank=True)
    education_form = models.CharField("Форма обучения", max_length=255, blank=True)

    # 22–27: адрес и директор
    legal_address_kz = models.TextField("Адрес юридический на казахском", blank=True)
    legal_address_ru = models.TextField("Адрес юридический на русском", blank=True)

    np_part_type = models.CharField("Тип составной части населенного пункта", max_length=255, blank=True)
    np_part_name = models.CharField("Наименование составной части населенного пункта", max_length=255, blank=True)
    house_number = models.CharField("№ дома", max_length=50, blank=True)

    head_full_name = models.CharField("ФИО руководителя", max_length=255, blank=True)
    acting_head_full_name = models.CharField("ФИО и.о. руководителя", max_length=255, blank=True)
    acting_head_position = models.CharField("Должность и.о. руководителя", max_length=255, blank=True)

    # 30–35: контакты
    phone_work = models.CharField("Рабочий телефон", max_length=100, blank=True)
    phone_mobile = models.CharField("Сотовый телефон", max_length=100, blank=True)
    fax = models.CharField("Факс", max_length=100, blank=True)
    email = models.CharField("E-mail организации образования", max_length=255, blank=True)
    website = models.CharField("Сайт", max_length=255, blank=True)
    postal_index = models.CharField("Почтовый индекс", max_length=20, blank=True)

    # 36–40: неделя, открытие, статус, ОПФ
    study_week = models.CharField("Учебная неделя", max_length=50, blank=True)
    open_date = models.DateField("Дата открытия", null=True, blank=True)
    status = models.CharField("Статус", max_length=255, blank=True)
    location = models.CharField("Расположен", max_length=255, blank=True)
    legal_form = models.CharField("Организационно-правовая форма", max_length=255, blank=True)

    # 41–43: лицензия
    license_authority = models.CharField(
        "Кем выдана лицензия на право образовательной деятельности",
        max_length=255,
        blank=True,
    )
    license_number = models.CharField("Номер лицензии", max_length=100, blank=True)
    license_date = models.DateField("Дата выдачи лицензии", null=True, blank=True)

    # 44–48: комплексы, смены, госзаказ
    complex_school_kindergarten = models.CharField(
        "Комплекс «школа-ясли-сад»",
        max_length=50,
        blank=True,
    )
    complex_special_school_kindergarten = models.CharField(
        "Специальный комплекс «школа-ясли-сад»",
        max_length=50,
        blank=True,
    )
    shifts_count = models.PositiveIntegerField("Количество смен", null=True, blank=True)
    special_classes_count = models.PositiveIntegerField("Количество спец классов", null=True, blank=True)
    has_state_order = models.CharField(
        "Наличие государственного заказа",
        max_length=50,
        blank=True,
    )

    # 49–51: начало и длительность обучения, ГПД
    start_grade = models.CharField("С какого класса ведется обучение", max_length=50, blank=True)
    education_duration = models.CharField("Продолжительность обучения", max_length=50, blank=True)
    afterschool_groups_count = models.PositiveIntegerField(
        "Количество групп продленного дня",
        null=True,
        blank=True,
    )

    # 52–77: контингенты
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
    """
    Вид проверки:
    - Проверка частных школ
    - Проверка гос. школ
    и т.д. (сейчас фактически будет один вид: 'Проверка частных школ').
    """
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
    """
    Раздел критериев (как блоки в твоей таблице: кадры, МТО, безопасность и т.д.)
    Привязан к ВИДУ проверки.
    """
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
    Один критерий (строка/колонка из чек-листа).
    """
    class ValueType(models.TextChoices):
        BOOLEAN = "bool", "Да/Нет"
        INTEGER = "int", "Целое число"
        DECIMAL = "decimal", "Число с точкой"
        TEXT = "text", "Текст"

    category = models.ForeignKey(
        CriterionCategory,
        on_delete=models.CASCADE,
        related_name="criterias",
        verbose_name="Раздел",
    )
    code = models.CharField("Код критерия", max_length=50, blank=True)
    name = models.CharField("Формулировка критерия", max_length=500)
    value_type = models.CharField(
        "Тип значения",
        max_length=10,
        choices=ValueType.choices,
        default=ValueType.BOOLEAN,
    )
    max_score = models.DecimalField(
        "Максимальный балл",
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Критерий"
        verbose_name_plural = "Критерии"
        ordering = ["category", "order", "id"]

    def __str__(self):
        return f"{self.code or ''} {self.name}".strip()


class Inspection(models.Model):
    """
    Конкретная проверка школы ДОКСО (акт).
    Здесь ДОКСО один раз заполняет форму по критериям.
    """
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

    year = models.PositiveIntegerField("Год проверки", null=True, blank=True)
    date_visit = models.DateField("Дата выезда", null=True, blank=True)

    inspector = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Инспектор (ДОКСО)",
        null=True,
        blank=True,
    )
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )

    total_score = models.DecimalField(
        "Итоговый балл",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    comment = models.TextField("Общий комментарий/вывод", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Проверка (акт)"
        verbose_name_plural = "Проверки (акты)"
        ordering = ["-year", "-date_visit", "-created_at"]

    def __str__(self):
        return f"{self.school} – {self.year or ''} ({self.get_status_display()})"


class InspectionResult(models.Model):
    """
    Значение по каждому критерию в рамках одной проверки.
    """
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
    value_decimal = models.DecimalField(
        "Числовое значение",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    value_text = models.TextField("Текстовое значение / пояснение", blank=True)

    score = models.DecimalField(
        "Баллы по критерию",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    has_violation = models.BooleanField("Есть нарушение", default=False)
    violation_comment = models.TextField("Замечания / описание нарушения", blank=True)

    class Meta:
        verbose_name = "Результат по критерию"
        verbose_name_plural = "Результаты по критериям"
        unique_together = ("inspection", "criterion")
