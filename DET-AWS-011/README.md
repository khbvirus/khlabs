# Welcome to LAB: DET-AWS-011

This lab is using AWS CDK to automate the deployment and deletion process. It facilitates also modification and replication.

This LAB is to deploy a vulnerable web application and a WAF in front of it in an attempt to detect and/or block malicious traffic.

# Some specifics about the stack:

The load balancer is not open to the world.
When you use the alb default construct and add a listener, cdk add a sg ingress allowing traffic from 0.0.0.0/0. To avoid this wh have to restrict the openness of the lisner when we add it to the ALB:
listener = lb.add_listener("Listener", port=80, open=False)

# TODO:

Add AWS WAF.
Activate Logs for AWS WAF.
Configure AWS WAF to send logs.

Add secret in AWS Secret Manager for the database secret and use it in userdata script: DONE.
Restrict the LB SG to personal IP address : DONE
Make some folders writeable(DVWA Config). : DONE
