# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os
from azure.iot.device import ProvisioningDeviceClient
import logging
import json


class Wizard(object):
    def __init__(self, first_name, last_name, dict_of_stuff):
        self.first_name = first_name
        self.last_name = last_name
        self.props = dict_of_stuff


logging.basicConfig(level=logging.INFO)

provisioning_host = os.getenv("PROVISIONING_HOST")
id_scope = os.getenv("PROVISIONING_IDSCOPE")
registration_id = os.getenv("PROVISIONING_REGISTRATION_ID")
symmetric_key = os.getenv("PROVISIONING_SYMMETRIC_KEY")

provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
    provisioning_host=provisioning_host,
    registration_id=registration_id,
    id_scope=id_scope,
    symmetric_key=symmetric_key,
)

properties = {"House": "Gryffindor", "Muggle-Born": "False"}
wizard_a = Wizard("Harry", "Potter", properties)

# Working
# custom_payload = "{\"payload\":{\"first_name'\": \"Jake\", \"last_name\": \"Doyle\"}}"
# Not Working
# custom_payload = "{\"payload\":{\"students\": [{\"first_name\": \"Jake\", \"last_name\": \"Foo\"}, {\"first_name\": \"Jason\", \"last_name\": \"Bar\"}]}}"

# Working
# custom_payload = "{\"payload\":{\"__iot:interfaces\":{\"capabilityModelId\":\"urn:example:com:MXChip:1\"}}}"
# Not Working
# custom_payload = "{\"payload\":{\"__iot:interfaces\":{\"capabilityModelId\":\"urn:example:com:MXChip\"}}}"
# "{\"__iot:interfaces\":{\"capabilityModelId\":\"urn:example:com:MXChip:1\"}}"
# "{\"__iot:interfaces\":{\"capabilityModelId\":\"urn:example:com:MXChip\"}}"
# custom_payload = json.dumps(custom_payload, default=lambda o: o.__dict__)

# custom_payload = "{\"registrationId\":\"testhardwareid1234\",\"payload\":{\"first_name\": \"Harry\", \"last_name\": \"Potter\", \"props\": {\"House\": \"Gryffindor\", \"Muggle-Born\": \"False\"}}}"
custom_payload = '{"registration_id":"testhardwareid1234","payload":{"first_name":"Harry", "last_name": "Potter", "props": {"House": "Gryffindor", "Muggle-Born": "False"}}}'

provisioning_device_client.set_provisioning_payload(custom_payload)
registration_result = provisioning_device_client.register()
# The result can be directly printed to view the important details.
print(registration_result)

# Individual attributes can be seen as well
print("The request_id was :-")
print(registration_result.request_id)
print("The etag is :-")
print(registration_result.registration_state.etag)
