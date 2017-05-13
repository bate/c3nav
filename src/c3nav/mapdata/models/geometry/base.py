from collections import OrderedDict

from shapely.geometry import Point, mapping

from c3nav.mapdata.models.base import EditorFormMixin
from c3nav.mapdata.utils.json import format_geojson

GEOMETRY_MODELS = OrderedDict()


class GeometryMixin(EditorFormMixin):
    """
    A map feature with a geometry
    """
    geometry = None

    class Meta:
        abstract = True

    def get_geojson_properties(self) -> dict:
        return OrderedDict((
            ('type', self.__class__.__name__.lower()),
            ('id', self.id),
        ))

    def to_geojson(self) -> dict:
        return OrderedDict((
            ('type', 'Feature'),
            ('properties', self.get_geojson_properties()),
            ('geometry', format_geojson(mapping(self.geometry), round=False)),
        ))

    @classmethod
    def serialize_type(cls, geomtype=True, **kwargs):
        result = super().serialize_type()
        if geomtype:
            result['geomtype'] = cls._meta.get_field('geometry').geomtype
        return result

    def serialize(self, geometry=True, **kwargs):
        result = super().serialize(geometry=geometry, **kwargs)
        if geometry:
            result.move_to_end('geometry')
        return result

    def _serialize(self, geometry=True, **kwargs):
        result = super()._serialize(**kwargs)
        if geometry:
            result['geometry'] = format_geojson(mapping(self.geometry), round=False)
        return result

    def get_shadow_geojson(self):
        pass

    def contains(self, x, y) -> bool:
        return self.geometry.contains(Point(x, y))