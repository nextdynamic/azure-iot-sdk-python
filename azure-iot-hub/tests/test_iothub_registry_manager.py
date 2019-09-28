# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""This module should be replaced when there are actual tests for the azure.iot.hub library"""

import pytest
from azure.iot.hub.iothub_registry_manager import IoTHubRegistryManager
from azure.iot.hub.protocol.iot_hub_gateway_service_ap_is20190630 import (
    IotHubGatewayServiceAPIs20190630,
)

# from azure.iot.hub.protocol.models.device_py3 import Device
from azure.iot.hub.auth import ConnectionStringAuthentication

from azure.iot.hub.protocol.models import (
    Device,
    Module,
    SymmetricKey,
    X509Thumbprint,
    AuthenticationMechanism,
    Configuration,
    ServiceStatistics,
    RegistryStatistics,
)

fake_shared_access_key = "Zm9vYmFy"
fake_shared_access_key_name = "alohomora"

fake_primary_key = "petrificus"
fake_secondary_key = "totalus"
fake_primary_thumbprint = "HELFKCPOXAIR9PVNOA3"
fake_secondary_thumbprint = "RGSHARLU4VYYFENINUF"
fake_hostname = "beauxbatons.academy-net"
fake_device_id = "MyPensieve"
fake_module_id = "Divination"
fake_managed_by = "Hogwarts"
fake_etag = "taggedbymisnitryogmagic"
fake_status = "flying"


@pytest.fixture(scope="function")
def mock_service_operations(mocker):
    mock_service_operations_init = mocker.patch(
        "azure.iot.hub.protocol.iot_hub_gateway_service_ap_is20190630.ServiceOperations"
    )
    return mock_service_operations_init.return_value


@pytest.fixture(scope="function")
def mock_device_constructor(mocker):
    return mocker.patch("azure.iot.hub.iothub_registry_manager.Device")


def create_registry(shared_access_key):
    connection_string = "HostName={hostname};DeviceId={device_id};SharedAccessKeyName={skn};SharedAccessKey={sk}".format(
        hostname=fake_hostname,
        device_id=fake_device_id,
        skn=fake_shared_access_key_name,
        sk=shared_access_key,
    )
    iothub_registry_manager = IoTHubRegistryManager(connection_string)
    return iothub_registry_manager


@pytest.mark.describe("IoTHubRegistryManager")
class TestIoTHubRegistryManagerInit(object):
    @pytest.mark.it("instantiates correctly with auth")
    def test_init_auth(self):
        iothub_registry_manager = IoTHubRegistryManager(
            "HostName={hostname};DeviceId={device_id};SharedAccessKeyName={skn};SharedAccessKey={sk}".format(
                hostname=fake_hostname,
                device_id=fake_device_id,
                skn=fake_shared_access_key_name,
                sk=fake_shared_access_key,
            )
        )
        assert iothub_registry_manager is not None
        assert iothub_registry_manager.auth is not None
        assert isinstance(iothub_registry_manager.auth, ConnectionStringAuthentication)

    @pytest.mark.it("instantiates correctly with protocol client with correct Service API version")
    def test_init_protocol_client(self):
        iothub_registry_manager = IoTHubRegistryManager(
            "HostName={hostname};DeviceId={device_id};SharedAccessKeyName={skn};SharedAccessKey={sk}".format(
                hostname=fake_hostname,
                device_id=fake_device_id,
                skn=fake_shared_access_key_name,
                sk=fake_shared_access_key,
            )
        )
        assert iothub_registry_manager is not None
        assert iothub_registry_manager.protocol is not None
        assert isinstance(iothub_registry_manager.protocol, IotHubGatewayServiceAPIs20190630)


