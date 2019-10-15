# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import logging
import pytest
from azure.iot.device.common.pipeline import pipeline_events_mqtt
from tests.common.pipeline import pipeline_data_object_test

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.describe("IncomingMQTTMessageEvent object")
def TestIncomingMQTTMessageEvent(object):
    pass


pipeline_data_object_test.add_event_test(
    test_cls=TestIncomingMQTTMessageEvent,
    cls=pipeline_events_mqtt.IncomingMQTTMessageEvent,
    positional_arguments=["topic", "payload"],
    keyword_arguments={},
)
