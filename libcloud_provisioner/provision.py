#!/usr/lib/python

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.base import NodeImage

from ConfigParser import SafeConfigParser
parser = SafeConfigParser()
parser.read('/home/docent/.aws/credentials')

ACCESS_ID = parser.get('docent', 'aws_access_key_id')
SECRET_KEY = parser.get('docent', 'aws_secret_access_key')

config = {
    'ami': 'ami-83cfd1ef',
    'instance_type': 't2.micro',
    'region': 'eu-central-1',
    'keypair': 'docent_ocado',
    'security_group': 'web-1'
}


cls = get_driver(Provider.EC2)
driver = cls(ACCESS_ID, SECRET_KEY, region=config['region'])

# Here we select
sizes = driver.list_sizes()
size = [s for s in sizes if s.id == config['instance_type']][0]
image = NodeImage(id=config['ami'], name=None, driver=driver)

node = driver.create_node(
                        name='test-node',
                        image=image,
                        size=size,
                        ex_keyname=config['keypair'],
                        ex_securitygroup=config['security_group'])