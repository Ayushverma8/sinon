import sys
sys.path.insert(0, '../')

import unittest
import lib.sinon.SinonBase as sinon
from lib.sinon.SinonMock import SinonMock
from lib.sinon.SinonSandbox import sinontest

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

from TestClass import ForTestOnly
"""
======================================================
                 FOR TEST ONLY END
======================================================
"""

class TestSinonMock(unittest.TestCase):

    @sinontest
    def test001_constructor_inside_module(self):
        mock = SinonMock(A_object)
        expectation = mock.expects("A_func") 
        self.assertTrue(expectation.never())

    @sinontest
    def test002_constructor_outside_module(self):
        mock = SinonMock(ForTestOnly)

    @sinontest
    def test003_constructor_function(self):
        mock = SinonMock(B_func)

    @sinontest
    def test004_constructor_empty(self):
        mock = SinonMock()

    @sinontest
    def test005_constructor_instance(self):
        fto = ForTestOnly()
        mock = SinonMock(fto)

    @sinontest
    def test006_constructor_redeclare_module(self):
        mock = SinonMock(A_object)
        mock = SinonMock(A_object) #nothing will happen

    @sinontest
    def test007_constructor_redeclare_function(self):
        mock = SinonMock(A_object)
        exp1 = mock.expects("A_func")
        exception = "[{}] have already been declared".format("A_func")
        with self.assertRaises(Exception) as context:
            exp2 = mock.expects("A_func")
        self.assertTrue(exception in str(context.exception))