"""
External OAuth Provider for Google Workspace MCP

Extends FastMCP's GoogleProvider to support external OAuth flows where
access tokens (ya29.*) are issued by external systems and need validation.
"""
import logging
import time
from typing import Optional

from fastmcp.server.auth.providers.google import GoogleProvider
from fastmcp.server.auth import AccessToken
from google.oauth2.credentials import Credentials

logger = logging.getLogger(__name__)


class ExternalOAuthProvider(GoogleProvider):
    """
    Extended GoogleProvider that supports validating external Google OAuth access tokens.

    This provider handles ya29.* access tokens by calling Google's userinfo API,
    while maintaining compatibility with standard JWT ID tokens.

    IMPORTANT: This provider DISABLES protocol-level authentication for initialize/tools/list.
    Authentication is only required for actual tool calls (tools/call).
    """

    def __init__(self, client_id: str, client_secret: str, **kwargs):
        """Initialize and store client credentials for token validation."""
        super().__init__(client_id=client_id, client_secret=client_secret, **kwargs)
        # Store credentials as they're not exposed by parent class
        self._client_id = client_id
        self._client_secret = client_secret

    async def verify_token(self, token: str) -> Optional[AccessToken]:
        """
        Verify a token - supports both JWT ID tokens and ya29.* access tokens.

        For ya29.* access tokens (issued externally), validates by calling
        Google's userinfo API. For JWT tokens, delegates to parent class.

        Args:
            token: Token string to verify (JWT or ya29.* access token)

        Returns:
            AccessToken object if valid, None otherwise
        """
        # For ya29.* access tokens, validate using Google's userinfo API
        if token.startswith("ya29."):
            logger.debug("Validating external Google OAuth access token")

            try:
                from auth.google_auth import get_user_info

                # Create minimal Credentials object for userinfo API call
                credentials = Credentials(
                    token=token,
                    token_uri="https://oauth2.googleapis.com/token",
                    client_id=self._client_id,
                    client_secret=self._client_secret
                )

                # Validate token by calling userinfo API
                user_info = get_user_info(credentials)

                if user_info and user_info.get("email"):
                    # Token is valid - create proper AccessToken object for FastMCP
                    logger.info(f"Validated external access token for: {user_info['email']}")

                    # Create a proper AccessToken object that FastMCP can use for session management
                    # Default expiry: 1 hour from now (standard for Google access tokens)
                    expires_at = int(time.time()) + 3600

                    user_email = user_info["email"]
                    user_sub = user_info.get("id", user_email)

                    access_token = AccessToken(
                        token=token,
                        scopes=[],  # Scopes not available from ya29.* access tokens
                        expires_at=expires_at,
                        claims={"email": user_email, "sub": user_sub},
                    )

                    # Set additional attributes for compatibility with middleware
                    access_token.email = user_email
                    access_token.sub = user_sub
                    access_token.client_id = self._client_id

                    return access_token
                else:
                    logger.error("Could not get user info from access token")
                    return None

            except Exception as e:
                logger.error(f"Error validating external access token: {e}")
                return None

        # For JWT tokens, use parent class implementation
        return await super().verify_token(token)