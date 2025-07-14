from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from database import Base

class SpatialPoint(Base):
    __tablename__ = "spatial_points"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    geom = Column(Geometry(geometry_type='POINT', srid=4326))

class SpatialPolygon(Base):
    __tablename__ = "spatial_polygons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    geom = Column(Geometry(geometry_type='POLYGON', srid=4326))
