from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from geoalchemy2.shape import from_shape
from shapely import wkt
from database import SessionLocal, engine, Base
import models, schemas

app = FastAPI()

# Create tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Dependency
async def get_db():
    async with SessionLocal() as session:
        yield session

# Point APIs
@app.post("/points/", response_model=schemas.PointOut)
async def create_point(point: schemas.PointCreate, db: AsyncSession = Depends(get_db)):
    geom_obj = from_shape(wkt.loads(point.geom), srid=4326)
    db_point = models.SpatialPoint(name=point.name, description=point.description, geom=geom_obj)
    db.add(db_point)
    await db.commit()
    await db.refresh(db_point)
    return db_point

@app.get("/points/", response_model=list[schemas.PointOut])
async def get_points(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.SpatialPoint))
    return result.scalars().all()

# Polygon APIs
@app.post("/polygons/", response_model=schemas.PolygonOut)
async def create_polygon(poly: schemas.PolygonCreate, db: AsyncSession = Depends(get_db)):
    geom_obj = from_shape(wkt.loads(poly.geom), srid=4326)
    db_poly = models.SpatialPolygon(name=poly.name, description=poly.description, geom=geom_obj)
    db.add(db_poly)
    await db.commit()
    await db.refresh(db_poly)
    return db_poly

@app.get("/polygons/", response_model=list[schemas.PolygonOut])
async def get_polygons(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.SpatialPolygon))
    return result.scalars().all()
