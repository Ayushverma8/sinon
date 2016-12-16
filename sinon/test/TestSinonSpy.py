import sys
sys.path.insert(0, '../')

import unittest
import lib.SinonBase as sinon
from lib.SinonSpy import SinonSpy
from lib.SinonSandbox import sinontest

"""
======================================================
                 FOR TEST ONLY START
======================================================
"""
# build-in module
import os
# customized class
class A_object(object):
    # customized function
    def A_func(self):
        return "test_global_A_func"

# global function
def B_func(x=None):
    if x:
        return "test_local_B_func"+str(x)
    return "test_local_B_func"

def C_func(a="a", b="b", c="c"):
    return "test_local_C_func"

def D_func(err=False):
    if err:
        raise err
    else:
        return "test_local_D_func"
"""
======================================================
                 FOR TEST ONLY END
======================================================
"""

class TestSinonSpy(unittest.TestCase):

    def setUp(self):
        sinon.init(globals())

    @sinontest
    def test040_called_method(self):
        spy = SinonSpy(B_func)
        sinon.g.B_func()
        self.assertTrue(spy.called)

    @sinontest
    def test041_calledOnce_method(self):
        spy = SinonSpy(B_func)
        sinon.g.B_func()
        self.assertTrue(spy.calledOnce)

    @sinontest
    def test042_calledTwice_method(self):
        spy = SinonSpy(B_func)
        sinon.g.B_func()
        sinon.g.B_func()
        self.assertTrue(spy.calledTwice)

    @sinontest
    def test043_calledThrice_method(self):
        spy = SinonSpy(B_func)
        sinon.g.B_func()
        sinon.g.B_func()
        sinon.g.B_func()
        self.assertTrue(spy.calledThrice)

    @sinontest
    def test044_calledOnce_module_method(self):
        spy = SinonSpy(os, "system")
        os.system("cd")
        self.assertTrue(spy.calledOnce)

    @sinontest
    def test045_calledTwice_module_method(self):
        spy = SinonSpy(os, "system")
        os.system("cd")
        os.system("cd")
        self.assertTrue(spy.calledTwice)

    @sinontest
    def test046_calledThrice_module_method(self):
        spy = SinonSpy(os, "system")
        os.system("cd")
        os.system("cd")
        os.system("cd")
        self.assertTrue(spy.calledThrice)

    @sinontest
    def test047_calledOnce_empty(self):
        spy = SinonSpy()
        spy()
        self.assertTrue(spy.calledOnce)

    @sinontest
    def test048_calledTwice_empty(self):
        spy = SinonSpy()
        spy()
        spy()
        self.assertTrue(spy.calledTwice)

    @sinontest
    def test049_calledThrice_empty(self):
        spy = SinonSpy()
        spy()
        spy()
        spy()
        self.assertTrue(spy.calledThrice)

    @sinontest
    def test050_firstCall_secondCall_thirdCall_lastCall(self):
        spy1 = SinonSpy(os, "system")
        spy2 = SinonSpy()
        spy3 = SinonSpy(B_func)
        spy4 = SinonSpy()
        os.system("cd")
        spy2()
        sinon.g.B_func()
        spy4()
        self.assertTrue(spy1.firstCall)
        self.assertTrue(spy2.secondCall)
        self.assertTrue(spy3.thirdCall)
        self.assertTrue(spy4.lastCall)
 
    @sinontest
    def test051_calledBefore_calledAfter_normal(self):
        spy1 = SinonSpy(os, "system")
        spy2 = SinonSpy()
        spy3 = SinonSpy(B_func)
        os.system("cd")
        spy2()
        sinon.g.B_func()
        self.assertTrue(spy1.calledBefore(spy2))
        self.assertTrue(spy1.calledBefore(spy3))
        self.assertTrue(spy2.calledBefore(spy3))
        self.assertTrue(spy2.calledAfter(spy1))
        self.assertTrue(spy3.calledAfter(spy1))
        self.assertTrue(spy3.calledAfter(spy2))

    @sinontest
    def test052_calledBefore_nothing_called(self):
        spy1 = SinonSpy(os, "system")
        spy2 = SinonSpy()
        spy3 = SinonSpy(B_func)
        exception = "_getCallQueueIndex(): the call queue is empty"
        with self.assertRaises(Exception) as context:
            self.assertFalse(spy1.calledBefore(spy2))
        self.assertTrue(exception in str(context.exception))
        with self.assertRaises(Exception) as context:
            self.assertFalse(spy2.calledAfter(spy1))
        self.assertTrue(exception in str(context.exception))
 
    @sinontest
    def test053_calledBefore_calledAfter_recalled_method(self):
        spy1 = SinonSpy(os, "system")
        spy2 = SinonSpy()
        os.system("cd")
        spy2()
        os.system("cd")
        self.assertTrue(spy1.calledBefore(spy2))
        self.assertTrue(spy1.calledAfter(spy2))
        self.assertTrue(spy2.calledBefore(spy1))
        self.assertTrue(spy2.calledAfter(spy1))

    @sinontest
    def test054_calledBefore_calledAfter_called_restore_recalled(self):
        spy1 = SinonSpy(os, "system")
        spy2 = SinonSpy()
        os.system("cd")
        spy1.restore()
        spy1 = SinonSpy(os, "system")
        spy2()
        os.system("cd")
        self.assertTrue(spy1.calledAfter(spy2))
        self.assertTrue(spy2.calledBefore(spy1))

    @sinontest
    def test070_calledWith_method_fullmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(spy.calledWith(a="a", b="b", c="c"))
        self.assertFalse(spy.calledWith(a="wrong", b="b", c="c"))
        #pure args
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(spy.calledWith("a", "b", "c"))
        self.assertFalse(spy.calledWith("a", "wrong", "c"))
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        self.assertTrue(spy.calledWith("a", b="b", c="c"))
        self.assertTrue(spy.calledWith("a", "b", c="c"))
        self.assertTrue(spy.calledWith("a", "b", "c"))
        self.assertFalse(spy.calledWith("a", "b", "d"))
        self.assertFalse(spy.calledWith("a", "b", c="d"))

    @sinontest
    def test071_calledWith_method_partialmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertFalse(spy.calledWith(a="wrong"))
        self.assertTrue(spy.calledWith(a="a"))
        self.assertTrue(spy.calledWith(b="b"))
        self.assertTrue(spy.calledWith(c="c"))
        self.assertFalse(spy.calledWith(a="wrong", b="b"))
        self.assertTrue(spy.calledWith(a="a", b="b"))
        self.assertTrue(spy.calledWith(b="b", c="c"))
        self.assertTrue(spy.calledWith(a="a", c="c"))
        #pure args
        sinon.g.C_func("a", "b", "c")
        self.assertFalse(spy.calledWith("d"))
        self.assertTrue(spy.calledWith("a"))
        self.assertTrue(spy.calledWith("b"))
        self.assertTrue(spy.calledWith("c"))
        self.assertFalse(spy.calledWith("wrong", "b"))
        self.assertTrue(spy.calledWith("a", "b"))
        self.assertTrue(spy.calledWith("b", "c"))
        self.assertTrue(spy.calledWith("a", "c"))
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        self.assertTrue(spy.calledWith("a", b="b"))
        self.assertTrue(spy.calledWith("a", c="c"))
        self.assertTrue(spy.calledWith(b="b", c="c"))
        self.assertTrue(spy.calledWith("a"))
        self.assertTrue(spy.calledWith(c="c"))
        self.assertFalse(spy.calledWith("wrong", b="b"))
        self.assertFalse(spy.calledWith("a", b="wrong"))
        self.assertFalse(spy.calledWith("a", c="wrong"))

    @sinontest
    def test072_alwaysCalledWith_method_fullmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(spy.alwaysCalledWith(a="a", b="b", c="c"))
        sinon.g.C_func(a="d", b="e", c="f")
        self.assertFalse(spy.alwaysCalledWith(a="a", b="b", c="c"))
        spy.restore()
        spy = SinonSpy(C_func)
        #pure args
        sinon.g.C_func("a", "b", "c")
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(spy.alwaysCalledWith("a", "b", "c"))
        sinon.g.C_func("d", "e", "f")
        self.assertFalse(spy.alwaysCalledWith("a", "b", "c"))
        spy.restore()
        spy = SinonSpy(C_func)
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        sinon.g.C_func("a", b="b", c="c")
        self.assertTrue(spy.alwaysCalledWith("a", b="b", c="c"))
        sinon.g.C_func("b", b="b", c="c")
        self.assertFalse(spy.alwaysCalledWith("a", b="b", c="c"))
        spy.restore()

    @sinontest
    def test073_alwaysCalledWith_method_partialmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        sinon.g.C_func(a="xxxx", b="b", c="c")
        self.assertTrue(spy.alwaysCalledWith(b="b", c="c"))
        sinon.g.C_func(a="d", b="e", c="f")
        self.assertFalse(spy.alwaysCalledWith(b="b", c="c"))
        spy.restore()
        spy = SinonSpy(C_func)
        #pure args
        sinon.g.C_func("a", "b", "c")
        sinon.g.C_func("a", "b", "xxxx")
        self.assertTrue(spy.alwaysCalledWith("a", "b"))
        sinon.g.C_func("d", "e", "f")
        self.assertFalse(spy.alwaysCalledWith("a", "b"))
        spy.restore()
        spy = SinonSpy(C_func)
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        sinon.g.C_func("a", b="b")
        self.assertTrue(spy.alwaysCalledWith("a", b="b"))
        sinon.g.C_func("b", b="b", c="c")
        self.assertFalse(spy.alwaysCalledWith("a", b="b"))
        spy.restore()

    @sinontest
    def test074_calledWithExactly_method_fullmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(spy.calledWithExactly(a="a", b="b", c="c"))
        self.assertFalse(spy.calledWithExactly(a="d", b="e", c="f"))
        #pure args
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(spy.calledWithExactly("a", "b", "c"))
        self.assertFalse(spy.calledWithExactly("d", "e", "f"))
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        self.assertTrue(spy.calledWithExactly("a", b="b", c="c"))
        self.assertFalse(spy.calledWithExactly("wrong", b="b", c="c"))

    @sinontest
    def test075_calledWithExactly_method_partialmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertFalse(spy.calledWithExactly(a="a", b="b"))
        #pure args
        sinon.g.C_func("a", "b", "c")
        self.assertFalse(spy.calledWithExactly("a", "b"))
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        self.assertFalse(spy.calledWithExactly("a", b="b"))

    @sinontest
    def test076_alwaysCalledWithExactly_method_fullmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(spy.alwaysCalledWithExactly(a="a", b="b", c="c"))
        sinon.g.C_func(a="d", b="e", c="f")
        self.assertFalse(spy.alwaysCalledWithExactly(a="a", b="b", c="c"))
        spy.restore()
        spy = SinonSpy(C_func)
        #pure args
        sinon.g.C_func("a", "b", "c")
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(spy.alwaysCalledWithExactly("a", "b", "c"))
        sinon.g.C_func("d", "e", "f")
        self.assertFalse(spy.alwaysCalledWithExactly("a", "b", "c"))
        spy.restore()
        spy = SinonSpy(C_func)
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        sinon.g.C_func("a", b="b", c="c")
        self.assertTrue(spy.alwaysCalledWithExactly("a", b="b", c="c"))
        sinon.g.C_func("b", b="b", c="c")
        self.assertFalse(spy.alwaysCalledWithExactly("a", b="b", c="c"))
        spy.restore()

    @sinontest
    def test077_alwaysCalledWithExactly_method_partialmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(spy.alwaysCalledWithExactly(a="a", b="b", c="c"))
        sinon.g.C_func(a="xxxx", b="b", c="c")
        self.assertFalse(spy.alwaysCalledWithExactly(b="b", c="c"))
        spy.restore()
        spy = SinonSpy(C_func)
        #pure args
        sinon.g.C_func("a", "b", "c")
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(spy.alwaysCalledWithExactly("a", "b", "c"))
        sinon.g.C_func("a", "b", "xxxx")
        self.assertFalse(spy.alwaysCalledWithExactly("a", "b"))
        spy.restore()
        spy = SinonSpy(C_func)
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        sinon.g.C_func("a", b="b", c="c")
        self.assertTrue(spy.alwaysCalledWithExactly("a", b="b", c="c"))
        sinon.g.C_func("a", b="b", c="xxx")
        self.assertFalse(spy.alwaysCalledWithExactly("a", b="b"))
        spy.restore()

    @sinontest
    def test078_neverCalledWith_method_fullmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertFalse(spy.neverCalledWith(a="a", b="b", c="c"))
        self.assertTrue(spy.neverCalledWith(a="wrong", b="b", c="c"))
        #pure args
        sinon.g.C_func("a", "b", "c")
        self.assertFalse(spy.neverCalledWith("a", "b", "c"))
        self.assertTrue(spy.neverCalledWith("a", "wrong", "c"))
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        self.assertFalse(spy.neverCalledWith("a", b="b", c="c"))
        self.assertFalse(spy.neverCalledWith("a", "b", c="c"))
        self.assertFalse(spy.neverCalledWith("a", "b", "c"))
        self.assertTrue(spy.neverCalledWith("a", "b", "d"))
        self.assertTrue(spy.neverCalledWith("a", "b", c="d"))

    @sinontest
    def test079_neverCalledWith_method_partialmatch(self):
        spy = SinonSpy(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(spy.neverCalledWith(a="wrong"))
        self.assertFalse(spy.neverCalledWith(a="a"))
        self.assertFalse(spy.neverCalledWith(b="b"))
        self.assertFalse(spy.neverCalledWith(c="c"))
        self.assertTrue(spy.neverCalledWith(a="wrong", b="b"))
        self.assertFalse(spy.neverCalledWith(a="a", b="b"))
        self.assertFalse(spy.neverCalledWith(b="b", c="c"))
        self.assertFalse(spy.neverCalledWith(a="a", c="c"))
        #pure args
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(spy.neverCalledWith("d"))
        self.assertFalse(spy.neverCalledWith("a"))
        self.assertFalse(spy.neverCalledWith("b"))
        self.assertFalse(spy.neverCalledWith("c"))
        self.assertTrue(spy.neverCalledWith("wrong", "b"))
        self.assertFalse(spy.neverCalledWith("a", "b"))
        self.assertFalse(spy.neverCalledWith("b", "c"))
        self.assertFalse(spy.neverCalledWith("a", "c"))
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        self.assertFalse(spy.neverCalledWith("a", b="b"))
        self.assertFalse(spy.neverCalledWith("a", c="c"))
        self.assertFalse(spy.neverCalledWith(b="b", c="c"))
        self.assertFalse(spy.neverCalledWith("a"))
        self.assertFalse(spy.neverCalledWith(c="c"))
        self.assertTrue(spy.neverCalledWith("wrong", b="b"))
        self.assertTrue(spy.neverCalledWith("a", b="wrong"))
        self.assertTrue(spy.neverCalledWith("a", c="wrong"))

    @sinontest
    def test090_threw_without_err(self):
        spy = SinonSpy(D_func)
        sinon.g.D_func(err=False)
        self.assertFalse(spy.threw()) 

    @sinontest
    def test091_threw_with_err(self):
        class MyException(Exception):
            pass

        spy = SinonSpy(D_func)

        try:
            sinon.g.D_func(err=MyException)
        except:
            pass
        self.assertTrue(spy.threw()) 
        self.assertTrue(spy.threw(MyException))
        self.assertFalse(spy.threw(ValueError))

        try:
            sinon.g.D_func(err=ValueError)
        except:
            pass
        self.assertTrue(spy.threw(ValueError))

    @sinontest
    def test092_alwaysThrew_without_err(self):
        spy = SinonSpy(D_func)
        sinon.g.D_func(err=False)
        sinon.g.D_func(err=False)
        self.assertFalse(spy.alwaysThrew()) 

    @sinontest
    def test093_alwaysThrew_with_same_err(self):
        class MyException(Exception):
            pass

        spy = SinonSpy(D_func)

        try:
            sinon.g.D_func(err=MyException)
            sinon.g.D_func(err=MyException)
        except:
            pass
        self.assertTrue(spy.alwaysThrew()) 
        self.assertTrue(spy.alwaysThrew(MyException))

        try:
            sinon.g.D_func(err=ValueError)
        except:
            pass
        self.assertFalse(spy.alwaysThrew(MyException))

    @sinontest
    def test100_returned(self):
        spy = SinonSpy(B_func)
        sinon.g.B_func()
        self.assertTrue(spy.returned("test_local_B_func"))
        sinon.g.B_func(2)
        self.assertTrue(spy.returned("test_local_B_func2"))

    @sinontest
    def test101_returned_exception(self):
        # exception will return a empty function with no return
        spy = SinonSpy(D_func)

        try:
            sinon.g.D_func(err=ValueError)
        except:
            pass
        self.assertFalse(spy.returned("test_local_D_func"))
        sinon.g.D_func()
        self.assertTrue(spy.returned("test_local_D_func"))

    @sinontest
    def test102_alwaysReturned(self):
        spy = SinonSpy(B_func)
        sinon.g.B_func()
        sinon.g.B_func()
        self.assertTrue(spy.alwaysReturned("test_local_B_func"))
        sinon.g.B_func(123)
        self.assertFalse(spy.alwaysReturned("test_local_B_func"))

    @sinontest
    def test110_getCall(self):
        spy1 = SinonSpy(B_func)
        spy2 = SinonSpy(C_func)
        sinon.g.B_func()
        call = SinonSpy.getCall(0)
        self.assertFalse(spy2.called)  #C_func is never called
        self.assertTrue(call.called)    #B_func is called

    @sinontest
    def test111_getCall_wrongIndex(self):
        exception = "The call queue only contains 0 calls"
        with self.assertRaises(Exception) as context:
            SinonSpy.getCall(100)
        self.assertTrue(exception in str(context.exception))

    @sinontest
    def test120_kwargs(self):
        spy = SinonSpy(C_func)
        self.assertEqual(spy.kwargs, [])
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertEqual(spy.kwargs, [{"a":"a", "b":"b", "c":"c"}])
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertEqual(spy.kwargs, [{"a":"a", "b":"b", "c":"c"}, {"a":"a", "b":"b", "c":"c"}])
        sinon.g.C_func("a", b="b", c="c")
        self.assertEqual(spy.kwargs, [{"a":"a", "b":"b", "c":"c"}, {"a":"a", "b":"b", "c":"c"}, {"b": "b", "c": "c"}])

    @sinontest
    def test121_args(self):
        spy = SinonSpy(C_func)
        self.assertEqual(spy.args, [])
        sinon.g.C_func("a", "b", "c")
        self.assertEqual(spy.args, [("a", "b", "c")])
        sinon.g.C_func("a", "b", "c")
        self.assertEqual(spy.args, [("a", "b", "c"), ("a", "b", "c")])
        sinon.g.C_func("a", b="b", c="c")
        self.assertEqual(spy.args, [("a", "b", "c"), ("a", "b", "c"), ("a",)])

    @sinontest
    def test122_exceptions(self):
        spy = SinonSpy(D_func)
        self.assertEqual(spy.exceptions, [])

        try:
            sinon.g.D_func(ValueError)
        except:
            pass
        self.assertEqual(spy.exceptions, [ValueError])

        try:
            sinon.g.D_func(TypeError)
        except:
            pass
        self.assertEqual(spy.exceptions, [ValueError, TypeError])

    @sinontest
    def test123_returnValues(self):
        spy = SinonSpy(B_func)
        self.assertEqual(spy.exceptions, [])
        sinon.g.B_func()
        self.assertEqual(spy.returnValues, ["test_local_B_func"])
        sinon.g.B_func(2)
        self.assertEqual(spy.returnValues, ["test_local_B_func", "test_local_B_func2"])

    @sinontest
    def test130_reset(self):
        spy = SinonSpy(B_func)
        sinon.g.B_func(2)
        self.assertTrue(spy.called)
        self.assertTrue(spy.args)
        spy.reset()
        self.assertFalse(spy.called)
        self.assertFalse(spy.args)

    @sinontest
    def test140_spy_as_callback(self):
        def func(f):
            f()
        spy = SinonSpy()
        func(spy) 
        self.assertTrue(spy.called)      
        self.assertTrue(spy.calledOnce)

    @sinontest
    def test141_spy_as_callback_withargs(self):
        def func(f):
            f(1)
        spy = SinonSpy()
        func(spy) 
        self.assertTrue(spy.calledWith(1))
