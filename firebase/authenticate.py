from .firebaseInit import auth

def getUser(sessionCookie):
    if sessionCookie is None:
        return None
    else:
        try:
            decoded_claims = auth.verify_session_cookie(sessionCookie, check_revoked=True)
            return decoded_claims
        except auth.InvalidSessionCookieError:
            # Session cookie is invalid, expired or revoked. Force user to login.
            return None