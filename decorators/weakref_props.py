import weakref


def weakref_props(*properties):
    """A class decorator to assign properties that hold weakrefs to objects.

    This decorator will not overwrite existing attributes and methods.

    Parameters
    ----------
    properties : list of str
        A list of property attributes to assign to weakrefs.

    Examples
    --------
    >>> @weakref_props('a', 'b')
    ... class Test(object):
    ...     pass
    >>> test = Test()
    >>> test2 = Test()
    >>> test.a = test2
    >>> test.b = Test()
    >>> test.c = 1
    >>> sorted(test.__dict__.keys())
    ['_a', '_b', 'c']
    >>> test.a == test2
    True
    >>> test.b is None  # Dead link
    True
    >>> test.c == 1
    True
    >>> del test.a
    >>> test.a is None
    True
    """
    def func(cls):
        def property_func(attr):
            def _set_attr(self, value):
                name = '_' + attr if not attr.startswith('_') else attr
                setattr(self, name, weakref.ref(value))

            def _get_attr(self):
                name = '_' + attr if not attr.startswith('_') else attr
                value = getattr(self, name, None)
                return value() if value is not None else None

            def _del_attr(self):
                name = '_' + attr if not attr.startswith('_') else attr
                delattr(self, name)

            docstr = "A weakref to the object stored in '{}'".format(attr)

            return _get_attr, _set_attr, _del_attr, docstr

        for prop in properties:
            if hasattr(cls, prop):
                continue
            fget, fset, fdel, docstr = property_func(prop)
            setattr(cls, prop, property(fget=fget, fset=fset, fdel=fdel,
                                        doc=docstr))

        return cls

    return func
