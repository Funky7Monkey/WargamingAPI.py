class APIException(Exception):
	"""Base class for excpetions for WargamingAPI.py"""
	pass

class HTTPException(APIException):
	"""Raised when an HTTP request operation fails.
	
	Attributes:
		response -- The response of the failed HTTP request. This is a dictionary.
		field -- The field from which the error originated. The specified value is found in this field. Can be None.
		message -- The error message returned by the API.
		code -- The error code.
		value -- The data that caused the error. Found in the specified field of the request. Can be None.
		request -- The request that caused the error. This is a dictionary.
	"""

	def __init__(self, response, field, message, code, value, request):
		self.response = response
		self.field    = field
		self.message  = message
		self.code     = code
		self.value    = value
		self.request  = request