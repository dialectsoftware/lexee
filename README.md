# lexee
Lexee example implementation for AWS IAM

**Lexee** is an extensible interpreter for the [**pylingo**](https://github.com/dialectsoftware/pylingo) declarative grammar. Lexee enables a programmer to quickly generate a DSL for virtually any purpose. Internally lexee maps the pylingo grammar to your custom classes. Syntactically pylingo is a very flexible grammar which allows you to express constructs with json and/or object syntax. Pylingo and by extension lexee has 5 basic constructs **config**, **variable**, **import**, **data** and **generator**. Config, for which there may be only one per document, is used to store runtime invariant data. Variables are used to capture runtime data, creating a contract between the runtime and the user. Imports bring in the namespaces from which data and generators can be bound. Data which are executable entities that retrieve data external to the environment at runtime and generators which effect state changes within the environment or within external resources. 

Lexee executes on the [**protolingo**](https://github.com/dialectsoftware/protolingo) runtime. This gives your DSL support for topological sorting and templating using {{ mustache }} syntax. Future versions of lexee will add the same state management features that are supported when using the YAML DSL natively supported by protolingo. The following example creates a DSL capable of creating roles and policies within AWS IAM, however, the grammar can be leveraged to perform any kind of function. This example is intended to demonstrate each one of the features of lexee in a manner that is hopefully self-explanatory. The example assumes that you have an AWS account and that you configure the AWS cli with a default profile (which will be leveraged by boto3). The example creates a policy and a role in your account and then attaches the customer managed policy as well as several AWS managed policies, necessary to manage an EKS cluster, to the role.  


Command to run the example:

```bash
pip install lexee
pip install boto3
aws configure
python -m lexee eks.lexee
```

Example:

```bash
config {
   name = "EKS config language"
   exit_on_error = "False"
   aws {
	   eks {
		   prefix = "MY"
	   }
	   profile = "default"
   }
}

import security {
	module = "aws.iam"
}

variable aws profile {
	description = "profile"
	default = "{{ config.aws.profile }}"
}

data aws sts identity current {}


# Note that the AssumeRolePolicyDocument is about defining the trust relationship and not the actual permissions of the role you are creating.
generator security role eks {
	Path="/"
	RoleName = "{{  config.aws.eks.prefix }}ServiceRoleForAmazonEKS"
	Description = "EKS Service Role"
	AssumeRolePolicyDocument= {
		"Version":"2012-10-17",
		"Statement" : [{
			"Effect" :"Allow",
			"Principal" : {
				"Service":"eks.amazonaws.com",
				"AWS":"arn:aws:iam::{{ data.aws.sts.identity.current.Account }}:root"
			},
			"Action": "sts:AssumeRole"
		}]			
	}
	Tags=[]
	depends_on=["data.aws.sts.identity.current"]
}

# Create policy for the EKS service role.
generator security policy eks {
	PolicyName = "{{  config.aws.eks.prefix }}ServiceRolePolicyForAmazonEKS"
	PolicyDocument= {
		"Version":"2012-10-17",
		"Statement" : [{
			"Effect" :"Allow",
			"Action": "iam:PassRole",
			"Resource":"{{  generator.security.role.eks.response.Role.Arn }}"			
		},
		{
			"Effect" :"Allow",
			"Action": "eks:*",
			"Resource": "*"

		}]		
	}
	Tags=[]
	depends_on=["generator.security.role.eks"]
}

# Attach policy for the EKS service role.
generator security attach_policy eks {
	PolicyArn = "{{ generator.security.policy.eks.response.Policy.Arn }}"
	RoleName = "{{ generator.security.role.eks.response.Role.RoleName }}"
	depends_on=["generator.security.role.eks","generator.security.policy.eks"]
}


# Attach managed policy for the EKS service role.
generator security attach_policy cluster {
	PolicyArn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
	RoleName = "{{ generator.security.role.eks.response.Role.RoleName }}"
	depends_on=["generator.security.role.eks","generator.security.policy.eks"]
}
	

# Attach managed policy for the EKS service role.
generator security attach_policy viewonly {
	PolicyArn = "arn:aws:iam::aws:policy/job-function/ViewOnlyAccess"
	RoleName = "{{ generator.security.role.eks.response.Role.RoleName }}"
	depends_on=["generator.security.role.eks","generator.security.policy.eks"]
}


# Attach managed policy for the EKS service role.
generator security attach_policy events {
	PolicyArn = "arn:aws:iam::aws:policy/CloudWatchEventsReadOnlyAccess"
	RoleName = "{{ generator.security.role.eks.response.Role.RoleName }}"
	depends_on=["generator.security.role.eks","generator.security.policy.eks"]
}

# Attach managed policy for the EKS service role.
generator security attach_policy logs {
	PolicyArn = "arn:aws:iam::aws:policy/CloudWatchLogsReadOnlyAccess"
	RoleName = "{{ generator.security.role.eks.response.Role.RoleName }}"
	depends_on=["generator.security.role.eks","generator.security.policy.eks"]
}

# Attach managed policy for the EKS service role.
generator security attach_policy service {
	PolicyArn = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
	RoleName = "{{ generator.security.role.eks.response.Role.RoleName }}"
	depends_on=["generator.security.role.eks","generator.security.policy.eks"]
}


```
