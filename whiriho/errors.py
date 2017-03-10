

class WhirihoException(Exception):
    """
    Abstract Whiriho exception.
    """
    pass

class CatalogNotFoundException(WhirihoException):
    """
    Exception raised when catalog file could not be found.
    """
    pass

class CatalogFormatException(WhirihoException):
    """
    Exception raised when catalog file is not well formatted.
    """
    pass

class CatalogVersionException(WhirihoException):
    """
    Exception raised when catalog version is not well formatted or not known.
    """
    pass

class CatalogPathException(WhirihoException):
    """
    Exception raised when catalog path could not be found.
    """
    pass

class ConfigurationUriException(WhirihoException):
    """
    Exception raised when Whiriho could not parse configuration URI.
    """
    pass

class ConfigurationException(WhirihoException):
    """
    Exception raised when Whiriho could not read configuration file.
    """
    pass


class ConfigurationSchemaException(WhirihoException):
    """
    Exception raised when Whiriho could not read or parse configuration schema.
    """
    pass

class CatalogInitializationException(WhirihoException):
    """
    Exception raised when Whiriho could not initialize the catalog.
    """
    pass
