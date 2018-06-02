import requests
from cache import Cache

class SentryClient:

    SENTRY_URL = "https://sentry.io"

    API_BASE_URL = "https://sentry.io/api/0"

    CACHE_TTL = 3600 # 1h

    CACHE_KEY = "sentry_projects"

    def __init__(self, authToken, logger):
        self.authToken = authToken
        self.logger = logger

    def setAuthToken(self, authToken):
        self.logger.debug("Setting access token to " + authToken)
        self.authToken = authToken

    def filterResults(self, projects, filter=None):

        if not filter:
            return projects

        filteredProjects = []
        for project in projects:
            if filter.lower() in project['name'].lower():
                filteredProjects.append(project)

        return filteredProjects
    
    def getProjects(self, filter=None):
        self.logger.debug("getting projects from sentry")

        if Cache.get(self.CACHE_KEY):
            self.logger.debug("Loading from cache")
            return self.filterResults(Cache.get(self.CACHE_KEY), filter)

        headers = {"Authorization": "Bearer {}".format(self.authToken)}
        r = requests.get(self.API_BASE_URL + '/projects/', headers=headers)

        if not r.ok:
            if r.status_code == 401:
                raise AuthenticationException(
                    "Failed to authenticate with access token " + self.authToken)

            raise GenericException(
                "Error connecting to Sentry API : status " + r.status_code)

        data = r.json()

        Cache.set(self.CACHE_KEY, data, self.CACHE_TTL)

        return self.filterResults(data, filter)

class GenericException(Exception):
      pass 

class AuthenticationException(Exception):
    pass
