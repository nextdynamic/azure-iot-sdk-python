# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import logging
import pytest
from azure.iot.device.provisioning.pipeline import pipeline_events_provisioning
from tests.common.pipeline import pipeline_data_object_test

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.describe("RegistrationResponseEvent object")
class TestRegistrationResponseEvent(object):
    pass


pipeline_data_object_test.add_event_test(
    test_cls=TestRegistrationResponseEvent,
    cls=pipeline_events_provisioning.RegistrationResponseEvent,
    positional_arguments=["request_id", "status_code", "key_values", "response_payload"],
    keyword_arguments={},
)
