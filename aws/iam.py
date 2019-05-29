import sys
import json
import boto3
import datetime
from dateutil.tz import tzutc
from lexee.expression import LexeeExpression

class role(LexeeExpression):
     
    def __init__(self, id=None, depends_on=[], output=None, exit=None, exitCode=None, symbol=None, **kwargs):
        super().__init__(id, depends_on, output, exit, exitCode, symbol, **kwargs)

    def exec(self,**kwargs):
        try:
            client = boto3.client("iam")
            response = client.create_role(
                Path=self.Path,
                RoleName=self.RoleName,
                AssumeRolePolicyDocument=json.dumps(self.AssumeRolePolicyDocument),
                Description=self.Description,
                MaxSessionDuration=3600,
                Tags=self.Tags
            )
            self.response = response
            print(response)
            sys.exit(0)
        except Exception as e:
            print(e.__str__(), file=sys.stderr)
            raise

    def __repr__(self):
        return "%s(id=%r, default=%r)" % (
            self.__class__.__name__, self.id)

class policy(LexeeExpression):
     
    def __init__(self, id=None, depends_on=[], output=None, exit=None, exitCode=None, symbol=None, **kwargs):
        super().__init__(id, depends_on, output, exit, exitCode, symbol, **kwargs)

    def exec(self,**kwargs):
        try:
            client = boto3.client("iam")
            response = client.create_policy(
                PolicyName=self.PolicyName,
                PolicyDocument=json.dumps(self.PolicyDocument)
            )
            self.response = response
            print(response)
            sys.exit(0)
        except Exception as e:
            print(e.__str__(), file=sys.stderr)
            raise

    def __repr__(self):
        return "%s(id=%r, default=%r)" % (
            self.__class__.__name__, self.id)

class attach_policy(LexeeExpression):
     
    def __init__(self, id=None, depends_on=[], output=None, exit=None, exitCode=None, symbol=None, **kwargs):
        super().__init__(id, depends_on, output, exit, exitCode, symbol, **kwargs)

    def exec(self,**kwargs):
        try:
            client = boto3.client("iam")
            response = client.attach_role_policy(
                PolicyArn=self.PolicyArn,
                RoleName=self.RoleName
            )
            self.response = response
            sys.exit(0)
        except Exception as e:
            print(e.__str__(), file=sys.stderr)
            raise

    def __repr__(self):
        return "%s(id=%r, default=%r)" % (
            self.__class__.__name__, self.id)