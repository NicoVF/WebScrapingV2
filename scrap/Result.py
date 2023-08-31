

class Result:
    def __init__(self):
        self.errors = []

    def add_error(self, error):
        self.errors.append(error)

    def errors_as_string(self):
        return ', '.join(self.errors)

    def has_errors(self):
        return len(self.errors) > 0