@pytest.mark.describe("IoTHubRegistryManager Create Device With Symmetric Key")
class TestIoTHubRegistryManagerCreateDeviceWithSymmetricKey(object):
    @pytest.mark.it("initializes device with device id, status and sas auth having primary key")
    def test_initializes_device_with_kwargs_having_primary_sas(
        self, mock_device_constructor, mock_service_operations
    ):
        iothub_registry_manager = create_registry(fake_shared_access_key)

        iothub_registry_manager.create_device_with_sas(
            device_id=fake_device_id,
            primary_key=fake_primary_key,
            secondary_key=None,
            status=fake_status,
        )
        assert_device_attributes_for_sas(
            mock_device_constructor, primary_key=fake_primary_key, secondary_key=None
        )

    @pytest.mark.it("initializes device with device id, status and sas auth having secondary key")
    def test_initializes_device_with_kwargs_having_secondary_sas(
        self, mock_device_constructor, mock_service_operations
    ):
        iothub_registry_manager = create_registry(fake_shared_access_key)

        iothub_registry_manager.create_device_with_sas(
            device_id=fake_device_id,
            primary_key=None,
            secondary_key=fake_secondary_key,
            status=fake_status,
        )

        assert_device_attributes_for_sas(
            mock_device_constructor, primary_key=None, secondary_key=fake_secondary_key
        )

    @pytest.mark.it(
        "calls 'create device' method from service operations with device id and previously constructed device"
    )
    def test_create_device_with_sas(self, mock_device_constructor, mock_service_operations):
        iothub_registry_manager = create_registry(fake_shared_access_key)

        iothub_registry_manager.create_device_with_sas(
            device_id=fake_device_id,
            primary_key=fake_primary_key,
            secondary_key=None,
            status=fake_status,
        )
        assert_device_creation(mock_service_operations, mock_device_constructor)


@pytest.mark.describe("IoTHubRegistryManager Create Device With X509")
class TestIoTHubRegistryManagerCreateDeviceWithX509(object):
    @pytest.mark.it(
        "initializes device with device id, status and self signed auth having primary thumbprint"
    )
    def test_initializes_device_with_kwargs_having_primary_thumbprint(
        self, mock_device_constructor, mock_service_operations
    ):
        iothub_registry_manager = create_registry(fake_shared_access_key)

        iothub_registry_manager.create_device_with_x509(
            device_id=fake_device_id,
            primary_thumbprint=fake_primary_thumbprint,
            secondary_thumbprint=None,
            status=fake_status,
        )
        assert_device_attributes_for_x509(
            mock_device_constructor,
            primary_thumbprint=fake_primary_thumbprint,
            secondary_thumbprint=None,
        )

    @pytest.mark.it(
        "initializes device with device id, status and self signed auth having secondary thumbprint"
    )
    def test_initializes_device_with_kwargs_having_secondary_thumbprint(
        self, mock_device_constructor, mock_service_operations
    ):
        iothub_registry_manager = create_registry(fake_shared_access_key)

        iothub_registry_manager.create_device_with_x509(
            device_id=fake_device_id,
            primary_thumbprint=None,
            secondary_thumbprint=fake_secondary_thumbprint,
            status=fake_status,
        )
        assert_device_attributes_for_x509(
            mock_device_constructor,
            primary_thumbprint=None,
            secondary_thumbprint=fake_secondary_thumbprint,
        )

    @pytest.mark.it(
        "calls 'create device' method from service operations with device id and previously constructed device"
    )
    def test_create_device_with_x509(self, mock_device_constructor, mock_service_operations):
        iothub_registry_manager = create_registry(fake_shared_access_key)

        iothub_registry_manager.create_device_with_x509(
            device_id=fake_device_id,
            primary_thumbprint=fake_primary_thumbprint,
            secondary_thumbprint=None,
            status=fake_status,
        )
        assert_device_creation(mock_service_operations, mock_device_constructor)


