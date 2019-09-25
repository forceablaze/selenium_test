from urllib.parse import urlparse
from urllib.parse import urljoin

# https://www.somed002.sony.co.jp/ccm/web/projects/OlySandBox#action=com.ibm.team.workitem.viewWorkItem&id=<id>

Actions = {
    # com.ibm.team.workitem.viewWorkItem&id=<id>
    'VIEW_WORKITEM': 'com.ibm.team.workitem.viewWorkItem',

    # com.ibm.team.workitem.viewQueries
    'VIEW_QUERIES': 'com.ibm.item.workitem.viewQueries'
}

Tabs = {
    'WORKITEM_TAB_LINKS': 'com.ibm.team.workitem.tab.links',
}

class URLBuilder():

    def __init__(self, hostUrl = 'https://www.somed002.sony.co.jp/ccm/web'):
        self.hostUrl = hostUrl

    def getProjectUrl(self, projectName):
        return '{}/projects/{}'.format(self.hostUrl, projectName)

    def getProjectWorkItemUrl(self, projectName, workItemId, tab = ''):
        actionUrl = self.getUrl(projectName, 'VIEW_WORKITEM')

        return '{}&id={}&tab={}'.format(actionUrl, workItemId, tab)

    def getUrl(self, projectName, action = None):

        if action is None:
            return '{}/projects/{}'.format(self.hostUrl, projectName)

        if action in Actions:
            return '{}/projects/{}#action={}'.format(
                self.hostUrl, projectName, Actions[action])

        raise Exception('No action found.')
