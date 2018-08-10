from time import time, sleep


def start_gen(f):
    def wrap(*args, **kwargs):
        gen = f(*args, **kwargs)
        gen.send(None)
        return gen
    return wrap


class TimeEvent:
    def __init__(self, loop, moment, callback):
        self.loop = loop
        self.moment = moment
        self.callback = callback

    def check_event(self):
        if time() >= self.moment:
            self.callback()
            return True
        else:
            return False


class AsyncLoop:
    def __init__(self):
        self.events: [TimeEvent] = []

    def process_events(self):
        self.events = [e for e in self.events if not e.check_event()]

    def run_loop(self):
        while self.events:
            self.process_events()
            sleep(0.1)

@start_gen
def run(gen):
    try:
        event = gen.send

