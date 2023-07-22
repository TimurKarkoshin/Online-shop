from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """Продукт"""

    class Meta:
        verbose_name = _("продукт")
        verbose_name_plural = _("продукты")

    name = models.CharField(max_length=512, verbose_name=_("наименование"))
    details = models.ManyToManyField("Detail", through="ProductDetail", verbose_name=_("характеристики"))

    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"


class Detail(models.Model):
    """Свойство продукта"""

    class Meta:
        verbose_name = _("свойство")
        verbose_name_plural = _("свойства")

    name = models.CharField(max_length=512, verbose_name=_("наименование"))

    def __str__(self) -> str:
        return f"Detail(pk={self.pk}, name={self.name!r})"


class ProductDetail(models.Model):
    """Значение свойства продукта"""

    class Meta:
        verbose_name = _("свойство продукта")
        verbose_name_plural = _("свойство продукта")

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    detail = models.ForeignKey(Detail, on_delete=models.PROTECT)
    value = models.CharField(max_length=128, verbose_name=_("значение"))
