# -*- coding: utf-8 -*-

import os
import anyconfig
import json
import jsonschema
import semantic_version
import urlparse

from . import __version__
from .schemas import (
    __whiriho_catalog__,
    __whiriho_catalog_v1__
)
from .errors import (
    CatalogNotFoundException,
    CatalogFormatException,
    CatalogVersionException,
    CatalogPathException,
    ConfigurationException,
    ConfigurationSchemaException,
    ConfigurationUriException
)

class Whiriho(object):
    """
    Configuration catalog object.
    """

    def __init__(self, path, format=None, allow_absolute=False, allow_unsafe=False):
        """
        Initialize a Whiriho catalog.

        Arguments:
        path -- File path.
        format -- File formatting (optional).
        """
        self.path = path
        self.forced_format = format
        self.allow_absolute = allow_absolute
        self.allow_unsafe = allow_unsafe
        self.version = None
        self.catalog = None

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

    def get_config_raw(self, path):
        """
        Return raw config specs from catalog.
        """
        if path not in self.catalog:
            raise CatalogPathException('Unable to get config path \'%s\'' % path)

        return self.catalog.get(path)

    def get_config_meta(self, path):
        """
        Return config metadata for specified path in catalog.

        Arguments:
        path -- Config path in catalog.

        It returns the following tuple of values:
        uri -- Configuration URI.
        format -- Configuration file format (optional, default=None)
        schema -- Configuration schema URI (optional, default=None)
        """
        raw = self.get_config_raw(path)

        return raw.get('uri'), raw.get('format', None), raw.get('schema', None)

    def get_config_data(self, path):
        """
        Return configuration data from specified path in catalog.
        """
        uri, format, _ = self.get_config_meta(path)
        scheme = Whiriho.parse_scheme(uri)

        if scheme == 'file':
            try:
                return anyconfig.load(
                    self.safe_config_path(urlparse.urlparse(uri).path),
                    ac_parser=format
                )
            except IOError:
                raise ConfigurationException('Failed to read configuration data')
            except anyconfig.backends.UnknownFileTypeError:
                raise ConfigurationException('Unknown configuration format, cannot parse it')
        else:
            raise ConfigurationUriException('Unknown scheme: %s' % scheme)

    def get_config_schema(self, path):
        """
        Return configuration schema from specified path in catalog.
        """
        _, _, schema = self.get_config_meta(path)

        if not schema:
            return None

        scheme = Whiriho.parse_scheme(schema)

        if scheme == 'file':
            try:
                with open(self.safe_config_path(urlparse.urlparse(schema).path), 'r') as file:
                    return json.loads(file.read())
                    # TODO validate schema itself
            except IOError:
                raise ConfigurationSchemaException('Failed to read configuration schema')
        else:
            raise ConfigurationUriException('Unknown scheme: %s' % scheme)

    def safe_config_path(self, path):
        """
        Create safe path from given file path with Whiriho options.
        It's using 'allow_unsafe' and 'absolute_path' to refactor input file.

        Arguments:
        path -- Path of file to review.
        """
        # If file has absolute path that we not authorize, raise an error
        if os.path.isabs(path):
            if not self.allow_absolute or not self.allow_unsafe:
                raise ConfigurationUriException('Not authorized to load absolute file')
        else:
            # TODO double check needed
            orig = path
            dir = os.path.realpath(os.path.dirname(self.path))
            path = os.path.join(dir, path)
            if not os.path.realpath(path).startswith(dir) and not self.allow_unsafe:
                raise ConfigurationUriException('Unsafe path: %s' % orig)

        return path

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

    @staticmethod
    def parse_scheme(uri):
        """
        Parse URI scheme.
        """
        scheme = urlparse.urlparse(uri).scheme
        if not scheme:
            scheme = 'file'

        return scheme

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
