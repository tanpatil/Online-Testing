from src.flask.api.controllers.implementations.binary_search import binary_search as bs

def protect(sessions, request):
    # we check if the token exists at first, then we go ahead and we extract the session data
    if 'token' in request.args:
        res = bs(sessions, request.args['token'])
        if res != -1:
            return True
        else:
            return False
    else:
        return False