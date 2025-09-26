import os, uuid, datetime
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import select, text
from models import Base, Player

DATABASE_URL = os.getenv("DATABASE_URL")
WEBAPP_ORIGIN = os.getenv("WEBAPP_ORIGIN", "*")

engine: Optional[AsyncEngine] = create_async_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionFactory: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

def iso_week_anchor(dt: datetime.date) -> str:
    y, w, _ = dt.isocalendar()
    return f"{y}-W{w:02d}"

app = FastAPI(title="ButonTap API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[WEBAPP_ORIGIN, "*"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with SessionFactory() as s:
        yield s

@app.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    await db.execute(text("SELECT 1"))
    return {"ok": True}

class PlayerOut(BaseModel):
    id: str
    telegram_user_id: int | None
    username: str | None
    coins: int
    diamonds: int
    xp: int
    weekly_taps: int
    class Config: from_attributes = True

class MeIn(BaseModel):
    telegram_id: int
    username: str | None = None

class ProgressIn(BaseModel):
    telegram_id: int
    delta_coins: int = 0
    delta_diamonds: int = 0
    delta_xp: int = 0
    add_taps: int = 0

@app.post("/players/me", response_model=PlayerOut)
async def players_me(body: MeIn, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Player).where(Player.telegram_user_id == body.telegram_id))
    player = res.scalar_one_or_none()
    if not player:
        player = Player(
            id=str(uuid.uuid4()),
            telegram_user_id=body.telegram_id,
            username=body.username,
            coins=0, diamonds=0, xp=0,
            weekly_taps=0,
            week_anchor=iso_week_anchor(datetime.date.today()),
        )
        db.add(player); await db.commit(); await db.refresh(player)
    else:
        if body.username and body.username != player.username:
            player.username = body.username
            await db.commit(); await db.refresh(player)
    return player

@app.post("/progress/update", response_model=PlayerOut)
async def progress_update(body: ProgressIn, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Player).where(Player.telegram_user_id == body.telegram_id))
    player = res.scalar_one_or_none()
    if not player: raise HTTPException(404, "Player not found")
    today_anchor = iso_week_anchor(datetime.date.today())
    if player.week_anchor != today_anchor:
        player.week_anchor = today_anchor
        player.weekly_taps = 0
    player.coins = max(0, player.coins + body.delta_coins)
    player.diamonds = max(0, player.diamonds + body.delta_diamonds)
    player.xp = max(0, player.xp + body.delta_xp)
    if body.add_taps: player.weekly_taps = max(0, player.weekly_taps + body.add_taps)
    await db.commit(); await db.refresh(player); return player

@app.get("/leaderboard/weekly", response_model=List[PlayerOut])
async def leaderboard_weekly(limit: int = Query(10, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    anchor = iso_week_anchor(datetime.date.today())
    res = await db.execute(select(Player).where(Player.week_anchor == anchor).order_by(Player.weekly_taps.desc()).limit(limit))
    return list(res.scalars())
