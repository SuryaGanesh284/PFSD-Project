from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    name = 'core'

    # Neo4j support has been removed; no additional initialization required
