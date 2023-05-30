class Action:
    type = None
    value = None

    def __init__(self, action_type, value):
        self.type = action_type
        self.value = value

    def __str__(self):
        return self.type
