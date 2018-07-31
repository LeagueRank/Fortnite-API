from exceptions import Exception


class UsernameNotFound(Exception):
    def __init__(self, http_error):
        self.http_error = http_error
        super(UsernameNotFound, self).__init__()
