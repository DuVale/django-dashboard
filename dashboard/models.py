from django.db import models
from django.contrib.auth.models import User

class Dashboard(models.Model):
    name = models.TextField(null=True, blank=False)
    user = models.ForeignKey(User,null=True, blank=True)
    xml = models.TextField()

    def __unicode__(self):
        return self.name
    class Meta :
        unique_together = (('name', 'user'),)


