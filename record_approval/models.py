from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class RecordToBeApproved(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    activity_type = models.CharField(max_length=20, choices=(('created', 'created'), ('changed', 'changed')))
    activity_user = models.ForeignKey(User, on_delete=models.PROTECT)

    created_date_time = models.DateTimeField(auto_now_add=True)
    last_changed_date_time = models.DateTimeField("last changed", auto_now=True, null=True)

    class Meta:
        verbose_name = 'record to be approved'
        verbose_name_plural = 'records to be approved'
    
