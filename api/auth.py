from allauth.headless.internal import token_util
from allauth.headless.tokens.base import TokenStrategy
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class AllauthJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Extract Authorization Header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            # Format: "Bearer <token>"
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != "bearer":
                return None
            
            token_string = parts[1]
            
            # Fetch the configured strategy via allauth utils
            strategy = token_util.get_token_strategy()
            
            # Lookup active session context from the JWT token string
            session = strategy.lookup_session(token_string)
            if not session or not session.user.is_active:
                raise AuthenticationFailed("Invalid or expired JWT token.")
                
            return (session.user, token_string)

        except Exception as e:
            raise AuthenticationFailed(str(e))
