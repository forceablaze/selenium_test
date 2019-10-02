
class WorkItem:

    def __init__(self, header, row):
        self._header = header
        self._row = row

    def getType(self):
        return self.get('タイプ')

    def getId(self):
        return self.get('ID')

    def getTitle(self):
        return self.get('要約')

    def getOwner(self):
        return self.get('所有者')

    def getStatus(self):
        return self.get('状況')

    def getRow(self):
        return self._row

    def get(self, title):
        index = self._header.index(title)

        return self._row[index]

    def isClosed(self):
        return self.getStatus() == 'Closed'
