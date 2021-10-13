from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
import os
# Create your models here.


class Exame(models.Model):
    title = models.CharField(max_length=50)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    exame_pdf = models.FileField(upload_to='main/static/Exame')

    def __str__(self):
        return self.title


    def filename(self):
        return os.path.basename(self.exame_pdf.name)


@receiver(models.signals.post_delete, sender=Exame)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Exame` object is deleted.
    """
    if instance.exame_pdf:
        if os.path.isfile(instance.exame_pdf.path):
            os.remove(instance.exame_pdf.path)

@receiver(models.signals.pre_save, sender=Exame)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Exame` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Exame.objects.get(pk=instance.pk).exame_pdf
    except Exame.DoesNotExist:
        return False

    new_file = instance.exame_pdf
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)