# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import logging
import pytest
from azure.iot.device.iothub.pipeline import pipeline_events_iothub
from tests.common.pipeline import pipeline_data_object_test

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.describe("C2DMessageEvent object")
class TestC2DMessageEvent(object):
    pass


pipeline_data_object_test.add_event_test(
    test_cls=TestC2DMessageEvent,
    cls=pipeline_events_iothub.C2DMessageEvent,
    positional_arguments=["message"],
    keyword_arguments={},
)


@pytest.mark.describe("InputMessageEvent object")
class TestInputMessageEvent(object):
    pass


pipeline_data_object_test.add_event_test(
    test_cls=TestInputMessageEvent,
    cls=pipeline_events_iothub.InputMessageEvent,
    positional_arguments=["input_name", "message"],
    keyword_arguments={},
)


@pytest.mark.describe("MethodRequestEvent object")
class TestMethodRequestEvent(object):
    pass


pipeline_data_object_test.add_event_test(
    test_cls=TestMethodRequestEvent,
    cls=pipeline_events_iothub.MethodRequestEvent,
    positional_arguments=["method_request"],
    keyword_arguments={},
)


@pytest.mark.describe("TwinDesiredPropertiesPatchEvent object")
class TestTwinDesiredPropertiesPatchEvent(object):
    pass


pipeline_data_object_test.add_event_test(
    test_cls=TestTwinDesiredPropertiesPatchEvent,
    cls=pipeline_events_iothub.TwinDesiredPropertiesPatchEvent,
    positional_arguments=["patch"],
    keyword_arguments={},
)
