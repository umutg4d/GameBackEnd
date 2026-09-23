"""Schemas for badge API requests."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


NonEmptyString = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        strict=True,
    ),
]

PositiveInteger = Annotated[
    int,
    Field(gt=0, strict=True),
]


class UpdateUserBadgeRequest(BaseModel):
    """Validated request body for awarding a badge to a user."""

    model_config = ConfigDict(extra="forbid")

    user_id: NonEmptyString = Field(alias="userId")
    badge_id: PositiveInteger = Field(alias="badgeId")
