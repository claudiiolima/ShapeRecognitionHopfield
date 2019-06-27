import builtins as _mod_builtins
import numpy as _mod_numpy
import numpy.linalg as _mod_numpy_linalg

LinAlgError = _mod_numpy_linalg.LinAlgError
__builtins__ = {}
__doc__ = None
__file__ = '/home/claudio/.local/lib/python3.7/site-packages/scipy/linalg/_solve_toeplitz.cpython-37m-x86_64-linux-gnu.so'
__name__ = 'scipy.linalg._solve_toeplitz'
__package__ = 'scipy.linalg'
def __pyx_unpickle_Enum():
    pass

__test__ = _mod_builtins.dict()
def asarray(a, dtype, order):
    "Convert the input to an array.\n\n    Parameters\n    ----------\n    a : array_like\n        Input data, in any form that can be converted to an array.  This\n        includes lists, lists of tuples, tuples, tuples of tuples, tuples\n        of lists and ndarrays.\n    dtype : data-type, optional\n        By default, the data-type is inferred from the input data.\n    order : {'C', 'F'}, optional\n        Whether to use row-major (C-style) or\n        column-major (Fortran-style) memory representation.\n        Defaults to 'C'.\n\n    Returns\n    -------\n    out : ndarray\n        Array interpretation of `a`.  No copy is performed if the input\n        is already an ndarray with matching dtype and order.  If `a` is a\n        subclass of ndarray, a base class ndarray is returned.\n\n    See Also\n    --------\n    asanyarray : Similar function which passes through subclasses.\n    ascontiguousarray : Convert input to a contiguous array.\n    asfarray : Convert input to a floating point ndarray.\n    asfortranarray : Convert input to an ndarray with column-major\n                     memory order.\n    asarray_chkfinite : Similar function which checks input for NaNs and Infs.\n    fromiter : Create an array from an iterator.\n    fromfunction : Construct an array by executing a function on grid\n                   positions.\n\n    Examples\n    --------\n    Convert a list into an array:\n\n    >>> a = [1, 2]\n    >>> np.asarray(a)\n    array([1, 2])\n\n    Existing arrays are not copied:\n\n    >>> a = np.array([1, 2])\n    >>> np.asarray(a) is a\n    True\n\n    If `dtype` is set, array is copied only if dtype does not match:\n\n    >>> a = np.array([1, 2], dtype=np.float32)\n    >>> np.asarray(a, dtype=np.float32) is a\n    True\n    >>> np.asarray(a, dtype=np.float64) is a\n    False\n\n    Contrary to `asanyarray`, ndarray subclasses are not passed through:\n\n    >>> issubclass(np.recarray, np.ndarray)\n    True\n    >>> a = np.array([(1.0, 2), (3.0, 4)], dtype='f4,i4').view(np.recarray)\n    >>> np.asarray(a) is a\n    False\n    >>> np.asanyarray(a) is a\n    True\n\n    "
    pass

complex128 = _mod_numpy.complex128
float64 = _mod_numpy.float64
def levinson(a, b):
    'Solve a linear Toeplitz system using Levinson recursion.\n\n    Parameters\n    ----------\n    a : array, dtype=double or complex128, shape=(2n-1,)\n        The first column of the matrix in reverse order (without the diagonal)\n        followed by the first (see below)\n    b : array, dtype=double  or complex128, shape=(n,)\n        The right hand side vector. Both a and b must have the same type\n        (double or complex128).\n\n    Notes\n    -----\n    For example, the 5x5 toeplitz matrix below should be represented as\n    the linear array ``a`` on the right ::\n\n        [ a0    a1   a2  a3  a4 ]\n        [ a-1   a0   a1  a2  a3 ]\n        [ a-2  a-1   a0  a1  a2 ] -> [a-4  a-3  a-2  a-1  a0  a1  a2  a3  a4]\n        [ a-3  a-2  a-1  a0  a1 ]\n        [ a-4  a-3  a-2  a-1 a0 ]\n\n    Returns\n    -------\n    x : arrray, shape=(n,)\n        The solution vector\n    reflection_coeff : array, shape=(n+1,)\n        Toeplitz reflection coefficients. When a is symmetric Toeplitz and\n        ``b`` is ``a[n:]``, as in the solution of autoregressive systems,\n        then ``reflection_coeff`` also correspond to the partial\n        autocorrelation function.\n    '
    pass

def zeros(shape, dtype=float, order='C'):
    "zeros(shape, dtype=float, order='C')\n\n    Return a new array of given shape and type, filled with zeros.\n\n    Parameters\n    ----------\n    shape : int or tuple of ints\n        Shape of the new array, e.g., ``(2, 3)`` or ``2``.\n    dtype : data-type, optional\n        The desired data-type for the array, e.g., `numpy.int8`.  Default is\n        `numpy.float64`.\n    order : {'C', 'F'}, optional, default: 'C'\n        Whether to store multi-dimensional data in row-major\n        (C-style) or column-major (Fortran-style) order in\n        memory.\n\n    Returns\n    -------\n    out : ndarray\n        Array of zeros with the given shape, dtype, and order.\n\n    See Also\n    --------\n    zeros_like : Return an array of zeros with shape and type of input.\n    empty : Return a new uninitialized array.\n    ones : Return a new array setting values to one.\n    full : Return a new array of given shape filled with value.\n\n    Examples\n    --------\n    >>> np.zeros(5)\n    array([ 0.,  0.,  0.,  0.,  0.])\n\n    >>> np.zeros((5,), dtype=int)\n    array([0, 0, 0, 0, 0])\n\n    >>> np.zeros((2, 1))\n    array([[ 0.],\n           [ 0.]])\n\n    >>> s = (2,2)\n    >>> np.zeros(s)\n    array([[ 0.,  0.],\n           [ 0.,  0.]])\n\n    >>> np.zeros((2,), dtype=[('x', 'i4'), ('y', 'i4')]) # custom dtype\n    array([(0, 0), (0, 0)],\n          dtype=[('x', '<i4'), ('y', '<i4')])"
    pass

