# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import pytest
import logging
from azure.iot.device.common.pipeline import pipeline_ops_base
from tests.common.pipeline import pipeline_data_object_test

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.describe("PipelineOperation object")
class TestPipelineOperation(object):
    @pytest.mark.it("Can't be instantiated")
    def test_instantiate(self):
        with pytest.raises(TypeError):
            pipeline_ops_base.PipelineOperation()


@pytest.mark.destribe("ConnectOperation object")
class TestConnectOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestConnectOperation, cls=pipeline_ops_base.ConnectOperation
)


@pytest.mark.destribe("DisconnectOperation object")
class TestDisconnectOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestDisconnectOperation, cls=pipeline_ops_base.DisconnectOperation
)


@pytest.mark.destribe("ReconnectOperation object")
class TestReconnectOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestReconnectOperation, cls=pipeline_ops_base.ReconnectOperation
)


@pytest.mark.destribe("EnbleFeatureOperation object")
class TestEnableFeatureOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestEnableFeatureOperation,
    cls=pipeline_ops_base.EnableFeatureOperation,
    positional_arguments=["feature_name", "callback"],
)


@pytest.mark.destribe("DisableFeatureOperation object")
class TestDisableFeatureOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestDisableFeatureOperation,
    cls=pipeline_ops_base.DisableFeatureOperation,
    positional_arguments=["feature_name", "callback"],
)


@pytest.mark.destribe("UpdateSasTokenOperation object")
class TestUpdateSasTokenOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestUpdateSasTokenOperation,
    cls=pipeline_ops_base.UpdateSasTokenOperation,
    positional_arguments=["sas_token", "callback"],
)


@pytest.mark.destribe("SendIotRequestAndWaitForResponseOperation object")
class TestSendIotRequestAndWaitForResponseOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestSendIotRequestAndWaitForResponseOperation,
    cls=pipeline_ops_base.SendIotRequestAndWaitForResponseOperation,
    positional_arguments=[
        "request_type",
        "method",
        "resource_location",
        "request_body",
        "callback",
    ],
)


@pytest.mark.destribe("SendIotRequestOperation object")
class TestSendIotRequestOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestSendIotRequestOperation,
    cls=pipeline_ops_base.SendIotRequestOperation,
    positional_arguments=[
        "request_type",
        "method",
        "resource_location",
        "request_body",
        "request_id",
        "callback",
    ],
)
