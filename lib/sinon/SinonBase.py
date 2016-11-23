import sys
sys.path.insert(0, '../')

import weakref
import inspect
from copy import deepcopy
from types import ModuleType, FunctionType

from lib.sinon.util import ErrorHandler, Wrapper, CollectionHandler

global LOCK
LOCK = "__SINONLOCK__"

class SinonGlobals(object):
    pass

def init(target_globals):
    global g
    g = SinonGlobals()
    funcs = [obj for obj in target_globals.values() if isinstance(obj, FunctionType)]
    for func in funcs:
        setattr(g, func.__name__, func)

class SinonBase(object):

    _queue = []

    def __new__(self, obj=None, prop=None):
        new = super(SinonBase, self).__new__(self)
        new.__init__(obj, prop)
        self._queue.append(new)
        return weakref.proxy(new)

    
    def restore(self):
        self.delWrap()
        self._queue.remove(self)


    def __init__(self, obj=None, prop=None):
        if not hasattr(self, "args_type"):
            self.setType(obj, prop)
            self.obj, self.prop = obj, prop
            self.checkLock()
            self.addWrap()
            self.pure_count = 0


    def setType(self, obj, prop):
        # pure
        if not prop and not obj:
            self.args_type = "PURE"

        # object
        if obj and (isinstance(obj, ModuleType) or inspect.isclass(obj) or isinstance(obj, FunctionType)):
            if isinstance(obj, ModuleType) or inspect.isclass(obj):
                self.args_type = "MODULE"
            elif isinstance(obj, FunctionType):
                self.args_type = "FUNCTION"
                self.orig_func = None
        elif obj:
            if hasattr(obj, "__class__"): #handle instance as class
                obj = obj.__class__
                self.args_type = "MODULE"
            else:
                ErrorHandler.objTypeError(obj) 

        # property
        if prop and (isinstance(prop, str) or isinstance(prop, unicode)):
            if prop in dir(obj):
                self.args_type = "MODULE_FUNCTION"
                self.orig_func = None
            else:
                ErrorHandler.propInObjError(obj, prop)
        elif prop:
            ErrorHandler.propTypeError(prop)


    def checkLock(self):
        if self.args_type == "MODULE_FUNCTION":
            if hasattr(self.obj, LOCK):
                ErrorHandler.lockError(self.obj.__name__)
            if hasattr(getattr(self.obj, self.prop), "callCount"):
                ErrorHandler.lockError(self.prop)
        elif self.args_type == "MODULE":
            if hasattr(self.obj, LOCK):
                ErrorHandler.lockError(self.obj.__name__)
        elif self.args_type == "FUNCTION":
            if hasattr(getattr(g, self.obj.__name__), "callCount"):
                ErrorHandler.lockError(self.obj.__name__)
        elif self.args_type == "PURE":
            pass

    def addWrap(self):
        if self.args_type == "MODULE_FUNCTION":
            self.orig_func = deepcopy(getattr(self.obj, self.prop))
            setattr(self.obj, self.prop, Wrapper.wrap(getattr(self.obj, self.prop)))
        elif self.args_type == "MODULE":
            setattr(self.obj, LOCK, True)
            #for key, value in self.obj.__dict__.items():
            #   if hasattr(value, '__call__'):
            #       setattr(self.obj, key, Wrapper.wrap(value))
        elif self.args_type == "FUNCTION":
            self.orig_func = deepcopy(getattr(g, self.obj.__name__))
            setattr(g, self.obj.__name__, Wrapper.wrap(getattr(g, self.obj.__name__)))
        elif self.args_type == "PURE":
            pass


    def delWrap(self):
        if self.args_type == "MODULE_FUNCTION":
            Wrapper.CALLQUEUE = [f for f in Wrapper.CALLQUEUE if f != getattr(self.obj, self.prop)]
            setattr(self.obj, self.prop, self.orig_func)
        elif self.args_type == "MODULE":
            Wrapper.CALLQUEUE = [f for f in Wrapper.CALLQUEUE if f != self]
            delattr(self.obj, LOCK)
        elif self.args_type == "FUNCTION":
            Wrapper.CALLQUEUE = [f for f in Wrapper.CALLQUEUE if f != getattr(g, self.obj.__name__)]
            setattr(g, self.obj.__name__, self.orig_func)
        elif self.args_type == "PURE":
            Wrapper.CALLQUEUE = [f for f in Wrapper.CALLQUEUE if f != self]

    def __call__(self):
        Wrapper.CALLQUEUE.append(self)
        self.pure_count = self.pure_count + 1

    def _args_list(self):
        if self.args_type == "MODULE_FUNCTION":
            return getattr(self.obj, self.prop).args_list
        elif self.args_type == "MODULE":
            pass
        elif self.args_type == "FUNCTION":
            return getattr(g, self.obj.__name__).args_list
        elif self.args_type == "PURE":
            pass

    def _kwargs_list(self):
        if self.args_type == "MODULE_FUNCTION":
            return getattr(self.obj, self.prop).kwargs_list
        elif self.args_type == "MODULE":
            pass
        elif self.args_type == "FUNCTION":
            return getattr(g, self.obj.__name__).kwargs_list
        elif self.args_type == "PURE":
            pass

    def _error_list(self): 
        if self.args_type == "MODULE_FUNCTION":
            return getattr(self.obj, self.prop).error_list
        elif self.args_type == "MODULE":
            pass
        elif self.args_type == "FUNCTION":
            return getattr(g, self.obj.__name__).error_list
        elif self.args_type == "PURE":
            pass

    def _ret_list(self):
        if self.args_type == "MODULE_FUNCTION":
            return getattr(self.obj, self.prop).ret_list
        elif self.args_type == "MODULE":
            pass
        elif self.args_type == "FUNCTION":
            return getattr(g, self.obj.__name__).ret_list
        elif self.args_type == "PURE":
            pass


    def _getCallQueueIndex(self):
        if self.args_type == "MODULE_FUNCTION":
            return [idx for idx, val in enumerate(Wrapper.CALLQUEUE) if val == getattr(self.obj, self.prop)]
        elif self.args_type == "MODULE":
            return [idx for idx, val in enumerate(Wrapper.CALLQUEUE) if val == self]
        elif self.args_type == "FUNCTION":
            return [idx for idx, val in enumerate(Wrapper.CALLQUEUE) if val == getattr(g, self.obj.__name__)]
        elif self.args_type == "PURE":
            return [idx for idx, val in enumerate(Wrapper.CALLQUEUE) if val == self]

    @property
    def callCount(self):
        if self.args_type == "MODULE_FUNCTION":
            return getattr(self.obj, self.prop).callCount
        elif self.args_type == "MODULE":
            return self.pure_count
        elif self.args_type == "FUNCTION":
            return getattr(g, self.obj.__name__).callCount
        elif self.args_type == "PURE":
            return self.pure_count
