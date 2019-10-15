# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import logging
import pytest
from azure.iot.device.iothub.pipeline import pipeline_ops_iothub
from tests.common.pipeline import pipeline_data_object_test

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.describe("SetAuthProviderOperation object")
class TestSetAuthProviderOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestSetAuthProviderOperation,
    cls=pipeline_ops_iothub.SetAuthProviderOperation,
    positional_arguments=["auth_provider", "callback"],
)


@pytest.mark.describe("SetX509AuthProviderOperation object")
class TestFSetX509AuthProviderOperationoo(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestFSetX509AuthProviderOperationoo,
    cls=pipeline_ops_iothub.SetX509AuthProviderOperation,
    positional_arguments=["auth_provider", "callback"],
)


@pytest.mark.describe("SetIotHubConnectionArgs object")
class TestSetIotHubConnectionArgs(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestSetIotHubConnectionArgs,
    cls=pipeline_ops_iothub.SetIoTHubConnectionArgsOperation,
    positional_arguments=["device_id", "hostname", "callback"],
    keyword_arguments={
        "module_id": None,
        "gateway_hostname": None,
        "ca_cert": None,
        "client_cert": None,
        "sas_token": None,
    },
)


@pytest.mark.describe("SendD2CMessageOperation object")
class TestSendD2CMessageOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestSendD2CMessageOperation,
    cls=pipeline_ops_iothub.SendD2CMessageOperation,
    positional_arguments=["message", "callback"],
)


@pytest.mark.describe("SendOutputEventOperation object")
class TestSendOutputEventOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestSendOutputEventOperation,
    cls=pipeline_ops_iothub.SendOutputEventOperation,
    positional_arguments=["message", "callback"],
)


@pytest.mark.describe("SendMethodResponseOperation object")
class TestSendMethodResponseOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestSendMethodResponseOperation,
    cls=pipeline_ops_iothub.SendMethodResponseOperation,
    positional_arguments=["method_response", "callback"],
)


@pytest.mark.describe("GetTwinOperation object")
class TestGetTwinOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestGetTwinOperation, cls=pipeline_ops_iothub.GetTwinOperation
)


@pytest.mark.describe("PatchTwinReportedPropertiesOperation object")
class TestPatchTwinReportedPropertiesOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestPatchTwinReportedPropertiesOperation,
    cls=pipeline_ops_iothub.PatchTwinReportedPropertiesOperation,
    positional_arguments=["patch", "callback"],
)
