import json
import jwt
from account.models import Account
from django.conf import settings

class JSONTokenAuthentication:

    
    
    def authenticate(request):

        USER_SETTINGS = getattr(settings, "JWT_AUTH", None)

        JWT_SECRET_KEY = USER_SETTINGS["JWT_SECRET_KEY"]
        JWT_ALGORITHM = USER_SETTINGS["JWT_ALGORITHM"]

        auth = request.META.get("HTTP_AUTHORIZATION")
        

        if auth != None:
            encoded_token = auth.split(" ")[1]

            decoded_token = jwt.decode(
                encoded_token, JWT_SECRET_KEY, algorithm="HS256")

            if Account.objects.filter(userid=decoded_token['userid']).exists():
                return True
            else:
                return False
        else:
            return False