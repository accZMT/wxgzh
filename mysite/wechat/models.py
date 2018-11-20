from django.db import models

# Create your models here.


class MaterialModel(models.Model):
    media_type = models.CharField(max_length=20, null=False, verbose_name="媒体文件类型")
    title = models.CharField(max_length=40, null=False, verbose_name="素材标题")
    introduction = models.CharField(max_length=100, null=False, verbose_name="素材简介")
    media_id = models.CharField(max_length=200, null=False, verbose_name="素材id")

    class Meta:
        db_table = "material"
