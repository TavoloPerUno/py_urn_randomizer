import os

import pandas as pd

from urand import Study, db
from urand.config import config

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
STUDY_NAME = "CHS JCOIN"

# Point confuse at the test config.yaml
config.set_file(os.path.join(os.path.dirname(__file__), "config.yaml"))


def test_upload_with_seed():
    study = Study(STUDY_NAME, memory=True)
    df_file = pd.read_csv(os.path.join(DATA_DIR, "test_asgmts_with_seed.csv"))
    study.upload_existing_history(
        file=os.path.join(DATA_DIR, "test_asgmts_with_seed.csv")
    )
    df_participants = db.get_participants(study.participant, study.session)
    assert (
        df_participants.shape[0] == df_file.shape[0]
    ), "Uploading file with seed unsuccessful"


def test_upload_without_seed():
    study = Study(STUDY_NAME, memory=True)
    df_file = pd.read_csv(os.path.join(DATA_DIR, "test_asgmts_without_seed.csv"))
    study.upload_existing_history(
        file=os.path.join(DATA_DIR, "test_asgmts_without_seed.csv")
    )
    df_participants = db.get_participants(study.participant, study.session)
    assert (
        df_participants.shape[0] == df_file.shape[0]
    ), "Uploading file without seed unsuccessful"
