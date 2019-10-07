class Event:
    def __init__(self, data, topic="default"):
        self.data = data
        self.topic = topic
        self.counter = 0

    def get_data(self):
        return self.data

    def get_topic(self):
        return self.topic
