

import os

from geopy.geocoders import MapQuest
from osp.institutions.models.institution_lonlat import InstitutionLonlat


def geocode(iid, q):

    """
    Geocode a query, write the lon/lat to Postgres.

    :param int iid: The institution id.
    :param str q: The query for the geocoder.
    """

    coder = MapQuest(os.environ['MAPQUEST_KEY'])

    # Geocode.
    g = coder.geocode(q, timeout=10)

    # Write the coordinate.
    InstitutionLonlat.create(
        institution=iid, lon=g.longitude, lat=g.latitude
    )
