# -*- coding: utf-8 -*-

import anyconfig
import jsonschema
import semantic_version

from . import __version__
from .schemas import (
    __whiriho_catalog__,
    __whiriho_catalog_v1__
)
from .errors import (
    CatalogNotFoundException,
    CatalogFormatException,
    CatalogVersionException
)

class Whiriho(object):
    """
    Configuration catalog object.
    """

    def __init__(self, path, format=None):
        """
        Initialize a Whiriho catalog.

        Arguments:
        path -- File path.
        format -- File formatting (optional).
        """
        self.path = path
        self.forced_format = format
        self.version = None
        self.catalog = None

    @staticmethod
    def parse_version(version):
        """
        Parse given version using semantic_version library.

        Arguments:
        version -- Version string.
        """
        try:
            return semantic_version.Version(version)
        except ValueError as error:
            raise CatalogVersionException(error.message)

    def load(self):
        """
        Load Whiriho catalog.
        """
        try:
            # Open and parse catalog (in forced format or by analyzing file extension)
            data = anyconfig.load(self.path, ac_parser=self.forced_format)

            # Validate generic catalog version. We only accept version 1.x.x
            jsonschema.validate(data, __whiriho_catalog__)

            # Analyze catalog version.
            self.version = Whiriho.parse_version(data['version'])

            # Parse catalog in version 1
            if self.version.major == 1:
                jsonschema.validate(data, __whiriho_catalog_v1__)
                self.catalog = data['catalog']
            else:
                raise CatalogVersionException(
                    'Whiriho (%s) cannot use catalog version %s' % (
                        __version__,
                        self.version
                    )
                )
        except jsonschema.ValidationError as error:
            raise CatalogFormatException('Invalid catalog format: %s' % error.message)
        except jsonschema.SchemaError:
            raise AssertionError('Internal library error; invalid schema')
        except IOError:
            raise CatalogNotFoundException('Failed to load configuration catalog')

    def get_paths(self):
        """
        Return the list of catalog paths.
        """
        return self.catalog.keys()

    def __enter__(self):
        """
        Method called when you are using 'with' statement.
        It will automatically load Whiriho catalog.
        """
        self.load()

    def __exit__(self, type, value, traceback):
        """
        Method called when you are using 'with' statement.
        """
        pass
