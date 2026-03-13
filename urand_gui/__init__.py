import os
import random
import secrets

import click
import pandas as pd
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory

from urand.config import config as urand_config
from urand.study import Study

from .cli import add_user, create_db, delete_user, list_users
from .config import Config as FlaskConfig
from .models import User, db, login_manager
from .oauth import blueprint

# Allow overriding the config file via environment variable
config_file = os.environ.get("URAND_CONFIG_FILE")
if config_file:
    urand_config.set_file(config_file)

study_name = os.environ.get("URAND_STUDY_NAME", "CHS JCOIN HUB")
study = Study(study_name)

app = Flask(__name__)
app.config.from_object(FlaskConfig)
app.register_blueprint(blueprint, url_prefix="/login")
app.cli.add_command(create_db)
app.cli.add_command(add_user)
app.cli.add_command(list_users)
app.cli.add_command(delete_user)
app.config["SQLALCHEMY_DATABASE_URI"] = urand_config["db"].get()
db.init_app(app)
login_manager.init_app(app)
bootstrap = Bootstrap(app)


BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return study.session


if app.config.get("DEMO_MODE"):

    @app.before_request
    def demo_auto_login():
        """Auto-login as demo user when DEMO_MODE is enabled."""
        from flask_login import current_user

        if current_user.is_authenticated:
            return
        demo_user = User.query.filter_by(username="demo").first()
        if not demo_user:
            demo_user = User()
            demo_user.username = "demo"
            demo_user.email = "demo@example.com"
            demo_user.api_key = secrets.token_hex(32)
            db.session.add(demo_user)
            db.session.commit()
        login_user(demo_user)


@app.cli.command("init-demo")
def init_demo():
    """Seed the demo database with ~25 dummy participants."""
    db.create_all()
    db.session.commit()

    from sqlalchemy.orm.exc import NoResultFound

    from urand_gui.models import Study as FlaskStudy

    try:
        FlaskStudy.query.filter_by(name=study_name).one()
    except NoResultFound:
        flask_study = FlaskStudy()
        flask_study.name = study_name
        db.session.add(flask_study)
        db.session.commit()

    # Ensure demo user exists
    demo_user = User.query.filter_by(username="demo").first()
    if not demo_user:
        demo_user = User()
        demo_user.username = "demo"
        demo_user.email = "demo@example.com"
        demo_user.api_key = secrets.token_hex(32)
        db.session.add(demo_user)
        db.session.commit()

    factors = study.factors
    rng = random.Random(42)
    num_participants = 25

    for i in range(num_participants):
        if study.get_participant(str(i)).shape[0] > 0:
            click.echo(f"Participant {i} already exists, skipping.")
            continue

        row = {"id": str(i), "user": "demo"}
        for factor, levels in factors.items():
            row["f_" + factor] = rng.choice(levels)

        df = pd.DataFrame(row, index=[0])
        study.upload_new_participants(pdf=df)
        participant = study.get_participant(str(i))
        trt = participant["trt"].values[0]
        click.echo(f"Participant {i} randomized to {trt}")

    click.echo(f"Demo seeding complete. {num_participants} participants processed.")
