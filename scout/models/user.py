# -*- coding: utf-8 -*-
"""

"main concept of MongoDB is embed whenever possible"
Ref: http://stackoverflow.com/questions/4655610#comment5129510_4656431
"""
from __future__ import absolute_import, unicode_literals
from datetime import datetime

from mongoengine import (DateTimeField, Document, EmailField, ListField,
                         ReferenceField, StringField)


class User(Document):
  """Represent a Scout user that can belong to multiple instututes."""
  email = EmailField(required=True, unique=True)
  name = StringField(max_length=40, required=True)
  created_at = DateTimeField(default=datetime.now)
  accessed_at = DateTimeField()
  location = StringField()
  institutes = ListField(ReferenceField('Institute'))
  roles = ListField(StringField())

  # Flask-Login integration
  def is_authenticated(self):
    """Perform a faux check that the user if properly authenticated."""
    return True

  def is_active(self):
    """Perform a faux check that the user is active."""
    return True

  def is_anonymous(self):
    """Perform a faux check whether the user is anonymous."""
    return False

  def get_id(self):
    # the id property is assigned each model automatically
    return str(self.id)

  def has_role(self, query_role):
    """Check if user has been assigned a specific role."""
    return query_role in self.roles

  def belongs_to(self, institute_id):
    """Check if user belongs to a specific institute."""
    return institute_id in self.institutes

  @property
  def first_name(self):
    """Return the first name of the user."""
    return self.name.split(' ')[0]

  # required for Flask-Admin interface
  def __unicode__(self):
    return self.name
