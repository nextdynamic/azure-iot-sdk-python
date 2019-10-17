# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from azure.iot.device.common.pipeline.pipeline_ops_base import PipelineOperation


class SetSymmetricKeySecurityClientOperation(PipelineOperation):
    """
    A PipelineOperation object which tells the pipeline to use a symmetric key security client.
    Some pipeline stage is expected to extract arguments out of the security client and pass them
    on so an even lower stage can use those arguments to connect.

    This operation is in the group of provisioning operations because security clients are currently
    very provisioning-specific
    """

    def __init__(self, security_client, callback):
        """
        Initializer for SetSecurityClient.

        :param object security_client: The security client object to use to retrieve connection parameters
          which can be used to connect to the service.
        :param Function callback: The function that gets called when this operation is complete or has failed.
         The callback function must accept A PipelineOperation object which indicates the specific operation which
         has completed or failed.
        """
        super(SetSymmetricKeySecurityClientOperation, self).__init__(callback=callback)
        self.security_client = security_client


class SetX509SecurityClientOperation(PipelineOperation):
    """
    A PipelineOperation object which contains connection arguments which were retrieved from a
    X509 security client likely by a pipeline stage which handles the
    SetX509SecurityClientOperation operation.

    This operation is in the group of Provisioning operations because the arguments which it accepts are
    very specific to DPS connections and would not apply to other types of client connections
    (such as a Provisioning client).
    """

    def __init__(self, security_client, callback):
        """
        Initializer for SetSecurityClient.

        :param object security_client: The security client object to use to retrieve connection parameters
        which can be used to connect to the service.
        :param Function callback: The function that gets called when this operation is complete or has failed.
        The callback function must accept A PipelineOperation object which indicates the specific operation which
        has completed or failed.
        """
        super(SetX509SecurityClientOperation, self).__init__(callback=callback)
        self.security_client = security_client


class SetProvisioningClientConnectionArgsOperation(PipelineOperation):
    """
    A PipelineOperation object which contains connection arguments which were retrieved from a
    symmetric key or a X509 security client likely by a pipeline stage which handles the
    SetSymmetricKeySecurityClientOperation or SetX509SecurityClientOperation operation.

    This operation is in the group of Provisioning operations because the arguments which it accepts are
    very specific to DPS connections and would not apply to other types of client connections
    (such as a Provisioning client).
    """

    def __init__(
        self,
        provisioning_host,
        registration_id,
        id_scope,
        callback,
        client_cert=None,
        sas_token=None,
    ):
        """
        Initializer for SetProvisioningClientConnectionArgsOperation.
        :param registration_id: The registration ID is used to uniquely identify a device in the Device Provisioning Service.
        The registration ID is alphanumeric, lowercase string and may contain hyphens.
        :param id_scope: The ID scope is used to uniquely identify the specific provisioning service the device will
        register through. The ID scope is assigned to a Device Provisioning Service when it is created by the user and
        is generated by the service and is immutable, guaranteeing uniqueness.
        """
        super(SetProvisioningClientConnectionArgsOperation, self).__init__(callback=callback)
        self.provisioning_host = provisioning_host
        self.registration_id = registration_id
        self.id_scope = id_scope
        self.client_cert = client_cert
        self.sas_token = sas_token


class SendRegistrationRequestOperation(PipelineOperation):
    """
    A PipelineOperation object which contains arguments used to send a registration request
    to an Device Provisioning Service.

    This operation is in the group of DPS operations because it is very specific to the DPS client.
    """

    def __init__(self, request_id, request_payload, registration_id, callback=None):
        """
        Initializer for SendRegistrationRequestOperation objects.

        :param request_id : The id of the request being sent
        :param request_payload: The request that we are sending to the service
        :param registration_id: The registration ID is used to uniquely identify a device in the Device Provisioning Service.
        :param Function callback: The function that gets called when this operation is complete or has failed.
         The callback function must accept A PipelineOperation object which indicates the specific operation which
         has completed or failed.
        """
        super(SendRegistrationRequestOperation, self).__init__(callback=callback)
        self.request_id = request_id
        self.request_payload = request_payload
        self.registration_id = registration_id


class SendQueryRequestOperation(PipelineOperation):
    """
    A PipelineOperation object which contains arguments used to send a registration request
    to an Device Provisioning Service.

    This operation is in the group of DPS operations because it is very specific to the DPS client.
    """

    def __init__(self, request_id, operation_id, request_payload, callback):
        """
        Initializer for SendRegistrationRequestOperation objects.

        :param request_id
        :param request_payload: The request that we are sending to the service
        :param Function callback: The function that gets called when this operation is complete or has failed.
         The callback function must accept A PipelineOperation object which indicates the specific operation which
         has completed or failed.
        """
        super(SendQueryRequestOperation, self).__init__(callback=callback)
        self.request_id = request_id
        self.operation_id = operation_id
        self.request_payload = request_payload
