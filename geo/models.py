from django.db import models

class Region(models.Model):
    name = models.CharField("Регион", max_length=100, unique=True)

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"

    def __str__(self):
        return self.name


class District(models.Model):
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="districts",
        verbose_name="Регион",
    )
    name = models.CharField("Район/город", max_length=100)

    class Meta:
        verbose_name = "Район/город"
        verbose_name_plural = "Районы/города"
        unique_together = ("region", "name")

    def __str__(self):
        return f"{self.region} – {self.name}"
