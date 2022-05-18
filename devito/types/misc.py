from ctypes import c_int, c_double, c_void_p

import numpy as np

from devito.types import CompositeObject, Indexed, Symbol
from devito.types.basic import IndexedData
from devito.tools import Pickable, as_tuple

__all__ = ['Timer', 'Pointer', 'VolatileInt', 'c_volatile_int',
           'c_volatile_int_p', 'FIndexed', 'Wildcard', 'Global', 'Hyperplane']


class Timer(CompositeObject):

    def __init__(self, name, sections):
        super().__init__(name, 'profiler', [(i, c_double) for i in sections])

    def reset(self):
        for i in self.fields:
            setattr(self.value._obj, i, 0.0)
        return self.value

    @property
    def total(self):
        return sum(getattr(self.value._obj, i) for i in self.fields)

    @property
    def sections(self):
        return self.fields

    def _arg_values(self, **kwargs):
        values = super()._arg_values(**kwargs)

        # Reset timer
        for i in self.fields:
            setattr(values[self.name]._obj, i, 0.0)

        return values

    # Pickling support
    _pickle_args = ['name', 'sections']


class VolatileInt(Symbol):

    @property
    def _C_typedata(self):
        return 'volatile int'

    _C_typename = _C_typedata

    @property
    def _C_ctype(self):
        return c_volatile_int


class Wildcard(Symbol):

    """
    A special Symbol used by the compiler to generate ad-hoc code
    (e.g. to work around known bugs in jit-compilers).
    """

    pass


class FIndexed(Indexed, Pickable):

    """
    A flatten Indexed with functional (primary) and indexed (secondary) representations.

    Examples
    --------
    Consider the Indexed `u[x, y]`. The corresponding FIndexed's functional representation
    is `u(x, y)`. This is a multidimensional representation, just like any other Indexed.
    The corresponding indexed (secondary) represenation is instead flatten, that is
    `uX[x*ny + y]`, where `X` is a string provided by the caller.
    """

    def __new__(cls, indexed, pname, strides=None):
        plabel = Symbol(name=pname, dtype=indexed.dtype)
        base = IndexedData(plabel, shape=indexed.shape, function=indexed.function)
        obj = super().__new__(cls, base, *indexed.indices)

        obj.indexed = indexed
        obj.pname = pname
        obj.strides = as_tuple(strides)

        return obj

    def __repr__(self):
        return "%s(%s)" % (self.name, ", ".join(str(i) for i in self.indices))

    __str__ = __repr__

    def _hashable_content(self):
        return super()._hashable_content() + (self.strides,)

    @property
    def name(self):
        return self.function.name

    @property
    def free_symbols(self):
        # The functional representation of the FIndexed "hides" the strides, which
        # are however actual free symbols of the object, since they contribute to
        # the address calculation just like all other free_symbols
        return (super().free_symbols |
                set().union(*[i.free_symbols for i in self.strides]))

    # Pickling support
    _pickle_args = ['indexed', 'pname']
    _pickle_kwargs = ['strides']
    __reduce_ex__ = Pickable.__reduce_ex__


class Global(Symbol):

    """
    A special Symbol representing global variables.
    """

    pass


class Hyperplane(tuple):

    """
    A collection of Dimensions defining an hyperplane.
    """

    @property
    def _defines(self):
        return frozenset().union(*[i._defines for i in self])


class Pointer(Symbol):

    @property
    def _C_typename(self):
        return '%s*' % super()._C_typename

    @property
    def _C_ctype(self):
        # Treat `np.void` as a special case since numpy, which doesn't manage
        # pointers, wouldn't know how to translate it into a ctype with its
        # internal dtype-to-ctype machinery
        if self.dtype is np.void:
            return c_void_p
        return super()._C_ctype


# ctypes subtypes

class c_volatile_int(c_int):
    pass


class c_volatile_int_p(c_void_p):
    pass
