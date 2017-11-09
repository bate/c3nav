from itertools import chain
from operator import attrgetter

from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from shapely.ops import cascaded_union

from c3nav.mapdata.models.locations import SpecificLocation


class LevelManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).defer('render_data')


class Level(SpecificLocation, models.Model):
    """
    A map level
    """
    base_altitude = models.DecimalField(_('base altitude'), null=False, unique=True, max_digits=6, decimal_places=2)
    default_height = models.DecimalField(_('default space height'), max_digits=6, decimal_places=2, default=3.0)
    on_top_of = models.ForeignKey('mapdata.Level', null=True, on_delete=models.CASCADE,
                                  related_name='levels_on_top', verbose_name=_('on top of'))
    short_label = models.SlugField(max_length=20, verbose_name=_('short label'), unique=True)

    render_data = models.BinaryField(null=True)

    objects = LevelManager()

    class Meta:
        verbose_name = _('Level')
        verbose_name_plural = _('Levels')
        default_related_name = 'levels'
        ordering = ['base_altitude']
        base_manager_name = 'objects'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def lower(self, level_model=None):
        if self.on_top_of_id is not None:
            raise TypeError
        if level_model is None:
            level_model = Level
        return level_model.objects.filter(base_altitude__lt=self.base_altitude,
                                          on_top_of__isnull=True).order_by('-base_altitude')

    def higher(self, level_model=None):
        if self.on_top_of_id is not None:
            raise TypeError
        if level_model is None:
            level_model = Level
        return level_model.objects.filter(base_altitude__gt=self.base_altitude,
                                          on_top_of__isnull=True).order_by('base_altitude')

    @property
    def sublevels(self):
        if self.on_top_of is not None:
            raise TypeError
        return chain((self, ), self.levels_on_top.all())

    @property
    def sublevel_title(self):
        return '-' if self.on_top_of_id is None else self.title

    @property
    def primary_level(self):
        return self if self.on_top_of_id is None else self.on_top_of

    @property
    def primary_level_pk(self):
        return self.pk if self.on_top_of_id is None else self.on_top_of_id

    def _serialize(self, level=True, **kwargs):
        result = super()._serialize(**kwargs)
        result['short_label'] = self.short_label
        result['on_top_of'] = self.on_top_of_id
        result['base_altitude'] = float(str(self.base_altitude))
        result['default_height'] = float(str(self.default_height))
        return result

    def details_display(self):
        result = super().details_display()
        result['display'].insert(3, (str(_('short label')), self.short_label))
        result['display'].extend([
            (str(_('outside only')), self.base_altitude),
            (str(_('default height')), self.default_height),
        ])
        result['editor_url'] = reverse('editor.levels.detail', kwargs={'pk': self.pk})
        return result

    @cached_property
    def min_altitude(self):
        return min(self.altitudeareas.all(), key=attrgetter('altitude'), default=self.base_altitude).altitude

    @cached_property
    def bounds(self):
        return cascaded_union(tuple(item.geometry.buffer(0)
                                    for item in chain(self.altitudeareas.all(), self.buildings.all()))).bounds