@pytest.mark.describe("IoTHubRegistryManager CreateDevice With CA")
class TestIoTHubRegistryManagerCreateDeviceWithCA(object):
    @pytest.mark.it("initializes device with device id, status and ca auth")
    def test_initializes_device_with_kwargs(self, mock_device_constructor, mock_service_operations):
        iothub_registry_manager = create_registry(fake_shared_access_key)

        iothub_registry_manager.create_device_with_certificate_authority(
            device_id=fake_device_id, status=fake_status
        )
        assert_device_attributes_for_ca(mock_device_constructor)

    @pytest.mark.it(
        "with certificate authority key calls create device service operations with device id, status and only ca auth"
    )
    def test_create_device_with_certificate_authority(
        self, mock_device_constructor, mock_service_operations
    ):
        iothub_registry_manager = create_registry(fake_shared_access_key)

        iothub_registry_manager.create_device_with_certificate_authority(
            device_id=fake_device_id, status=fake_status
        )

        assert_device_creation(mock_service_operations, mock_device_constructor)


@pytest.mark.skip("Skip")
@pytest.mark.describe("IoTHubRegistryManagerUpdateDevice")
class TestIoTHubRegistryManagerUpdateDevice(object):
    @pytest.mark.it(
        "with symmetric key calls device update service operations with device id, status and only sas auth with primary key"
    )
    def test_update_device_with_primary_sas(self, mock_service_operations):
        iothub_registry_manager = create_registry(fake_shared_access_key)
        device = iothub_registry_manager.update_device_with_sas(
            device_id=fake_device_id,
            etag=fake_etag,
            primary_key=fake_primary_key,
            secondary_key=None,
            status=fake_status,
        )
        assert device is not None

        assert_for_device_sas(
            mock_call=mock_service_operations,
            primary_key=fake_primary_key,
            secondary_key=None,
            device_status=fake_status,
            is_etag=True,
        )

    @pytest.mark.it(
        "with symmetric key calls device update service operations with device id, status and only sas auth with secondary key"
    )
    def test_update_device_with_secondary_sas(self, mock_service_operations):
        iothub_registry_manager = create_registry(fake_shared_access_key)
        device = iothub_registry_manager.update_device_with_sas(
            device_id=fake_device_id,
            etag=fake_etag,
            primary_key=None,
            secondary_key=fake_secondary_key,
            status=fake_status,
        )
        assert device is not None

        assert_for_device_sas(
            mock_call=mock_service_operations,
            primary_key=None,
            secondary_key=fake_secondary_key,
            device_status=fake_status,
            is_etag=True,
        )

    @pytest.mark.it(
        "with x509 key calls update device service operations with device id, status and only self signed auth with primary thumbprint"
    )
    def test_update_device_with_primary_x509(self, mock_service_operations):
        iothub_registry_manager = create_registry(fake_shared_access_key)

        device = iothub_registry_manager.update_device_with_x509(
            device_id=fake_device_id,
            etag=fake_etag,
            primary_thumbprint=fake_primary_thumbprint,
            secondary_thumbprint=None,
            status=fake_status,
        )
        assert device is not None

        assert_for_device_x509(
            mock_call=mock_service_operations,
            primary_thumbprint=fake_primary_thumbprint,
            secondary_thumbprint=None,
            device_status=fake_status,
            is_etag=True,
        )

    @pytest.mark.it(
        "with x509 key calls update device service operations with device id, status and only self signed auth with secondary thumbprint"
    )
    def test_update_device_with_secondary_x509(self, mock_service_operations):
        iothub_registry_manager = create_registry(fake_shared_access_key)

        device = iothub_registry_manager.update_device_with_x509(
            device_id=fake_device_id,
            etag=fake_etag,
            primary_thumbprint=None,
            secondary_thumbprint=fake_secondary_thumbprint,
            status=fake_status,
        )
        assert device is not None

        assert_for_device_x509(
            mock_call=mock_service_operations,
            primary_thumbprint=None,
            secondary_thumbprint=fake_secondary_thumbprint,
            device_status=fake_status,
            is_etag=True,
        )

    @pytest.mark.it(
        "with certificate authority key calls device update service operations with device id, status and only ca auth"
    )
    def test_update_device_with_certificate_authority(self, mocker):
        mock_service_operations_init = mocker.patch(
            "azure.iot.hub.protocol.iot_hub_gateway_service_ap_is20190630.ServiceOperations"
        )
        mock_service_operations = mock_service_operations_init.return_value

        iothub_registry_manager = create_registry(fake_shared_access_key)

        device = iothub_registry_manager.update_device_with_certificate_authority(
            device_id=fake_device_id, etag=fake_etag, status=fake_status
        )
        assert device is not None

        assert_for_device_ca(
            mock_call=mock_service_operations, device_status=fake_status, is_etag=True
        )


