import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../')

from decorators import weakref_props


def test_weakref_props():
    """Test the weakref_props decorations."""
    # Create test classes

    # attributes 'a' and 'b' contain weakrefs to objects
    @weakref_props('a', 'b')
    class Test(object):
        pass

    @weakref_props('b', 'c')
    class SubTest(Test):
        pass

    # Create a class from the base Test class
    test1 = Test()
    test2 = Test()

    test1.a = test2
    test1.b = Test()
    test1.c = 1

    assert all(i in test1.__dict__ for i in ['_a', '_b'])

    assert test1.a == test2
    assert test1.b is None  # Dead link
    assert test1.c == 1

    # Try removing an object
    del test2
    assert test1.b is None  # Dead link

    # Now try with the subclass
    subtest1 = SubTest()
    subtest2 = SubTest()

    subtest1.a = subtest2
    subtest1.b = SubTest()
    subtest1.c = subtest2

    assert all(i in subtest1.__dict__ for i in ['_a', '_b', '_c'])

    assert subtest1.a == subtest2
    assert subtest1.b is None  # Dead link
    assert subtest1.c == subtest2

    del subtest2
    assert subtest1.a is None
    assert subtest1.c is None
