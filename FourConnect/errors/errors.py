class Error(Exception):
    pass

class ColumnError(Error):

    def __init__ (self, *args):

        self.message = args[0] if args else None

    def __str__(self):
        if self.message:
            return 'ColumnError, {}'.format(self.message)
        else:
            return 'ColumnError'

class BoardError(Error):

    def __init__ (self, *args):

        self.message = args[0] if args else None

    def __str__(self):
        if self.message:
            return 'BoardError, {}'.format(self.message)
        else:
            return 'BoardError'

