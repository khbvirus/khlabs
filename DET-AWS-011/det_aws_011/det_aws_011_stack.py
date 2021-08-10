import base64
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_elasticloadbalancingv2 as elbv2,
    aws_autoscaling as autoscaling,
    core as cdk
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.


instance_type = ec2.InstanceType("t3.small")
# key_name = "test-alb"  # Setup key_name for EC2 instance login 

ubuntu_ami = ec2.GenericLinuxImage({
    "eu-west-1": "ami-0a8e758f5e873d1c1"
})
linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                 )  # Indicate your AMI, no need a specific id in the region
with open("./user_data/user_data_amazonlinux2.sh") as f:
    user_data_linux = f.read()

userdata_linux=ec2.UserData.for_linux()
userdata_linux.add_commands(user_data_linux)

with open("./user_data/user_data_ubuntu.sh") as f:
    user_data_ubuntu = f.read()

userdata_ubuntu=ec2.UserData.for_linux()
userdata_ubuntu.add_commands(user_data_ubuntu)


class DetAws011Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        #Parameter: LinuxDistro
        # distro = cdk.CfnParameter(self, 'distro',allowed_values=["ubuntu","amazonlinux2"],type="String")

        #Getting the data
        vpc = ec2.Vpc.from_lookup(self, "VPC",vpc_name="AwsLabsCoreStack/labs-core-vpc")

        #Instance Profile fro ec2-instance
        role = iam.Role(self, "myDVWA-Role", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))


        #Creating the instance that will host DVWA
        # dvwa_instance = ec2.Instance(self, "myDVWA",
        #                                vpc=vpc, 
        #                                vpc_subnets= ec2.SubnetSelection(subnet_type=ec2.SubnetType.ISOLATED),
        #                                instance_name="myDVWA",
        #                                instance_type=instance_type, 
        #                                key_name=key_name,
        #                                machine_image= linux_ami,
        #                                role = role,
        #                                user_data=userdata)

        security_group = ec2.SecurityGroup(
            self, "openHTTPtoASGs",
            vpc=vpc,
            allow_all_outbound=True
        )
        security_group.add_ingress_rule(
            ec2.Peer.ipv4("10.20.0.0/16"),
            ec2.Port.tcp(80)
        )

        # print(distro.value_as_string)

        # if (distro.value_as_string == "amazonlinux2"):
        #     asg_amazonlinux = autoscaling.AutoScalingGroup(
        #         self,
        #         "DVWA_LINUX_ASG",
        #         vpc=vpc,
        #         vpc_subnets= ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        #         instance_type=instance_type, 
        #         key_name=key_name,
        #         machine_image= linux_ami,
        #         role = role,
        #         user_data=userdata_linux
        #     )
        #     listener.add_targets("Target", port=80, targets=[asg_amazonlinux])
        
        # if (distro.value_as_string == "ubuntu"):
        asg_ubuntu = autoscaling.AutoScalingGroup(
            self,
            "DVWA_UBUNTU_ASG",
            vpc=vpc,
            vpc_subnets= ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            instance_type=instance_type, 
            # key_name=key_name,
            machine_image= ubuntu_ami,
            role = role,
            user_data=userdata_ubuntu
        )
        


        #Creating the ALB
        lb = elbv2.ApplicationLoadBalancer(
            self, "LB",
            vpc=vpc,
            internet_facing=True)

        listener = lb.add_listener("Listener", port=80)
        listener.connections.allow_default_port_from_any_ipv4("Open to the world")
        listener.add_targets("Target", port=80, targets=[asg_ubuntu])
        
        output = cdk.CfnOutput(self, "LoadBalancer DNS NAME",
                                value=lb.load_balancer_dns_name,
                                description="Application Load Balancer DNS")
    
        #Creating the WAF