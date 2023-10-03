from gi.repository.GLib import GError
from . import bluezutils as utils

from time import sleep


class Bluetooth(object):

    def __init__(self):
        self._adapter = utils.find_adapter()
        self._devices = utils.get_managed_objects()
        self._scan_thread = None

    def start_scan(self):
        try:
            self._adapter.StartDiscovery()
            return True
        except GError:
            return False

    def stop_scan(self):
        try:
            self._adapter.StopDiscovery()
            while self._adapter.Discovering:
                sleep(0.1)
            self._devices = utils.get_managed_objects()
            return True
        except GError:
            return False

    def get_available_devices(self):
        available_devices = self._get_devices("Available")
        return available_devices

    def get_paired_devices(self):
        paired_devices = self._get_devices("Paired")
        return paired_devices

    def get_connected_devices(self):
        connected_devices = self._get_devices("Connected")
        return connected_devices

    def _get_devices(self, condition):
        try:
            for path, iFaces in self._devices.items():
                if (dev := iFaces.get(utils.DEVICE_INTERFACE)) is not None:
                    if condition == "Available" or condition in dev and dev[condition]:
                        if (addr := dev.get("Address")) is not None and (device := utils.get_device(path)) is not None:
                            yield addr, BluetoothDevice(device, addr)
        except GError as error:
            print(error)
            pass

    def make_discoverable(self, value=True, timeout=180):
        try:
            timeout = int(timeout)
            value = int(value)

            if int(self._adapter.DiscoverableTimeout) != timeout:
                self._adapter.DiscoverableTimeout = timeout
            if int(self._adapter.Discoverable) != value:
                self._adapter.Discoverable = value
            return True
        except GError:
            return False

    def set_adapter_property(self, prop, value):
        try:
            setattr(self._adapter, prop, value)
            return True
        except GError:
            return False

    def get_adapter_property(self, prop):
        try:
            return getattr(self._adapter, prop)
        except GError:
            return None


class BluetoothDevice:
    def __init__(self, device=None, mac=None):
        if device is None and mac is None:
            raise ValueError("device or mac must be provided")
        self._device = device if device else utils.find_device(mac)

    def get_property(self, prop):
        try:
            return getattr(self._device, prop)
        except GError:
            return None

    def call(self, method, timeout=5000):
        fn = self.get_property(method)
        try:
            fn(timeout=timeout / 1000)
            return True
        except GError:
            return False

    @property
    def address(self):
        return self.get_property("Address")

    @property
    def name(self):
        return self.get_property("Name")

    @property
    def dev_class(self):
        return self.get_property("Class")

    @property
    def connected(self):
        return self.get_property("Connected")

    def connect(self, timeout=None):
        return self.call("Connect", timeout)

    def disconnect(self, timeout=None):
        return self.call("Disconnect", timeout)
