class MySecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Strict-Transport-Security"] = "max-age=31536000"
        return response
