# jlabs-academy-aws

Materials from my presentation during J-Labs Academy Devops/AWS 2015-01-12

- [ansible-deployer](ansible-deployer) - Ansible playbook used to test all provisioned VMs
    - [inventory](ansible-deployer/inventory) - directory with inventory and variable files
    - [plays](ansible-deployer/plays) - directory with playbooks
    - [vault](ansible-deployer/vault) - directory with vault files
- [libcloud_provisioner/provision.py](libcloud_provisioner/provision.py) - Python wrapper for libcloud
  that acts as simple EC2 provisioner
  
## Cheatsheets ###

#### Create EC2 from AWS console ####

- create instance from AWS console (manually via GUI)
- edit **inventory/prod** and replace IP addr with the new one
- simply invoke `ansible-playbook -i inventory/prod plays/deploy_ec2_nginx.yml --extra-vars="www_msg=manual-deploy"`

#### Poke with AWS CLI ###

- create security group:
    - `aws ec2 create-security-group --group-name <group_name> --description test --region eu-central-1 --vpc-id <vpc_id>`
    - `aws ec2 authorize-security-group-ingress --group-id <group_id> --protocol tcp --port 22 --cidr 0.0.0.0/0 --region eu-central-1`
- provision VM:
    - `aws ec2 --output json --profile <aws_config_profile> --region eu-central-1 run-instances --image-id <ami_id> --instance-type t2.micro --security-groups <group_name> --key-name <key_name>`
    - wait till it's deployed: `aws --profile <aws_config_profile> ec2 describe-instances --filters "Name=instance-state-name,Values=running,pending"`
    - get IP addr: `aws --profile <aws_config_profile> ec2 describe-instances --filters "Name=instance-state-name,Values=running,pending" | grep PublicIp`
- edit **inventory/prod** and replace IP addr with the new one
- run Ansible Nginx installer:
    - `ansible-playbook -i inventory/prod plays/deploy_ec2_nginx.yml --extra-vars="www_msg=awscli-deploy"`
- Simply `curl <PublicIp>`