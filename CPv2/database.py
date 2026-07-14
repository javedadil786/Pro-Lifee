import json
import os

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class CareerSave(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    save_name = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
    )

    player_data = db.Column(
        db.Text,
        nullable=False,
    )

    def set_player(self, player):
        self.player_data = json.dumps(player)

    def get_player(self):
        return json.loads(self.player_data)


def configure_database(app):
    database_url = os.environ.get(
        "DATABASE_URL",
        "sqlite:///career_path.db",
    )

    # Some older PostgreSQL URLs use postgres://.
    # SQLAlchemy expects postgresql://.
    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1,
        )

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        database_url
    )

    app.config[
        "SQLALCHEMY_TRACK_MODIFICATIONS"
    ] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()