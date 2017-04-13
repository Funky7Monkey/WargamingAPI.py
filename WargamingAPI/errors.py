"""
The MIT License (MIT)

Copyright (c) 2017 Funky7Monkey

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

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