

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
