

import os
import click
import csv

from osp.common.models.base import database
from osp.locations.models.doc_to_inst import DocToInst
from osp.locations.jobs.locate import locate
from osp.institutions.models.institution import Institution
from osp.institutions.models.lonlat import LonLat
from osp.corpus.corpus import Corpus
from rq import Queue
from redis import StrictRedis
from peewee import *


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    database.connect()
    database.create_tables([DocToInst])


@cli.command()
def queue_location():

    """
    Queue institution matching tasks in the worker.
    """

    # TODO: ENV-ify.
    queue = Queue(connection=StrictRedis())
    corpus = Corpus(os.environ['OSP_CORPUS'])

    for syllabus in corpus.syllabi():
        queue.enqueue(locate, syllabus.path)


@cli.command()
@click.argument('out_path', type=click.Path())
def make_csv(out_path):

    """
    DEV: Generate a CSV file.

    :param in_file: A path for the new CSV file.
    """

    out_file = open(out_path, 'w')

    # CSV writer:
    cols = ['document', 'longitude', 'latitude']
    writer = csv.DictWriter(out_file, cols)

    # Get current doc->inst links.
    current = DocToInst.select_current()

    rows = []
    for doc in current.naive().iterator():

        lonlat = (
            doc.institution.lonlats
            .order_by(LonLat.created.desc())
            .first()
        )

        rows.append({
            'document': doc.document,
            'latitude': lonlat.lat,
            'longitude': lonlat.lon
        })

    writer.writeheader()
    writer.writerows(rows)
