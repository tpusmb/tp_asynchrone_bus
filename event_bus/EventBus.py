from threading import Lock, Thread, Semaphore


class EventBus(Thread):
    singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls.singleton:
            cls.singleton = object.__new__(EventBus)
        return cls.singleton

    def __init__(self):
        Thread.__init__(self)

        self.topicsListeners = {}
        self.events2Process = []
        self.events2ProcessCS = Semaphore(1)

        self.alive = True
        self.newEvent = Lock()
        self.setName("EventBus")
        self.start()

    @staticmethod
    def getInstance():
        if not EventBus.singleton:
            EventBus()
        return EventBus.singleton

    def register(self, listener, topic="default"):
        if topic in self.topicsListeners.keys():
            self.topicsListeners[topic].append(listener)
        else:
            self.topicsListeners[topic] = [listener]

    def post(self, event):
        if event.getTopic() in self.topicsListeners.keys():
            # lock SC
            self.events2ProcessCS.acquire()
            self.events2Process.append(event)
            self.events2ProcessCS.release()
            # unlock SC
            try:
                self.newEvent.release()
            except:
                None

    def run(self):
        while self.alive:
            self.newEvent.acquire()
            # lock SC
            self.events2ProcessCS.acquire()
            toProcess = self.events2Process[:]
            self.events2Process = []
            self.events2ProcessCS.release()
            # unlock SC
            for event in toProcess:
                for listener in self.topicsListeners[event.getTopic()]:
                    listener.process(event)

        print(self.getName() + " stopped")

    def stop(self):
        self.alive = False
        try:
            self.newEvent.release()
        except:
            None
        self.join()