@pytest.mark.skip("Skip")
@pytest.mark.describe("IoTHubRegistryManagerCreateModulee")
class TestIoTHubRegistryManagerCreateModule(object):
    @pytest.mark.it(
        "with symmetric key calls create module service operations with device id, module_id , managed by and only sas auth with primary key"
    )
    def test_create_module_with_primary_sas(self, mock_service_operations):
        iothub_registry_manager = create_registry(fake_shared_access_key)

        module = iothub_registry_manager.create_module_with_sas(
            device_id=fake_device_id,
            module_id=fake_module_id,
            managed_by=fake_managed_by,
            primary_key=fake_primary_key,
            secondary_key=None,
            status=fake_status,
        )
        assert module is not None

        # assert_for_sas(mock_call=mock_service_operations, primary_key=fake_primary_key,
        #                secondary_key=None, device_status=fake_status)

        assert mock_service_operations.create_or_update_module.call_count == 1
        assert mock_service_operations.create_or_update_module.call_args[0][0] == fake_device_id
        assert mock_service_operations.create_or_update_module.call_args[0][1] == fake_module_id
        assert (
            mock_service_operations.create_or_update_module.call_args[0][2].authentication.type
            == "sas"
        )
        assert (
            mock_service_operations.create_or_update_module.call_args[0][
                2
            ].authentication.x509_thumbprint
            is None
        )
        assert (
            mock_service_operations.create_or_update_module.call_args[0][
                2
            ].authentication.symmetric_key
            is not None
        )
        assert (
            mock_service_operations.create_or_update_module.call_args[0][
                2
            ].authentication.symmetric_key.primary_key
            == fake_primary_key
        )
        assert (
            mock_service_operations.create_or_update_module.call_args[0][
                2
            ].authentication.symmetric_key.secondary_key
            is None
        )
        assert (
            mock_service_operations.create_or_update_module.call_args[0][2].managed_by
            == fake_managed_by
        )


"""
Asserts for devices created with Symmetric Key Authentication
"""


def assert_for_device_sas(
    mock_call, primary_key, secondary_key, device_status, is_etag=False, is_module=False
):

    # index = 1
    #     # if is_module:
    #     #     index = 2

    # fn = function("create_or_update_device")
    assert mock_call.create_or_update_device.call_count == 1
    assert callable(mock_call.create_or_update_device.call_args[0][0])

    assert mock_call.create_or_update_device.call_args[0][0] == fake_device_id
    assert mock_call.create_or_update_device.call_args[0][1].authentication.type == "sas"
    assert mock_call.create_or_update_device.call_args[0][1].authentication.x509_thumbprint is None
    assert (
        mock_call.create_or_update_device.call_args[0][1].authentication.symmetric_key is not None
    )
    assert (
        mock_call.create_or_update_device.call_args[0][1].authentication.symmetric_key.primary_key
        == primary_key
    )
    assert (
        mock_call.create_or_update_device.call_args[0][1].authentication.symmetric_key.secondary_key
        is secondary_key
    )
    assert mock_call.create_or_update_device.call_args[0][1].status == device_status

    if is_etag:
        assert mock_call.create_or_update_device.call_args[0][1].etag == fake_etag


"""
Asserts for devices created/updated with X509 Self Signed Authentication
"""


