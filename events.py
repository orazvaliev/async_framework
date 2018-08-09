from time import time, sleep


class TimeEvent:
    def __init__(self, loop, moment, callback):
        self.loop = loop
        self.moment = moment
        self.callback = callback
        loop.new_events.append(self)

    def check(self):
        if time() >= self.moment:
            self.callback(self.moment)
            return True


class AsyncLoop:
    def __init__(self):
        self.events = []
        self.new_events = []

    def process_events(self):
        self.events = [e for e in self.events if not e.check()]
        self.events.extend(self.new_events)
        self.new_events = []

    def run_foreva(self):
        while self.events or self.new_events:
            self.process_events()
            sleep(0.1)


def f1(v):
    print("Callback", v)
    TimeEvent(loop, time() + 1, f1)


def run(gen):
    def _callback(v):
        try:
            ev = gen.send(v)
        except StopIteration as e:
            return
        ev.callback = _callback

    _callback(None)


def my_gen_coroutine(loop):
    print((yield TimeEvent(loop, time() + 1, None)))
    print("QQ")
    print((yield TimeEvent(loop, time() + 2, None)))
    print("QQ")
    print((yield TimeEvent(loop, time() + 3, None)))
    print("QQ")


loop = AsyncLoop()

run(my_gen_coroutine(loop))

loop.run_foreva()

