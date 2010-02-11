try:
    set
except NameError:
    from sets import Set as set

try:
    reversed
except NameError:
    def reversed(sequence):
        new = list(sequence)
        new.reverse()
        return new

try:
    sorted
except NameError:
    def sorted(sequence):
        new = list(sequence)
        new.sort()
        return new

try:
    enumerate
except NameError:
    def enumerate(iterable):
        i = 0
        for entry in iterable:
            yield i, entry
