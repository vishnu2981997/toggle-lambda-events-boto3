import json
import os
import uuid

import boto3
from botocore.client import ClientError


class Boto3:
    __region_name = None
    __aws_access_key_id = None
    __aws_secret_access_key = None

    def __init__(self, params: dict) -> None:
        self.__region_name = params.get("region_name", None)
        if not self.__region_name:
            raise Exception("region_name required")

        self.__aws_access_key_id = params.get("aws_access_key_id", None)
        if not self.__aws_access_key_id:
            raise Exception("aws_access_key_id required")

        self.__aws_secret_access_key = params.get("aws_secret_access_key", None)
        if not self.__aws_secret_access_key:
            raise Exception("aws_secret_access_key required")

        self.__client = None

    def initialize_client(self, client_type: str) -> bool:
        try:
            self.__client = boto3.client(
                client_type,
                region_name=self.__region_name,
                aws_access_key_id=self.__aws_access_key_id,
                aws_secret_access_key=self.__aws_secret_access_key
            )
            return True
        except ClientError as exe:
            raise Exception(exe)
        except Exception as exe:
            raise Exception(exe)

    def disable_rule(self, rule_name: str) -> object:
        if not self.__client:
            raise Exception("client has not been initialized")

        try:
            return self.__client.disable_rule(Name=rule_name)
        except ClientError as exe:
            raise Exception(exe)
        except Exception as exe:
            raise Exception(exe)

    def enable_rule(self, rule_name: str) -> object:
        if not self.__client:
            raise Exception("client has not been initialized")

        try:
            return self.__client.enable_rule(Name=rule_name)
        except ClientError as exe:
            raise Exception(exe)
        except Exception as exe:
            raise Exception(exe)

    def toggle_rules(self, rules: []) -> []:
        response = []
        print('rules', rules)
        for rule in rules:
            data = {
                "rule": rule.get("name", None)
            }
            print('rule', data)
            try:
                if rule.get("status"):
                    data["result"] = self.enable_rule(rule_name=data["rule"])
                else:
                    response.append(self.disable_rule(rule_name=data["rule"]))
            except Exception as exe:
                data["error"] = str(exe)

            response.append(data)

        return response


def set_default(obj: object) -> []:
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def lambda_handler(event, context):
    event_log_id = uuid.uuid4()

    api_response = {
        "statusCode": "200",
        "body": {}
    }

    if event["httpMethod"].lower() == "post":
        response = {}
        try:
            # for running in local
            # b3 = Boto3({
            #     "region_name": "<aws region name | str>",
            #     "aws_access_key_id": "<aws access key | str>",
            #     "aws_secret_access_key": "<aws secret key | str>"
            # })

            b3 = Boto3({
                "region_name": os.environ["region_name"],
                "aws_access_key_id": os.environ["aws_access_key_id"],
                "aws_secret_access_key": os.environ["aws_secret_access_key"]
            })

            if b3.initialize_client(client_type="events"):
                response["data"] = b3.toggle_rules(rules=json.loads(event["body"])["rules"])

        except Exception as exe:
            print(event_log_id, str(exe))
            api_response["statusCode"] = "500"
            response["error"] = 'Internal server error - refer uuid: ' + str(event_log_id)

        api_response["body"] = json.dumps(response, default=set_default)
        return api_response

    api_response["statusCode"] = "404"
    api_response["body"] = json.dumps({
        "message": "route not found"
    }, default=set_default)
    return api_response


# for running in local
# print(lambda_handler(
#     {
#         "httpMethod": "post",
#         "body": json.dumps({
#             "rules": [
#                 {"name": "tracking-ids-import-redis", "status": 1}
#             ]
#         })
#     },
#     {}
# ))
