"""HTTP API blueprints."""

from app.api.badges import badges_blueprint
from app.api.categories import categories_blueprint
from app.api.catventure import catventure_blueprint
from app.api.daily_levels import daily_levels_blueprint
from app.api.health import health_blueprint
from app.api.missions import missions_blueprint
from app.api.progression import progression_blueprint
from app.api.statistics import statistics_blueprint
from app.api.tournaments import tournaments_blueprint
from app.api.users import users_blueprint


BLUEPRINTS = (
    health_blueprint,
    users_blueprint,
    categories_blueprint,
    statistics_blueprint,
    missions_blueprint,
    daily_levels_blueprint,
    progression_blueprint,
    catventure_blueprint,
    badges_blueprint,
    tournaments_blueprint,
)
