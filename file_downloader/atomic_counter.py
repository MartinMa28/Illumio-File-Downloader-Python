from multiprocessing import Value, Lock


class AtomicCounter:
    def __init__(self, initial=0):
        self.val = Value('i', initial)
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    def increment_by_value(self, val):
        with self.lock:
            self.val.value += val

    def get_value(self):
        return self.val.value
