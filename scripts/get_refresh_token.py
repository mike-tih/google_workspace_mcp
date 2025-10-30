#!/usr/bin/env python3
"""
Script to obtain a Google OAuth refresh token with specific scopes.

Usage:
    python get_refresh_token.py

Requirements:
    pip install google-auth-oauthlib google-auth-httplib2

Before running:
    Set environment variables:
    - GOOGLE_CLIENT_ID
    - GOOGLE_CLIENT_SECRET
"""

import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes needed for Gmail and Calendar
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    # Gmail
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels",
    # Calendar
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events",
]


def main():
    """Get refresh token with specified scopes."""
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("Error: GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set")
        sys.exit(1)

    # Create client config
    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost:8080/"],
        }
    }

    print("=" * 70)
    print("Google OAuth Refresh Token Generator")
    print("=" * 70)
    print(f"\nRequesting the following scopes:")
    for scope in SCOPES:
        print(f"  - {scope}")
    print()

    # Run OAuth flow
    flow = InstalledAppFlow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri="http://localhost:8080/"
    )

    print("Opening browser for authorization...")
    print("If browser doesn't open, copy the URL from console and open manually.")
    print()

    # This will start a local server and open browser
    credentials = flow.run_local_server(
        port=8080,
        prompt="consent",  # Force consent screen to show all scopes
        success_message="Authorization successful! You can close this window.",
    )

    print("\n" + "=" * 70)
    print("SUCCESS!")
    print("=" * 70)
    print(f"\nRefresh Token:\n{credentials.refresh_token}")
    print(f"\nAccess Token:\n{credentials.token}")
    print(f"\nScopes granted:")
    for scope in credentials.scopes:
        print(f"  - {scope}")

    print("\n" + "=" * 70)
    print("Next steps:")
    print("=" * 70)
    print("1. Copy the refresh token above")
    print("2. Set it as TMP_REFRESH_TOKEN environment variable")
    print("3. Update your code to use it")
    print()


if __name__ == "__main__":
    main()
