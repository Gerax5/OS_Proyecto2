class Recurso:
    def __init__(self, name, count):
        self.name = name
        self.count = count
        self.in_use = 0

    def try_access(self):
        raise NotImplementedError

    def release(self):
        if self.in_use > 0:
            self.in_use -= 1

class Mutex(Recurso):
    def try_access(self):
        if self.in_use == 0:
            self.in_use = 1
            return True
        return False

class Semaforo(Recurso):
    def try_access(self):
        if self.in_use < self.count:
            self.in_use += 1
            return True
        return False