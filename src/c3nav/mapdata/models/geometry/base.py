import math
from collections import OrderedDict

from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from shapely.geometry import LineString, Point, mapping
from shapely.ops import unary_union

from c3nav.mapdata.models.base import SerializableMixin
from c3nav.mapdata.utils.geometry import assert_multilinestring, assert_multipolygon
from c3nav.mapdata.utils.json import format_geojson


class GeometryManager(models.Manager):
    def within(self, minx, miny, maxx, maxy):
        return self.get_queryset().filter(minx__lte=maxx, maxx__gte=minx, miny__lte=maxy, maxy__gte=miny)


class GeometryMixin(SerializableMixin):
    """
    A map feature with a geometry
    """
    geometry = None
    minx = models.DecimalField(_('min x coordinate'), max_digits=6, decimal_places=2, db_index=True)
    miny = models.DecimalField(_('min y coordinate'), max_digits=6, decimal_places=2, db_index=True)
    maxx = models.DecimalField(_('max x coordinate'), max_digits=6, decimal_places=2, db_index=True)
    maxy = models.DecimalField(_('max y coordinate'), max_digits=6, decimal_places=2, db_index=True)
    objects = GeometryManager()

    class Meta:
        abstract = True
        base_manager_name = 'objects'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orig_geometry = None if 'geometry' in self.get_deferred_fields() else self.geometry

    def get_geojson_properties(self, *args, **kwargs) -> dict:
        result = OrderedDict((
            ('type', self.__class__.__name__.lower()),
            ('id', self.pk),
        ))
        if getattr(self, 'bounds', False):
            result['bounds'] = True
        return result

    def to_geojson(self, instance=None) -> dict:
        result = OrderedDict((
            ('type', 'Feature'),
            ('properties', self.get_geojson_properties(instance=instance)),
            ('geometry', format_geojson(mapping(self.geometry), round=False)),
        ))
        original_geometry = getattr(self, 'original_geometry', None)
        if original_geometry:
            result['original_geometry'] = format_geojson(mapping(original_geometry), round=False)
        return result

    @classmethod
    def serialize_type(cls, geomtype=True, **kwargs):
        result = super().serialize_type()
        if geomtype:
            result['geomtype'] = cls._meta.get_field('geometry').geomtype
        return result

    @cached_property
    def point(self):
        c = self.geometry.centroid
        x1, y1, x2, y2 = self.geometry.bounds
        lines = (tuple(assert_multilinestring(LineString(((x1, c.y), (x2, c.y))).intersection(self.geometry))) +
                 tuple(assert_multilinestring(LineString(((c.x, y1), (c.x, y2))).intersection(self.geometry))))
        return min(lines, key=lambda line: (line.distance(c), line.length),
                   default=self.geometry.representative_point).centroid

    def serialize(self, **kwargs):
        result = super().serialize(**kwargs)
        if 'geometry' in result:
            result.move_to_end('geometry')
        return result

    def _serialize(self, geometry=True, simple_geometry=False, **kwargs):
        result = super()._serialize(simple_geometry=simple_geometry, **kwargs)
        if geometry:
            result['geometry'] = format_geojson(mapping(self.geometry), round=False)
        if simple_geometry:
            result['point'] = (self.level_id, ) + tuple(round(i, 2) for i in self.point.coords[0])
            if not isinstance(self.geometry, Point):
                result['bounds'] = ((int(math.floor(self.minx)), int(math.floor(self.miny))),
                                    (int(math.ceil(self.maxx)), int(math.ceil(self.maxy))))
        return result

    def details_display(self):
        result = super().details_display()
        result['geometry'] = format_geojson(mapping(self.geometry), round=False)
        return result

    def get_shadow_geojson(self):
        pass

    def contains(self, x, y) -> bool:
        return self.geometry.contains(Point(x, y))

    def recalculate_bounds(self):
        self.minx, self.miny, self.maxx, self.maxy = self.geometry.bounds

    @property
    def geometry_changed(self):
        if self.orig_geometry is None:
            return True
        if self.geometry is self.orig_geometry:
            return False
        if not self.geometry.almost_equals(self.orig_geometry, 1):
            return True
        field = self._meta.get_field('geometry')
        rounded = field.to_python(field.get_prep_value(self.geometry))
        if not rounded.almost_equals(self.orig_geometry, 2):
            return True
        return False

    def get_changed_geometry(self):
        if self.orig_geometry is None:
            return self.geometry
        difference = self.geometry.symmetric_difference(self.orig_geometry)
        if self._meta.get_field('geomety').geomtype in ('polygon', 'multipolygon'):
            difference = unary_union(assert_multipolygon(difference))
        return difference

    def save(self, *args, **kwargs):
        self.recalculate_bounds()
        super().save(*args, **kwargs)
