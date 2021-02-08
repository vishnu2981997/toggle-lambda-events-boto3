# toggle-lambda-events-boto3
enable/ disable aws lambda triggers(rules) using boto3 and python
## Prerequisites
* python 3.8.x

## Deployment

1. Install boto3 into the toggle-lambda-events function

```terminal
pip install --target={{path_to_toggle-lambda-events}} boto3
```
eg:
```terminal
pip install --target=D:\vishnu_personal\projects\rf\toggle-lambda-events boto3
```

2. Zip the the files including the packages
```
- toggle-lambda-events.zip
    - bin
    - boto3
    - boto3-1.17.3.dist-info
    - .
    - .
    - .
    - lambda_function.py
```
3. Specify the following env variables in the lambda environment variables

    * aws_access_key_id
    * aws_secret_access_key
    * region_name

4. Upload the zipfile to the respective lambda function

## Execution

Assuming a succesfull api gateway has been setup for the lambda

Using the entry point perform a POST request with the following JSON format as body

```terminal
{
  "rules": [
    {
      "name": "<rule name | str>",
      "status": <status | bool | 0-disable 1-enable>
    }
  ]
}
```
eg:
```terminal
{
  "rules": [
    {
      "name": "rule-1",
      "status": 0
    },
    {
      "name": "rule-2",
      "status": 1
    }
  ]
}
```

