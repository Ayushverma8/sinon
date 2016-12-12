properties = ["SinonSpy", "SinonStub", "SinonMock"]
production_properties = ["spy", "stub", "mock"]

def _clear_item_in_queue(queue):
    for item in reversed(queue):
        item.restore()


def sinontest(f):
    def fn(*args, **kwargs):
        ret = f(*args, **kwargs)
        # handle production mode (called by sinon.py)
        for prop in production_properties:
            if "sinon" in f.__globals__ and prop in dir(f.__globals__["sinon"]):
                _clear_item_in_queue(getattr(f.__globals__["sinon"], prop)._queue)
        # handle unittest (direct use)
        for prop in properties:
            if prop in f.__globals__.keys():
                _clear_item_in_queue(f.__globals__[prop]._queue)
        return ret
    return fn


class SinonSandbox(object):

    def __init__(self):
        pass

    def create(self, config=None):
        pass

    def spy(self):
        pass

    def stub(self):
        pass

    def mock(self):
        pass

    def restore(self):
        pass