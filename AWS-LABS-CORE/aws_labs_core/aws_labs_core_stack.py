from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_ec2 as ec2



# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class AwsLabsCoreStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # LABS_CORE VPC
        self.vpc = ec2.Vpc(
            self, "labs-core-vpc",
            cidr="10.20.0.0/16",
            max_azs=3,
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(subnet_type=ec2.SubnetType.PUBLIC,name="labs-core-vpc-public-subnet",cidr_mask=24),
                # ec2.SubnetConfiguration(subnet_type=ec2.SubnetType.PRIVATE,name="labs-core-vpc-private-subnet",cidr_mask=24),
                ec2.SubnetConfiguration(subnet_type=ec2.SubnetType.ISOLATED,name="labs-core-vpc-isolated-subnet",cidr_mask=24)
            ]
        )
        self.vpc.add_flow_log("labs-core-vpc-flowLog")

        security_group = ec2.SecurityGroup(self, "labs-core-Allow443ForSSMEndpoints",
            vpc=self.vpc,
            allow_all_outbound=False
        )
        security_group.add_ingress_rule(
            ec2.Peer.ipv4(self.vpc.vpc_cidr_block),
            ec2.Port.tcp(443)
        )
        
        # AWS INTERFACE ENDPOINTS Needed for SSM Session Manager
        # "com.amazonaws.eu-west-3.ec2messages",
        # "com.amazonaws.eu-west-3.ssm",
        # "com.amazonaws.eu-west-3.ssmmessages",

        ssmEndpoints = ['ec2messages', 'ssm', 'ssmmessages']
        for ssmEndpoint in ssmEndpoints:   
            # vpc.add_interface_endpoint("labs-core-"+ssmEndpoint,service=ec2.InterfaceVpcEndpointService("com.amazonaws."+core.Aws.REGION+"."+ssmEndpoint,443))
            self.vpc.add_interface_endpoint("labs-core-"+ssmEndpoint,service=ec2.InterfaceVpcEndpointService("com.amazonaws."+core.Aws.REGION+ "."+ssmEndpoint,443),private_dns_enabled=True, security_groups=[security_group])

