class ErrorMessage:
	INVALID_CREDENTIALS = {'code': 1000, 'message': "Invalid Login Credentials."}
	INTERNAL_SERVER_ERROR = {'code': 1001, 'message': "The server could not process the request."}
	VALIDATION_ERROR = {'code': 1002, 'message': "Validation Failed"}
	MISSING_PARAMETERS = {'code': 1003, 'message': "Missing required parameter."}
	INVALID_PARAMETERS = {'code': 1004, 'message': "Invalid Parameters"}
	UNAUTHORIZED_ACCESS = {'code': 1005, 'message': "UnAuthorized Access"}