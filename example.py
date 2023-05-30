from googleapiclient.discovery import build

import gmail_rule_runner

gmail_rule_runner.credentials_path= "credentials.json"
gmail_rule_runner.secrets_path= "secrets.pickle"
gmail_rule_runner.rules_file= "sample_rules.json"


def main():
    token = gmail_rule_runner.get_token()
    service = build('gmail', 'v1', credentials=token)
    gmail_rule_runner.execute_all_rules(service)


if __name__ == "__main__":
    main()
