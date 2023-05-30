class Condition:
    predicate = None
    field = None
    value = None

    def __init__(self, condition_json):
        self.predicate = condition_json['predicate']
        self.field = condition_json['field']
        self.value = condition_json['value']

    def __str__(self):
        return self.field + " " + self.predicate + " " + self.value
