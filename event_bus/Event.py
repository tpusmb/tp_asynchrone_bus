class Event:
    def __init__(self, data, topic="default"):
        self.data=data
        self.topic=topic

    def getData(self):
        return self.data

    def getTopic(self):
        return self.topic
