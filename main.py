import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from sentry import SentryClient, AuthenticationException, GenericException

logger = logging.getLogger(__name__)

class SentryExtension(Extension):

    def __init__(self):
        logger.info('init Sentry Extension')
        super(SentryExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        # TODO find a way to get preferences here.
        self.sentryClient = SentryClient("", logger)

    def buildResultsList(self, projects):
        items = []
        for project in projects:
            url = "%s/%s/%s" % (self.sentryClient.SENTRY_URL, project['organization']
                                    ['slug'], project['slug'])
            items.append(ExtensionResultItem(icon='images/icon.png',
                                                 name=project["name"],
                                                 description=project['organization']['name'],
                                                 on_enter=OpenUrlAction(
                                                     url)
                                                ))
        return items

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
   
        try:
            extension.sentryClient.setAuthToken(extension.preferences['auth_token'])
            projects = extension.sentryClient.getProjects(event.get_argument())

            items = extension.buildResultsList(projects)

        except AuthenticationException as e:
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name="Authentication failed",
                                             description="Please check the 'auth token' value on extension preferences",
                                             on_enter=HideWindowAction()
                                             ))
        except GenericException as e:
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name="Error fetching information from Sentry",
                                             on_enter=HideWindowAction()
                                             ))
        return RenderResultListAction(items)

if __name__ == '__main__':
   SentryExtension().run()
