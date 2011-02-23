from django.db import models
import simplejson as json # you can get this from http://pypi.python.org/pypi/simplejson/
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from djangodashboard.dashboard.gadgets import open_gadget

from django.db.models import CharField
import uuid
from xml_utils import readValueFromXMLField

#------------------------------------------------------------------------------

class UUIDVersionError(Exception):
    pass

class UUIDField(CharField):
    """ UUIDField
    By default uses UUID version 1 (generate from host ID, sequence number and current time)
    The field support all uuid versions which are natively supported by the uuid python module.
    For more information see: http://docs.python.org/lib/module-uuid.html
    More Info
    http://en.wikipedia.org/wiki/Universally_unique_identifier
    """

    def __init__(self, verbose_name=None, name=None, auto=True, version=1, node=None, clock_seq=None, namespace=None, **kwargs):
        kwargs['max_length'] = 36
        if auto:
            kwargs['blank'] = True
            kwargs.setdefault('editable', False)
        self.auto = auto
        self.version = version
        if version==1:
            self.node, self.clock_seq = node, clock_seq
        elif version==3 or version==5:
            self.namespace, self.name = namespace, name
        CharField.__init__(self, verbose_name, name, **kwargs)

    def get_internal_type(self):
        return CharField.__name__

    def create_uuid(self):
        if not self.version or self.version==4:
            return uuid.uuid4()
        elif self.version==1:
            return uuid.uuid1(self.node, self.clock_seq)
        elif self.version==2:
            raise UUIDVersionError("UUID version 2 is not supported.")
        elif self.version==3:
            return uuid.uuid3(self.namespace, self.name)
        elif self.version==5:
            return uuid.uuid5(self.namespace, self.name)
        else:
            raise UUIDVersionError("UUID version %s is not valid." % self.version)

    def pre_save(self, model_instance, add):
        if self.auto and add:
            value = unicode(self.create_uuid()).upper()
            setattr(model_instance, self.attname, value)
            return value
        else:
            value = super(UUIDField, self).pre_save(model_instance, add)
            if self.auto and not value:
                value = unicode(self.create_uuid()).upper()
                setattr(model_instance, self.attname, value)
        return value

#------------------------------------------------------------------------------

class Dashboard(models.Model):
    uuid = UUIDField(primary_key=True)
    name = models.TextField(null=True, blank=False)
    user = models.ForeignKey(User,null=True, blank=True)

    def __unicode__(self):
        return self.name
    class Meta :
        unique_together = (('name', 'user'),)
        db_table = 'dashboard'

#------------------------------------------------------------------------------

class DashboardItem(models.Model):
    uuid = UUIDField(primary_key=True)
    dashboard = models.ForeignKey(Dashboard, db_column='dashboard_uuid')
    gadget = models.TextField()
    column_number = models.IntegerField()
    position = models.IntegerField()
    colour = models.TextField(null=True, blank=False)
    title = models.TextField(null=True, blank=False)
    collapsed = models.BooleanField()
    modifier = models.TextField(null=True, blank=False)
    active = models.BooleanField()
    
    class Meta:
        db_table = 'dashboard_item'
        
    def get_colour(self):
        if self.colour != None:
            return self.colour
        try:
            return open_gadget(self.gadget).gadget_info()['colour']
        except:
            return ""

    def get_icon(self):
        try:
            return open_gadget(self.gadget).gadget_info()['icon']
        except:
            return ""

    def get_extra_fields(self):
        try:
            fields = open_gadget(self.gadget).gadget_info()['fields']
        except:
            return ""
        newFields={}
        for field in fields:
            value = readValueFromXMLField(field['id'],self.modifier)
            if value != '':
                field['value'] = value
            newFields[field['id']] = value
        return newFields

    def get_extra_fields_json(self):
        try:
            fields = open_gadget(self.gadget).gadget_info()['fields']
        except:
            return []
        newFields=[]
        for field in fields:
            value = readValueFromXMLField(field['id'],self.modifier)
            if value != '':
                field['value'] = value
            newFields.append(field)
        return mark_safe(json.JSONEncoder().encode(newFields))
    
    def get_collapsed_style(self):
        if self.collapsed:
            return ' collapsed'
        else:
            return ''
    
    def make_html_id(self):
        id = "id" + self.uuid.replace('-','')
        return id
