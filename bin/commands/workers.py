

import click
import requests

from osp.common.utils import partitions
from osp.common.inventory import Inventory
from blessings import Terminal


term = Terminal()


@click.group()
def cli():
    pass


@cli.command()
def ping():

    """
    Ping the workers.
    """

    for url in Inventory().worker_urls:

        # Hit /ping.
        r = requests.get(url+'/ping')

        code = r.status_code
        click.echo(url)

        if code == 200:
            click.echo(term.green('pong'))
        else:
            click.echo(term.red(str(code)))


@cli.command()
def status():

    """
    List the number of pending jobs for each worker.
    """

    for url in Inventory().worker_urls:

        # Load rq-dashboard.
        r = requests.get(url+'/rq/queues.json')

        click.echo(url)
        for queue in r.json()['queues']:

            # Pending jobs:
            if queue['name'] == 'default':
                click.echo(term.green(str(queue['count'])))

            # Failed jobs:
            if queue['name'] == 'failed':
                click.echo(term.red(str(queue['count'])))


@cli.command()
def queue_text():

    """
    Queue text extraction.
    """

    urls = Inventory().worker_urls
    pts = partitions(4095, len(urls))

    for i, url in enumerate(urls):

        s1 = pts[i][0]
        s2 = pts[i][1]

        # Post the boundaries.
        r = requests.post(
            url+'/corpus/text',
            params={'s1': s1, 's2': s2 }
        )

        code = r.status_code
        click.echo(url)

        if code == 200:
            click.echo(term.green(str(s1)+'-'+str(s2)))
        else:
            click.echo(term.red(str(code)))
