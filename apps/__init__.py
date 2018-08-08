import logging

from walkoff.executiondb.device import get_app as get_db_app
from apps.messaging import *
from walkoff.appgateway.console import ConsoleLoggingHandler
import dill

from walkoff.cache import make_cache
import walkoff.config

from walkoff.appgateway.decorators import *

_logger = logging.getLogger(__name__)
_console_handler = ConsoleLoggingHandler()
_logger.setLevel(logging.DEBUG)
_logger.addHandler(_console_handler)

_reserved_fields = [
        'app',
        'app_name',
        'device',
        'device_fields',
        'device_type',
        'device_id',
        'context',
        '_cache',
        '__cache_separator'
        '_is_walkoff_app',
    ]


class App(object):
    """Base class for apps
    Attributes:
        app (apps.devicedb.App): The ORM of the App with the name passed into the constructor
        device (apps.devicedb.Device): The ORM of the device with the ID passed into teh constructor
        device_fields (dict): A dict of the plaintext fields of the device
        device_type (str): The type of device associated with self.device
    Args:
        app (str): The name of the app
        device (int): The ID of the device
    """

    _is_walkoff_app = True
    __cache_separator = ':'

    def __init__(self, app, device, context):
        self.app_name = app
        self.app = get_db_app(app)
        self.device = self.app.get_device(device) if (self.app is not None and device) else None
        if self.device is not None:
            self.device_fields = self.device.get_plaintext_fields()
            self.device_type = self.device.type
        else:
            self.device_fields = {}
            self.device_type = None
        self.device_id = device
        self.context = context
        self._cache = make_cache(walkoff.config.Config.CACHE)

    def _format_cache_key(self, field_name):
        return self.__cache_separator.join(
            [str(self.context['workflow_execution_id']), self.app_name, str(self.device_id), field_name]
        )

    def _get_field_pattern(self, context=None):
        if context is None:
            context = self.context
        return self.__cache_separator.join(
            [str(context['workflow_execution_id']), self.app_name, str(self.device_id), '*']
        )

    def get_all_devices(self):
        """Gets all the devices associated with this app
        Returns:
            list: A list of apps.appdevice.Device objects associated with this app
        """
        return list(self.app.devices) if self.app is not None else []

    def _reset_context(self, new_context):
        self.context = new_context
        key_pattern = self._get_field_pattern(context=new_context)
        for key in self._cache.scan(key_pattern):
            value = dill.loads(self._cache.get(key))
            field = key.split('.')[-1]
            self.__dict__[field] = value

    def _clear_cache(self):
        for key in self._cache.scan(self._get_field_pattern()):
            self._cache.delete(key)

    def __getattr__(self, item):
        if item in _reserved_fields:
            return self.__dict__[item]
        else:
            obj = self._cache.get(self._format_cache_key(item))
            return dill.loads(obj)

    def __setattr__(self, key, value):
        if key in _reserved_fields:
            self.__dict__[key] = value
        else:
            value = dill.dumps(value)
            key = self._format_cache_key(key)
            self._cache.set(key, value)

    def shutdown(self):
        """When implemented, this method performs shutdown procedures for the app
        """
        pass
