# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import pytest
import logging
from azure.iot.device.provisioning.abstract_provisioning_device_client import (
    AbstractProvisioningDeviceClient,
)
import json

logging.basicConfig(level=logging.DEBUG)


class Wizard(object):
    def __init__(self, first_name, last_name, dict_of_stuff):
        self.first_name = first_name
        self.last_name = last_name
        self.props = dict_of_stuff


def test_raises_exception_on_init_of_abstract_client(mocker):
    fake_pipeline = mocker.MagicMock()
    with pytest.raises(TypeError):
        AbstractProvisioningDeviceClient(fake_pipeline)


class Student(object):
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class Team(object):
    def __init__(self, students):
        self.students = students


def test_object_complex():
    student1 = Student(first_name="Jake", last_name="Foo")
    student2 = Student(first_name="Jason", last_name="Bar")
    team = Team(students=[student1, student2])

    # print(type(team))
    # Serializing
    data = json.dumps(team, default=lambda o: o.__dict__)
    print(data)

    properties = {"House": "Gryffindor", "Muggle-Born": "False"}
    wizard_a = Wizard("Harry", "Potter", properties)
    # print(type(wizard_a))

    json_data_1 = json.dumps(wizard_a, default=lambda o: o.__dict__)
    print(json_data_1)

    # json_data_2 = json.dumps(wizard_a.__dict__)
    # print(json_data_2)
    #
    # json_data_3 = json.dumps("String string string")
    # print(json_data_3)

    device_reg_payload = DeviceRegistrationPayload(
        registration_id="123213", custom_payload=wizard_a
    )
    publish_payload = device_reg_payload.get_json()
    print(publish_payload)


class DeviceRegistrationPayload(object):
    def __init__(self, registration_id, custom_payload):
        self.registration_id = registration_id
        self.payload = custom_payload

    def get_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
