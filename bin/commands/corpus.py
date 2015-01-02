

import os
import click

from osp.common.models.base import postgres
from osp.common.overview import Overview
from osp.corpus.models.document import Document
from osp.corpus.corpus import Corpus
from collections import Counter
from prettytable import PrettyTable


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    postgres.connect()
    postgres.create_tables([Document])


@cli.command()
def insert_documents():

    """
    Insert documents in the database.
    """

    for s in Corpus.from_env().cli_syllabi():
        try:
            with postgres.transaction():
                Document.create(path=s.relative_path)
        except: pass


@cli.command()
def pull_overview_ids():

    """
    Copy document ids from Overview.
    """

    id = os.environ['OSP_DOC_SET_ID']
    ov = Overview.from_env()

    for o_doc in ov.stream_documents(id):

        query = (
            Document
            .update(stored_id=o_doc['id'])
            .where(Document.path==o_doc['title'])
        )

        query.execute()


@cli.command()
def file_count():

    """
    Print the total number of files.
    """

    corpus = Corpus.from_env()
    click.echo(corpus.file_count)
