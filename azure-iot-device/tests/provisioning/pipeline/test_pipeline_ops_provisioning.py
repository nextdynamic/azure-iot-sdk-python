# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import logging
import pytest
from azure.iot.device.provisioning.pipeline import pipeline_ops_provisioning
from tests.common.pipeline import pipeline_data_object_test

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.describe("SetSymetricKeySecurityClientOperation object")
class TestSetSymetricKeySecurityClientOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestSetSymetricKeySecurityClientOperation,
    cls=pipeline_ops_provisioning.SetSymmetricKeySecurityClientOperation,
    positional_arguments=["security_client", "callback"],
)


@pytest.mark.describe("SetProvisioningClientConnectionArgs object")
class TestSetProvisioningClientConnectionArgs(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestSetProvisioningClientConnectionArgs,
    cls=pipeline_ops_provisioning.SetProvisioningClientConnectionArgsOperation,
    positional_arguments=["provisioning_host", "registration_id", "id_scope", "callback"],
    keyword_arguments={"client_cert": None, "sas_token": None},
)


@pytest.mark.describe("SendRegistraionRequestOperation object")
class TestSendRegistraionRequestOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestSendRegistraionRequestOperation,
    cls=pipeline_ops_provisioning.SendRegistrationRequestOperation,
    positional_arguments=["request_id", "request_payload", "callback"],
)


@pytest.mark.describe("SendQueryRequestOperation object")
class TestSendQueryRequestOperation(object):
    pass


pipeline_data_object_test.add_operation_test(
    test_cls=TestSendQueryRequestOperation,
    cls=pipeline_ops_provisioning.SendQueryRequestOperation,
    positional_arguments=["request_id", "operation_id", "request_payload", "callback"],
)
