class NoDataError(Exception):
    """
    Exception to handle cases where API doesn't provide data
    """
    pass

class InvalidParameterError(Exception):
    """
    Exception to handle invalid parameters for API call
    """
    pass
