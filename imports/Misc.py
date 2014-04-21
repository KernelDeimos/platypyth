class RefVar:
    def __init__(self,val):
        self.var = val
    def __call__(self):
        return self.var

class InfiniteList: # USELESS CLASS
    # Problem: can't use list() on one of these...
    # it would sort've throw us in an infinite loop :/
    def __init__(self,items=False):
        if isinstance(items,tuple):
            self.items = list(items)
        else:
            self.items = items or []
        self.current = 0
    def __getitem__(self,key):
        if key >= len(self.items):
            return 0
        else:
            return self.items[key]
    def __setitem__(self,key,val):
        while key >= len(self.items):
            self.items.append(0)
        self.items[key] = val
    def __iter__(self):
        return self
    def __len__(self):
        return len(self.items)
    def append(self,val):
        self.items.append(val)
    def next(self):
        try:
            retval = self.items[self.current]
        except IndexError:
            raise StopIteration
        self.current += 1
        return retval

def getSign(val):
    if val > 0:
        return True
    else:
        return False