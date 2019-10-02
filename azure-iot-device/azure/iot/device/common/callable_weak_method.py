# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import weakref


class CallableWeakMethod(object):
    def __init__(self, object, method_name):
        self.object_weakref = weakref.ref(object)
        self.method_name = method_name

    def _get_method(self):
        return getattr(self.object_weakref(), self.method_name)

    def __call__(self, *args, **kwargs):
        return self._get_method()(*args, **kwargs)

    def __eq__(self, other):
        return self._get_method() == other

    def __repr__(self):
        if self.object_weakref():
            return "CallableWeakMethod for {}".format(self._get_method())
        else:
            return "CallableWeakMethod for {}".format(self.method_name)
