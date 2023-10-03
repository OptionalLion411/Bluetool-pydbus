from pydbus import SystemBus

SERVICE_NAME = "org.bluez"
MANAGER_INTERFACE = "org.freedesktop.DBus.ObjectManager"
ADAPTER_INTERFACE = SERVICE_NAME + ".Adapter1"
DEVICE_INTERFACE = SERVICE_NAME + ".Device1"


class BluezUtilError(Exception):
    pass


def get_managed_objects():
    bus = SystemBus()
    manager = bus.get(SERVICE_NAME, "/")[MANAGER_INTERFACE]
    return manager.GetManagedObjects()


def get_adapter(path):
    bus = SystemBus()
    return bus.get(SERVICE_NAME, path)[ADAPTER_INTERFACE]


def find_adapter(objects=get_managed_objects(), pattern=None):
    for path, iFaces in objects.items():
        if (adapter := iFaces.get(ADAPTER_INTERFACE)) is None:
            continue

        if not pattern or pattern == adapter["Address"] or path.endswith(pattern):
            return get_adapter(path)

    raise BluezUtilError("Bluetooth adapter not found")


def get_device(path):
    bus = SystemBus()
    try:
        return bus.get(SERVICE_NAME, path)[DEVICE_INTERFACE]
    except KeyError:
        return None


def find_device(device_address, objects=get_managed_objects(), adapter_pattern=None, adapter=None):
    path_prefix = ""

    if adapter_pattern:
        adapter = adapter if adapter else find_adapter(objects, adapter_pattern)
        path_prefix = adapter.object_path

    for path, iFaces in objects.items():
        if (device := iFaces.get(DEVICE_INTERFACE)) is None:
            continue

        if device["Address"] == device_address and path.startswith(path_prefix):
            return get_device(path)

    raise BluezUtilError("Bluetooth device not found")
