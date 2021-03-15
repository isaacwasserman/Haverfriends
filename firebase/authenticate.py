from .firebaseInit import auth
from .firebaseFunctions import getUser
from .firebaseFunctions import addUser

def authenticate(sessionCookie):
    if sessionCookie is None:
        print("sessionCookie is None")
        return {"redirect": "/login"}
    else:
        try:
            decoded_claims = auth.verify_session_cookie(sessionCookie, check_revoked=True)
            print(decoded_claims)
            if getUser(decoded_claims["user_id"]) is None:
                userInfo = {
                    "name": decoded_claims["name"],
                    "uid": decoded_claims["user_id"],
                    "email": decoded_claims["email"]
                }
                addUser(userInfo)
                decoded_claims = auth.verify_session_cookie(sessionCookie, check_revoked=True)
                return {"redirect": "/create-profile", "uid": decoded_claims["user_id"]}
            elif len(getUser(decoded_claims["user_id"])["guide_qns"]) == 0:
                print(getUser(decoded_claims["user_id"])["guide_qns"])
                return {"redirect": "/create-profile", "uid": decoded_claims["user_id"]}
            else:
                return decoded_claims
        except auth.InvalidSessionCookieError:
            # Session cookie is invalid, expired or revoked. Force user to login.
            print("sessionCookie is invalid")
            return {"redirect": "/login"}
