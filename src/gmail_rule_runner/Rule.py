import json
import os
import traceback
from datetime import datetime

from .Action import Action
from .Condition import Condition


class Rule:
    conditions = []
    actions = []
    filtered_mails = []
    service = None
    rule_name = None
    rule_predicate = None

    def __init__(self, rule_json, rule_name, service):
        self.rule_name = rule_name
        self.service = service
        self.rule_predicate = rule_json['rule_predicate']
        for condition in rule_json['conditions']:
            self.conditions.append(Condition(condition))
        for action_type, value in rule_json['actions'].items():
            self.actions.append(Action(action_type, value))

    def __str__(self):
        return self.rule_name

    def get_response_header_data(self, response, data_type):
        """
    The get_response_header_data function takes in a response and data_type as parameters.
    It then iterates through the headers of the response, looking for a header with the name that matches
    the data_type parameter. If it finds one, it returns its value. Otherwise, it returns None.

    :param self: Represent the instance of the class
    :param response: Store the response from the api
    :param data_type: Specify the type of data that is to be returned
    :return: The value of the header data type
    :doc-author: prabhakarant
    """

        for data in response.get("payload").get("headers"):
            if data['name'] == data_type:
                if data['name'] == 'Date':
                    date = data['value'].split(',')
                    if len(date) > 1:
                        date = date[1].split("+" if "+" in date[1] else "-")[
                            0].strip()  # remove day e.g. Fri,Thu from string if exists
                    else:
                        date = date[0].split("+" if "+" in date[0] else "-")[0].strip()  # remove timezone
                    try:
                        date = datetime.strptime(date[:20],
                                                 '%d %b %Y %H:%M:%S')  # convert final date and time to python datetime
                    except:
                        date = datetime.strptime(date[:20],
                                                 '%d %b %y %H:%M:%S')

                    return date
                return data['value']

    def execute_rule(self, request, response, exception):

        """
    The execute_rule function takes in a request, response and exception.
        The function then checks if the rule predicate is 'all' or 'any'.
        If it is all, it will check if all conditions are met for that particular mail.
        If they are, the mail id will be added to filtered_mails list.

    :param self: Refer to the object itself
    :param request: Get the request data
    :param response: Get the headers of a mail
    :param exception: Check if the response is an exception
    :doc-author: prabhakarant
    """
        if not exception:
            condition_checks = []
            for condition in self.conditions:
                field_data = self.get_response_header_data(response, condition.field)
                if not condition.field == "Date":
                    if condition.predicate == "contains":
                        condition_checks.append(condition.value.lower() in field_data.lower())
                    if condition.predicate == 'equal':
                        condition_checks.append(condition.value.lower() == field_data.lower())
                    if condition.predicate == 'not_equal':
                        condition_checks.append(condition.value.lower() != field_data.lower())
                else:
                    if condition.predicate == "less":
                        condition_checks.append(
                            datetime.strptime(condition.value[:20], "%d-%m-%Y").date() > field_data.date())
                    if condition.predicate == "equal":
                        condition_checks.append(
                            datetime.strptime(condition.value[:20], "%d-%m-%Y").date() == field_data.date())
                    if condition.predicate == "greater":
                        condition_checks.append(
                            datetime.strptime(condition.value[:20], "%d-%m-%Y").date() < field_data.date())
                    if condition.predicate == "between":
                        from_date, to_date = json.loads(condition.value)
                        condition_checks.append(
                            datetime.strptime(from_date, "%d-%m-%Y").date() <= field_data.date() <= datetime.strptime(
                                to_date, "%d-%m-%Y").date())
            if self.rule_predicate == 'all':
                if all(condition_checks):
                    self.filtered_mails.append(response['id'])
            else:
                if any(condition_checks):
                    self.filtered_mails.append(response['id'])

    def get_label(self, label_name):

        """
    The get_label function takes a label name as an argument and returns the corresponding label ID.

    :param self: Represent the instance of the class
    :param label_name: Find the label id of a specific label
    :return: The label's id
    :doc-author: prabhakarant
    """
        all_user_labels = self.service.users().labels().list(userId='me').execute()
        for label in all_user_labels['labels']:
            if label['name'].lower() == label_name:
                return label['id']

    def execute_actions(self):

        """
    The execute_actions function takes the actions that have been defined for a given rule and applies them to all
    messages that match the filter criteria. It does this by creating a new batch request, which is then populated with
    modify requests for each message in filtered_mails. The modify request contains information about what action should be
    taken on the message (e.g., mark it as read or move it to another folder). Once all of these requests are added to the
    batch, they are executed.

    :param self: Access the attributes of the class
    :doc-author: prabhakarant
    """

        message_body = {}
        type_list = []
        for action in self.actions:
            type_list.append(action.type)
        batch = self.service.new_batch_http_request()
        if "mark_read" in type_list:
            message_body['removeLabelIds'] = ["UNREAD"]
        if "move_to_folder" in type_list:
            label = self.get_label(action.value)
            message_body['addLabelIds'] = [label]
        for message in self.filtered_mails:
            batch.add(self.service.users().messages().modify(userId='me', id=message, body=message_body))
        batch.execute()
        self.filtered_mails = []

    def execute(self):

        """
    The execute function is the main function of this class. It first gets all mails from the user's inbox, then it iterates
    over them and adds a request to get each mail to a batch request. The callback for each mail is execute_rule, which will
    check if any rule applies to that specific mail and add an action (if applicable) to self.actions.

    :param self: Represent the instance of the class
    :doc-author: prabhakarant
    """
        messages_api = self.service.users().messages()
        all_mail_req = self.service.users().messages().list(userId='me', maxResults=100)
        count = 1
        while all_mail_req:
            all_mails = all_mail_req.execute()
            batch = self.service.new_batch_http_request()
            for mail in all_mails['messages']:
                batch.add(self.service.users().messages().get(userId="me", id=mail["id"]), callback=self.execute_rule)
            batch.execute()
            all_mail_req = messages_api.list_next(all_mail_req, all_mails)
            count += 1
            self.execute_actions()
