import logging
import requests
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

logger = logging.getLogger(__name__)

SENTRY_URL = "https://sentry.io"
API_ENDPOINT = "https://sentry.io/api/0"

class HashExtension(Extension):

    def __init__(self):
        logger.info('init sentry Extension')
        super(HashExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
   
        authToken = extension.preferences['auth_token']

        headers = {"Authorization": "Bearer {}".format(authToken)}
        r = requests.get('https://sentry.io/api/0/projects/', headers=headers)

        if not r.ok:
            if r.status_code == 401:
                items.append(ExtensionResultItem(icon='images/icon.png',
                                                  name="401 - Unauthorized",
                                                  description="Please check Extension settings and confirm your 'auth_token' is correct",
                                                  highlightable=False,
                                                  on_enter=HideWindowAction()))
            
            else:
                items.append(ExtensionResultItem(icon='images/icon.png',
                                                  name="Unexpected Error " + r.status_code,
                                                  highlightable=False,
                                                  on_enter=HideWindowAction()))
            return RenderResultListAction(items)
                
        projects = r.json()

        for project in projects:
            url = "%s/%s/%s" % (SENTRY_URL, project['organization']
                                ['slug'], project['slug'])
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=project["name"],
                                             description=project['organization']['name'],
                                             on_enter=OpenUrlAction(
                                                 url)
                                             ))

        return RenderResultListAction(items)

if __name__ == '__main__':
   HashExtension().run()
