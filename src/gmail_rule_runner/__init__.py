import json
import os

from .Action import Action
from .Condition import Condition
from .Rule import Rule
from .auth import set_token, get_token

credentials_path = ""
secrets_path = ""
rules_file = ""


def execute_all_rules(service):
    """
The execute_all_rules function is the main function of this script.
It reads in the rules file, and for each rule it finds, it creates a Rule object with that rule's name and JSON data.
Then, it executes that Rule object.

:param service: Pass in the service object for the api call
:return: The number of rules that were executed
:doc-author: prabhakarant
"""
    if os.path.exists(rules_file):
        with open(rules_file, 'rb') as json_file:
            rules_json = json.load(json_file)
        for rule_name, rule in rules_json.items():
            rule_obj = Rule(rule, rule_name, service)
            rule_obj.execute()
