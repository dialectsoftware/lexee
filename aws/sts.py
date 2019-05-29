import sys
import json
import boto3
from lexee.expression import LexeeExpression


class identity(LexeeExpression):
     
    def __init__(self, id=None, depends_on=[], output=None, exit=None, exitCode=None, symbol=None, **kwargs):
        super().__init__(id, depends_on, output, exit, exitCode, symbol, **kwargs)

    def exec(self,**kwargs):
        try:
            result = boto3.client('sts').get_caller_identity()
            print(result)
            self.UserId = result["UserId"]
            self.Account = result["Account"]
            self.Arn = result["Arn"]
            sys.exit(0)
        except Exception as e:
            print(e.__str__(), file=sys.stderr)
            raise

    def __repr__(self):
        return "%s(id=%r, default=%r)" % (
            self.__class__.__name__, self.id)

