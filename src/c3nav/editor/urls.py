from django.apps import apps
from django.conf.urls import url

from c3nav.editor.views.account import change_password_view, login_view, logout_view, register_view
from c3nav.editor.views.changes import changeset_detail, changeset_edit
from c3nav.editor.views.edit import edit, graph_edit, level_detail, list_objects, main_index, sourceimage, space_detail
from c3nav.editor.views.users import user_detail


def add_editor_urls(model_name, parent_model_name=None, with_list=True, explicit_edit=False):
    model = apps.get_model('mapdata', model_name)
    model_name_plural = model._meta.default_related_name
    if parent_model_name:
        parent_model = apps.get_model('mapdata', parent_model_name)
        parent_model_name_plural = parent_model._meta.default_related_name
        prefix = (parent_model_name_plural+r'/(?P<'+parent_model_name.lower()+'>c?[0-9]+)/')+model_name_plural
    else:
        prefix = model_name_plural

    name_prefix = 'editor.'+model_name_plural+'.'
    kwargs = {'model': model_name, 'explicit_edit': explicit_edit}
    explicit_edit = r'edit' if explicit_edit else ''

    result = []
    if with_list:
        result.append(url(r'^'+prefix+r'/$', list_objects, name=name_prefix+'list', kwargs=kwargs))
    result.extend([
        url(r'^'+prefix+r'/(?P<pk>c?\d+)/'+explicit_edit+'$', edit, name=name_prefix+'edit', kwargs=kwargs),
        url(r'^'+prefix+r'/create$', edit, name=name_prefix+'create', kwargs=kwargs),
    ])
    return result


urlpatterns = [
    url(r'^$', main_index, name='editor.index'),
    url(r'^levels/(?P<pk>c?[0-9]+)/$', level_detail, name='editor.levels.detail'),
    url(r'^levels/(?P<level>c?[0-9]+)/spaces/(?P<pk>c?[0-9]+)/$', space_detail, name='editor.spaces.detail'),
    url(r'^levels/(?P<on_top_of>c?[0-9]+)/levels_on_top/create$', edit, name='editor.levels_on_top.create',
        kwargs={'model': 'Level'}),
    url(r'^levels/(?P<level>c?[0-9]+)/graph/$', graph_edit, name='editor.levels.graph'),
    url(r'^spaces/(?P<space>c?[0-9]+)/graph/$', graph_edit, name='editor.spaces.graph'),
    url(r'^changesets/(?P<pk>[0-9]+)/$', changeset_detail, name='editor.changesets.detail'),
    url(r'^changesets/(?P<pk>[0-9]+)/edit$', changeset_edit, name='editor.changesets.edit'),
    url(r'^sourceimage/(?P<filename>[^/]+)$', sourceimage, name='editor.sourceimage'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='editor.users.detail'),
    url(r'^login$', login_view, name='editor.login'),
    url(r'^logout$', logout_view, name='editor.logout'),
    url(r'^register$', register_view, name='editor.register'),
    url(r'^change_password$', change_password_view, name='editor.change_password'),
]
urlpatterns.extend(add_editor_urls('Level', with_list=False, explicit_edit=True))
urlpatterns.extend(add_editor_urls('LocationGroupCategory'))
urlpatterns.extend(add_editor_urls('LocationGroup'))
urlpatterns.extend(add_editor_urls('WayType'))
urlpatterns.extend(add_editor_urls('AccessRestriction'))
urlpatterns.extend(add_editor_urls('AccessRestrictionGroup'))
urlpatterns.extend(add_editor_urls('Source'))
urlpatterns.extend(add_editor_urls('Building', 'Level'))
urlpatterns.extend(add_editor_urls('Space', 'Level', explicit_edit=True))
urlpatterns.extend(add_editor_urls('Door', 'Level'))
urlpatterns.extend(add_editor_urls('Hole', 'Space'))
urlpatterns.extend(add_editor_urls('Area', 'Space'))
urlpatterns.extend(add_editor_urls('Stair', 'Space'))
urlpatterns.extend(add_editor_urls('Ramp', 'Space'))
urlpatterns.extend(add_editor_urls('Obstacle', 'Space'))
urlpatterns.extend(add_editor_urls('LineObstacle', 'Space'))
urlpatterns.extend(add_editor_urls('Column', 'Space'))
urlpatterns.extend(add_editor_urls('POI', 'Space'))
urlpatterns.extend(add_editor_urls('AltitudeMarker', 'Space'))
urlpatterns.extend(add_editor_urls('LeaveDescription', 'Space'))
urlpatterns.extend(add_editor_urls('CrossDescription', 'Space'))
urlpatterns.extend(add_editor_urls('WifiMeasurement', 'Space'))
