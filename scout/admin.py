# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from flask.ext.login import current_user
from flask.ext.admin import AdminIndexView, expose
from flask.ext.admin.contrib.mongoengine import ModelView


class AuthMixin(object):
  """All admin views should subclass AuthMixin."""
  def is_accessible(self):
    """Check if the current user should have access to the view."""
    return current_user.is_authenticated() and current_user.has_role('admin')


class AdminView(AuthMixin, AdminIndexView):
  @expose('/')
  def index(self):
    """Expose the index view of the admin section of the site."""
    return self.render('admin/index.html')


# customized admin views
class UserView(ModelView):
  """Slightly customized admin view for the user model."""
  column_filters = ['name', 'email', 'created_at', 'location']

  column_searchable_list = ('name', 'email')
