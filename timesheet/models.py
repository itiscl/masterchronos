import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, validate_unicode_slug
from django.db import models


class Employee(User, models.Model):
    """
    Класс описывает сотрудника.
    """
    number = models.CharField(
        max_length=10,
        verbose_name='Табельный номер',
        validators=[validate_unicode_slug],
        unique=True
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.last_name} {self.first_name} ({self.number})'


class ActivityType(models.Model):
    """
    Класс описывает вид деятельности сотрудника.
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование'
    )

    class Meta:
        verbose_name = 'Активность'
        verbose_name_plural = 'Активности'

    def __str__(self):
        return self.name


class TimeSheet(models.Model):
    """
    Класс описывает табель сотрудника.
    """
    DRAFT = "DRAFT"
    FILLED = "FILLED"
    APPROVED = "APPROVED"

    STATUS_CHOICES = [
        (DRAFT, "Черновик"),
        (FILLED, "Оформлен"),
        (APPROVED, "Утвержден"),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT
    )

    month = models.DateField(
        verbose_name='Месяц'
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    class Meta:
        verbose_name = 'Табель'
        verbose_name_plural = 'Табели'
        ordering = ['month']

    def get_total(self):
        return int(self.timesheetentry_set.aggregate(total=models.aggregates.Sum("quantity"))["total"] or 0)

    def save(self, *args, **kwargs):
        self.month = datetime.date(self.month.year, self.month.month, 1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Табель {self.employee.number} за {self.month.year}-{self.month.month:02d}'


class TimeSheetEntry(models.Model):
    """
    Класс описывает запись в табеле сотрудника.
    """
    timesheet = models.ForeignKey(
        TimeSheet,
        on_delete=models.CASCADE,
        verbose_name='Табель',
    )

    date = models.DateField(
        verbose_name='Дата'
    )

    activity = models.ForeignKey(
        ActivityType,
        on_delete=models.CASCADE,
        verbose_name='Активность'
    )

    quantity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(24)
        ],
        verbose_name='Кол-во часов'
    )

    comment = models.TextField(
        verbose_name='Комментарий'
    )

    class Meta:
        verbose_name = 'Запись в табеле'
        verbose_name_plural = 'Записи в табеле'
        ordering = ['date']

    def __str__(self):
        return f'Запись в табеле {self.timesheet.employee.number} за {self.date.strftime("%d.%m.%Y")}'