def assert_for_device_x509(
    mock_call, primary_thumbprint, secondary_thumbprint, device_status, is_etag=False
):
    assert mock_call.create_or_update_device.call_count == 1
    assert mock_call.create_or_update_device.call_args[0][0] == fake_device_id
    assert mock_call.create_or_update_device.call_args[0][1].authentication.type == "selfSigned"
    assert mock_call.create_or_update_device.call_args[0][1].authentication.symmetric_key is None

    assert (
        mock_call.create_or_update_device.call_args[0][
            1
        ].authentication.x509_thumbprint.primary_thumbprint
        == primary_thumbprint
    )
    assert (
        mock_call.create_or_update_device.call_args[0][
            1
        ].authentication.x509_thumbprint.secondary_thumbprint
        is secondary_thumbprint
    )
    assert mock_call.create_or_update_device.call_args[0][1].status == device_status

    if is_etag:
        assert mock_call.create_or_update_device.call_args[0][1].etag == fake_etag


"""
Asserts for devices created/updated with Certificate Authority Authentication
"""


def assert_for_device_ca(mock_call, device_status, is_etag=False):
    assert mock_call.create_or_update_device.call_count == 1
    assert mock_call.create_or_update_device.call_args[0][0] == fake_device_id
    assert (
        mock_call.create_or_update_device.call_args[0][1].authentication.type
        == "certificateAuthority"
    )
    assert mock_call.create_or_update_device.call_args[0][1].authentication.symmetric_key is None
    assert mock_call.create_or_update_device.call_args[0][1].authentication.x509_thumbprint is None
    assert mock_call.create_or_update_device.call_args[0][1].status == device_status

    if is_etag:
        assert mock_call.create_or_update_device.call_args[0][1].etag == fake_etag


def assert_device_attributes_for_sas(mock_device_constructor, primary_key, secondary_key):
    assert mock_device_constructor.call_count == 1
    assert mock_device_constructor.call_args[1]["device_id"] == fake_device_id
    assert mock_device_constructor.call_args[1]["status"] == fake_status
    assert isinstance(
        mock_device_constructor.call_args[1]["authentication"], AuthenticationMechanism
    )
    auth_mechanism = mock_device_constructor.call_args[1]["authentication"]
    assert auth_mechanism.type == "sas"
    assert auth_mechanism.x509_thumbprint is None
    sym_key = auth_mechanism.symmetric_key
    assert sym_key.primary_key == primary_key
    assert sym_key.secondary_key == secondary_key


def assert_device_attributes_for_x509(
    mock_device_constructor, primary_thumbprint, secondary_thumbprint
):
    assert mock_device_constructor.call_count == 1
    assert mock_device_constructor.call_args[1]["device_id"] == fake_device_id
    assert mock_device_constructor.call_args[1]["status"] == fake_status
    assert isinstance(
        mock_device_constructor.call_args[1]["authentication"], AuthenticationMechanism
    )
    auth_mechanism = mock_device_constructor.call_args[1]["authentication"]
    assert auth_mechanism.type == "selfSigned"
    assert auth_mechanism.symmetric_key is None
    x509_thumbprint = auth_mechanism.x509_thumbprint
    assert x509_thumbprint.primary_thumbprint == primary_thumbprint
    assert x509_thumbprint.secondary_thumbprint == secondary_thumbprint


def assert_device_attributes_for_ca(mock_device_constructor):
    assert mock_device_constructor.call_count == 1
    assert mock_device_constructor.call_args[1]["device_id"] == fake_device_id
    assert mock_device_constructor.call_args[1]["status"] == fake_status
    assert isinstance(
        mock_device_constructor.call_args[1]["authentication"], AuthenticationMechanism
    )
    auth_mechanism = mock_device_constructor.call_args[1]["authentication"]
    assert auth_mechanism.type == "certificateAuthority"
    assert auth_mechanism.x509_thumbprint is None
    assert auth_mechanism.symmetric_key is None


def assert_device_creation(service_call, device_constructor):
    assert service_call.create_or_update_device.call_count == 1
    assert service_call.create_or_update_device.call_args[0][0] == fake_device_id
    assert service_call.create_or_update_device.call_args[0][1] == device_constructor.return_value
