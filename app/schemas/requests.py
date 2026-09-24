"""Pydantic schemas for the application's existing HTTP request contracts."""

from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StrictBool, model_validator


MYSQL_INTEGER_MAX = 2_147_483_647

NonEmptyString = Annotated[str, Field(min_length=1, max_length=36)]
PositiveInteger = Annotated[int, Field(gt=0, le=MYSQL_INTEGER_MAX)]
NonNegativeInteger = Annotated[int, Field(ge=0, le=MYSQL_INTEGER_MAX)]
StrictNonNegativeInteger = Annotated[
    int,
    Field(ge=0, le=MYSQL_INTEGER_MAX, strict=True),
]


class RequestSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class GetUserRequest(RequestSchema):
    idfv: Annotated[str, Field(min_length=1, max_length=50)]
    stat_date: date


class CreateUserRequest(GetUserRequest):
    pass


class UpdateUserRequest(RequestSchema):
    user_id: NonEmptyString
    vip_status: Literal["True", "False"]
    no_ads_status: Literal["True", "False"]
    soft_currency: NonNegativeInteger
    hint_count: NonNegativeInteger
    match_count: NonNegativeInteger


class CamelCaseUserRequest(RequestSchema):
    user_id: NonEmptyString = Field(alias="userId")


class SnakeCaseUserRequest(RequestSchema):
    user_id: NonEmptyString


class OpenCategoryRequest(SnakeCaseUserRequest):
    category_id: PositiveInteger


class CompleteImageRequest(SnakeCaseUserRequest):
    image_id: PositiveInteger


StatisticName = Literal[
    "session_count",
    "puzzle_count",
    "pieces_connected",
    "daily_gift",
    "tarot_offer",
    "impossible_offer",
    "daily_mission",
    "catventure",
    "spin_wheel",
    "spin_count",
    "multiplayer",
    "multiplayer_win",
    "daily_level_completed",
]


class GetDailyStatisticsRequest(SnakeCaseUserRequest):
    stat_date: date


class UpdateDailyStatisticsRequest(GetDailyStatisticsRequest):
    stat_name: StatisticName
    delta_count: PositiveInteger


class GetClaimedMissionsRequest(SnakeCaseUserRequest):
    current_date: date


class ClaimMissionRequest(GetClaimedMissionsRequest):
    mission_id: PositiveInteger
    step: NonNegativeInteger


class CompleteDailyLevelRequest(SnakeCaseUserRequest):
    day: Annotated[int, Field(ge=1, le=31)]
    month: Annotated[int, Field(ge=1, le=12)]
    year: PositiveInteger

    @model_validator(mode="after")
    def validate_calendar_date(self):
        date(self.year, self.month, self.day)
        return self


class ClaimDailyLevelRewardRequest(SnakeCaseUserRequest):
    milestone: PositiveInteger
    month: Annotated[int, Field(ge=1, le=12)]
    year: PositiveInteger


class UpdateUserProgressRequest(SnakeCaseUserRequest):
    section_id: PositiveInteger
    current_xp: NonNegativeInteger
    completed_status: Literal["True", "False"]


class UpdateCatventureProgressRequest(SnakeCaseUserRequest):
    current_section_id: PositiveInteger
    current_level_id: PositiveInteger


class CreateTournamentRequest(SnakeCaseUserRequest):
    seed: NonNegativeInteger


class UpdateTournamentRequest(RequestSchema):
    tournament_id: NonEmptyString = Field(alias="tournamentId")
    user_id: NonEmptyString = Field(alias="userId")
    points: StrictNonNegativeInteger | None = None
    matches_played: StrictNonNegativeInteger | None = Field(
        default=None,
        alias="matchesPlayed",
    )
    final_rank: StrictNonNegativeInteger | None = Field(
        default=None,
        alias="finalRank",
    )
    prize_presented: StrictBool | None = Field(
        default=None,
        alias="prizePresented",
    )

    @model_validator(mode="after")
    def require_an_update(self):
        update_fields = (
            self.points,
            self.matches_played,
            self.final_rank,
            self.prize_presented,
        )
        if all(value is None for value in update_fields):
            raise ValueError("at least one tournament field must be provided")
        return self
