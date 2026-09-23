"""Application database models."""

from app.models.badges import Badge, UserBadge
from app.models.categories import Category, CategoryImage, UserCategory, UserCategoryImage
from app.models.catventure import CatventureLevel, CatventureLevelProgress, CatventureSection
from app.models.daily_levels import DailyLevelCompletion, DailyLevelRewardClaimed
from app.models.missions import UserMission
from app.models.progression import Section, UserProgress
from app.models.statistics import UserDailyStatistics
from app.models.tournaments import TournamentPlayer
from app.models.users import User


__all__ = (
    "Badge",
    "Category",
    "CategoryImage",
    "CatventureLevel",
    "CatventureLevelProgress",
    "CatventureSection",
    "DailyLevelCompletion",
    "DailyLevelRewardClaimed",
    "Section",
    "TournamentPlayer",
    "User",
    "UserBadge",
    "UserCategory",
    "UserCategoryImage",
    "UserDailyStatistics",
    "UserMission",
    "UserProgress",
)
