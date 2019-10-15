# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import pytest
import logging
from azure.iot.device.common.pipeline import pipeline_events_base
from tests.common.pipeline import pipeline_data_object_test

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.describe("PipelineEvent object")
class TestPipelineEvent(object):
    @pytest.mark.it("Can't be instantiated")
    def test_instantiate(self):
        with pytest.raises(TypeError):
            pipeline_events_base.PipelineEvent()


@pytest.mark.describe("IotResponseEvent object")
class TestIotResponseEvent(object):
    pass


pipeline_data_object_test.add_event_test(
    test_cls=TestIotResponseEvent,
    cls=pipeline_events_base.IotResponseEvent,
    positional_arguments=["request_id", "status_code", "response_body"],
    keyword_arguments={},
)
