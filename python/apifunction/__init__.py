import logging
import os

import azure.functions as func
from sqlalchemy.orm import sessionmaker

from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        with SessionLocal() as db:
            new_word = models.WordIndex(word="maupa")
            db.add(new_word)
            db.commit()
            nasze_dziedzictwo = db.query(models.WordIndex)
        return func.HttpResponse(
            f"Hello from Python, {name}! Indeks: {str(nasze_dziedzictwo)}"
        )
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
