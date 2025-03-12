from django.db import models
from django.utils import timezone

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', '未完成'),
        ('completed', '已完成'),
        ('overdue', '已逾期'),
    ]

    name = models.CharField(max_length=255, verbose_name="任务名称")
    source = models.CharField(max_length=255, verbose_name="任务来源")
    description = models.TextField(blank=True, verbose_name="任务描述")
    deadline = models.DateTimeField(verbose_name="截止时间")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="状态"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def save(self, *args, **kwargs):
        if self.status != 'completed' and self.deadline < timezone.now():
            self.status = 'overdue'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name