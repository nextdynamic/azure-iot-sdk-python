# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import logging
import pytest
from azure.iot.device.common.pipeline import pipeline_ops_mqtt
from tests.common.pipeline import pipeline_data_object_test

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.describe("SetMQTTConnectionArgsOperation object")
class TestSetMQTTConnectionArgsOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestSetMQTTConnectionArgsOperation,
    cls=pipeline_ops_mqtt.SetMQTTConnectionArgsOperation,
    positional_arguments=["client_id", "hostname", "username", "callback"],
    keyword_arguments={"ca_cert": None, "client_cert": None, "sas_token": None},
)


@pytest.mark.describe("MQTTPublishOperation object")
class TestMQTTPublishOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestMQTTPublishOperation,
    cls=pipeline_ops_mqtt.MQTTPublishOperation,
    positional_arguments=["topic", "payload", "callback"],
    extra_defaults={"needs_connection": True},
)


@pytest.mark.describe("MQTTSubscribeOperation object")
class TestMQTTSubscribeOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestMQTTSubscribeOperation,
    cls=pipeline_ops_mqtt.MQTTSubscribeOperation,
    positional_arguments=["topic", "callback"],
    extra_defaults={"needs_connection": True},
)


@pytest.mark.describe("MQTTUnsubscribeOperation object")
class TestMQTTUnsubscribeOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestMQTTUnsubscribeOperation,
    cls=pipeline_ops_mqtt.MQTTUnsubscribeOperation,
    positional_arguments=["topic", "callback"],
    extra_defaults={"needs_connection": True},
)
