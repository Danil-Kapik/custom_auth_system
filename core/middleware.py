from core.container import get_session_repository, get_user_repository


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.session_repository = get_session_repository()
        self.user_repository = get_user_repository()

    def __call__(self, request):
        request.user = None

        token = self._extract_token(request)
        if token:
            session = self.session_repository.get_by_token(token)
            if session:
                request.user = self.user_repository.get_by_id(session.user_id)

        return self.get_response(request)

    def _extract_token(self, request):
        authorization = request.META.get("HTTP_AUTHORIZATION", "")
        if isinstance(authorization, str) and authorization.startswith(
            "Bearer "
        ):
            return authorization.split(" ", 1)[1].strip()
        return None
