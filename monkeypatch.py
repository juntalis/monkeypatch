# encoding: utf-8
"""
monkeypatch.py
Using ctypes to monkeypatch python builtin types at runtime.

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://sam.zoy.org/wtfpl/COPYING for more details.
"""
from ctypes import *
from ctypes import _Pointer
from collections import OrderedDict as odict

c_ptr = POINTER
c_int_p = c_ptr(c_int)
c_char_pp = c_ptr(c_char_p)
c_void_pp = c_ptr(c_void_p)
c_file_p = c_void_p
py_object_p = c_ptr(py_object)

Py_ssize_t = \
	hasattr(pythonapi, 'Py_InitModule4_64') \
		and c_int64 or c_int

Py_ssize_t_p = c_ptr(Py_ssize_t)

class MethodMapping(Structure):
	_fields_ = []

	@property
	def fieldnames(self):
		return [fieldname for fieldname, ignored in self._fields_]

unaryfunc = CFUNCTYPE(py_object, py_object)
binaryfunc = CFUNCTYPE(py_object, py_object, py_object)
ternaryfunc = CFUNCTYPE(py_object, py_object, py_object, py_object)
inquiry = CFUNCTYPE(c_int, py_object)
lenfunc = CFUNCTYPE(Py_ssize_t, py_object)
coercion = CFUNCTYPE(c_int, py_object_p, py_object_p)
ssizeargfunc = CFUNCTYPE(py_object, py_object, Py_ssize_t)
ssizessizeargfunc = CFUNCTYPE(py_object, py_object, Py_ssize_t, Py_ssize_t)
intobjargproc = CFUNCTYPE(c_int, py_object, c_int, py_object)
intintobjargproc = CFUNCTYPE(c_int, py_object, c_int, c_int, py_object)
ssizeobjargproc = CFUNCTYPE(c_int, py_object, Py_ssize_t, py_object)
ssizessizeobjargproc = CFUNCTYPE(c_int, py_object, Py_ssize_t, Py_ssize_t, py_object)
objobjargproc = CFUNCTYPE(c_int, py_object, py_object, py_object)
getreadbufferproc = CFUNCTYPE(c_int, py_object, c_int, c_void_pp)
getwritebufferproc = CFUNCTYPE(c_int, py_object, c_int, c_void_pp)
getsegcountproc = CFUNCTYPE(c_int, py_object, c_int_p)
getcharbufferproc = CFUNCTYPE(c_int, py_object, c_int, c_char_pp)
readbufferproc = CFUNCTYPE(Py_ssize_t, py_object, Py_ssize_t, c_void_pp)
writebufferproc = CFUNCTYPE(Py_ssize_t, py_object, Py_ssize_t, c_void_pp)
segcountproc = CFUNCTYPE(Py_ssize_t, py_object, Py_ssize_t_p)
charbufferproc = CFUNCTYPE(Py_ssize_t, py_object, Py_ssize_t, c_char_pp)

class Py_buffer(MethodMapping):
	"""
	c_void_p buf;
	 py_object obj;
	 Py_ssize_t len;
	 Py_ssize_t itemsize;
	 c_int readonly;
	 c_int ndim;
	 c_char_p format;
	 Py_ssize_t_p shape;
	 Py_ssize_t_p strides;
	 Py_ssize_t_p suboffsets;
	 Py_ssize_t smalltable[2];
	 c_void_p internal;
	"""
	_fields_ = [
		('buf', c_void_p),
		('obj', py_object),
		('len', Py_ssize_t),
		('itemsize', Py_ssize_t),
		('readonly', c_int),
		('ndim', c_int),
		('format', c_char_p),
		('shape', Py_ssize_t_p),
		('strides', Py_ssize_t_p),
		('suboffsets', Py_ssize_t_p),
		('smalltable', Py_ssize_t * 2),
		('internal', c_void_p),
	]

Py_buffer_p = c_ptr(Py_buffer)

getbufferproc = CFUNCTYPE(c_int, py_object, Py_buffer_p, c_int)
releasebufferproc = CFUNCTYPE(None, py_object, Py_buffer_p)
objobjproc = CFUNCTYPE(c_int, py_object, py_object)
visitproc = CFUNCTYPE(c_int, py_object, c_void_p)
traverseproc = CFUNCTYPE(c_int, py_object, visitproc, c_void_p)
freefunc = CFUNCTYPE(None, c_void_p)
destructor = CFUNCTYPE(None, py_object)
printfunc = CFUNCTYPE(c_int, py_object, c_file_p, c_int)
getattrfunc = CFUNCTYPE(py_object, py_object, c_char_p)
getattrofunc = CFUNCTYPE(py_object, py_object, py_object)
setattrfunc = CFUNCTYPE(c_int, py_object, c_char_p, py_object)
setattrofunc = CFUNCTYPE(c_int, py_object, py_object, py_object)
cmpfunc = CFUNCTYPE(c_int, py_object, py_object)
reprfunc = CFUNCTYPE(py_object, py_object)
hashfunc = CFUNCTYPE(c_long, py_object)
richcmpfunc = CFUNCTYPE(py_object, py_object, py_object, c_int)
getiterfunc = CFUNCTYPE(py_object, py_object)
iternextfunc = CFUNCTYPE(py_object, py_object)
descrgetfunc = CFUNCTYPE(py_object, py_object, py_object, py_object)
descrsetfunc = CFUNCTYPE(c_int, py_object, py_object, py_object)
initproc = CFUNCTYPE(c_int, py_object, py_object, py_object)

class PyNumberMethods(MethodMapping):
	"""
	binaryfunc nb_add;
	 binaryfunc nb_subtract;
	 binaryfunc nb_multiply;
	 binaryfunc nb_divide;
	 binaryfunc nb_remainder;
	 binaryfunc nb_divmod;
	 ternaryfunc nb_power;
	 unaryfunc nb_negative;
	 unaryfunc nb_positive;
	 unaryfunc nb_absolute;
	 inquiry nb_nonzero;
	 unaryfunc nb_invert;
	 binaryfunc nb_lshift;
	 binaryfunc nb_rshift;
	 binaryfunc nb_and;
	 binaryfunc nb_xor;
	 binaryfunc nb_or;
	 coercion nb_coerce;
	 unaryfunc nb_int;
	 unaryfunc nb_long;
	 unaryfunc nb_float;
	 unaryfunc nb_oct;
	 unaryfunc nb_hex;
	 binaryfunc nb_inplace_add;
	 binaryfunc nb_inplace_subtract;
	 binaryfunc nb_inplace_multiply;
	 binaryfunc nb_inplace_divide;
	 binaryfunc nb_inplace_remainder;
	 ternaryfunc nb_inplace_power;
	 binaryfunc nb_inplace_lshift;
	 binaryfunc nb_inplace_rshift;
	 binaryfunc nb_inplace_and;
	 binaryfunc nb_inplace_xor;
	 binaryfunc nb_inplace_or;
	 binaryfunc nb_floor_divide;
	 binaryfunc nb_true_divide;
	 binaryfunc nb_inplace_floor_divide;
	 binaryfunc nb_inplace_true_divide;
	 unaryfunc nb_index;
	"""
	_fields_ = [
		('nb_add', binaryfunc),
		('nb_subtract', binaryfunc),
		('nb_multiply', binaryfunc),
		('nb_divide', binaryfunc),
		('nb_remainder', binaryfunc),
		('nb_divmod', binaryfunc),
		('nb_power', ternaryfunc),
		('nb_negative', unaryfunc),
		('nb_positive', unaryfunc),
		('nb_absolute', unaryfunc),
		('nb_nonzero', inquiry),
		('nb_invert', unaryfunc),
		('nb_lshift', binaryfunc),
		('nb_rshift', binaryfunc),
		('nb_and', binaryfunc),
		('nb_xor', binaryfunc),
		('nb_or', binaryfunc),
		('nb_coerce', coercion),
		('nb_int', unaryfunc),
		('nb_long', unaryfunc),
		('nb_float', unaryfunc),
		('nb_oct', unaryfunc),
		('nb_hex', unaryfunc),

		# Added in release 2.0
		('nb_inplace_add', binaryfunc),
		('nb_inplace_subtract', binaryfunc),
		('nb_inplace_multiply', binaryfunc),
		('nb_inplace_divide', binaryfunc),
		('nb_inplace_remainder', binaryfunc),
		('nb_inplace_power', ternaryfunc),
		('nb_inplace_lshift', binaryfunc),
		('nb_inplace_rshift', binaryfunc),
		('nb_inplace_and', binaryfunc),
		('nb_inplace_xor', binaryfunc),
		('nb_inplace_or', binaryfunc),

		# Added in release 2.2
		('nb_floor_divide', binaryfunc),
		('nb_true_divide', binaryfunc),
		('nb_inplace_floor_divide', binaryfunc),
		('nb_inplace_true_divide', binaryfunc),

		# Added in release 2.5
		('nb_index', unaryfunc),
	]

PyNumberMethods_p = c_ptr(PyNumberMethods)

class PySequenceMethods(MethodMapping):
	"""
	lenfunc sq_length;
	 binaryfunc sq_concat;
	 ssizeargfunc sq_repeat;
	 ssizeargfunc sq_item;
	 ssizessizeargfunc sq_slice;
	 ssizeobjargproc sq_ass_item;
	 ssizessizeobjargproc sq_ass_slice;
	 objobjproc sq_contains;
	 binaryfunc sq_inplace_concat;
	 ssizeargfunc sq_inplace_repeat;
	"""
	_fields_ = [
		('sq_length', lenfunc),
		('sq_concat', binaryfunc),
		('sq_repeat', ssizeargfunc),
		('sq_item', ssizeargfunc),
		('sq_slice', ssizessizeargfunc),
		('sq_ass_item', ssizeobjargproc),
		('sq_ass_slice', ssizessizeobjargproc),
		('sq_contains', objobjproc),
		('sq_inplace_concat', binaryfunc),
		('sq_inplace_repeat', ssizeargfunc),
	]

PySequenceMethods_p = c_ptr(PySequenceMethods)

class PyMappingMethods(MethodMapping):
	"""
	lenfunc mp_length;
	 binaryfunc mp_subscript;
	 objobjargproc mp_ass_subscript;
	"""
	_fields_ = [
		('mp_length', lenfunc),
		('mp_subscript', binaryfunc),
		('mp_ass_subscript', objobjargproc),
	]

PyMappingMethods_p = c_ptr(PyMappingMethods)

class PyBufferProcs(MethodMapping):
	"""
	readbufferproc bf_getreadbuffer;
	 writebufferproc bf_getwritebuffer;
	 segcountproc bf_getsegcount;
	 charbufferproc bf_getcharbuffer;
	 getbufferproc bf_getbuffer;
	 releasebufferproc bf_releasebuffer;
	"""
	_fields_ = [
		('bf_getreadbuffer', readbufferproc),
		('bf_getwritebuffer', writebufferproc),
		('bf_getsegcount', segcountproc),
		('bf_getcharbuffer', charbufferproc),
		('bf_getbuffer', getbufferproc),
		('bf_releasebuffer', releasebufferproc),
	]

PyBufferProcs_p = c_ptr(PyBufferProcs)

# TODO: Fill in the rest of these.
cname_map = [
	('__name__', 'tp_name'),
	('__doc__', 'tp_doc'),
	('__new__', 'tp_new'),
	('__init__', 'tp_init'),
	('__del__', 'tp_del'),
	('__pos__', 'nb_positive'),
	('__neg__', 'nb_negative'),
	('__abs__', 'nb_absolute'),
	('__invert__', 'nb_invert'),
	('__add__', 'nb_add'),
	('__sub__', 'nb_subtract'),
	('__mul__', 'nb_multiply'),
	('__floordiv__', 'nb_floor_divide'),
	('__div__', 'nb_divide'),
	('__truediv__', 'nb_true_divide'),
	('__mod__', 'nb_remainder'),
	('__divmod__', 'nb_divmod'),
	('__pow__', 'nb_power'),
	('__lshift__', 'nb_lshift'),
	('__rshift__', 'nb_rshift'),
	('__and__', 'nb_and'),
	('__or__', 'nb_or'),
	('__xor__', 'nb_xor'),
	('__iadd__', 'nb_inplace_add'),
	('__isub__', 'nb_inplace_subtract'),
	('__imul__', 'nb_inplace_multiply'),
	('__ifloordiv__', 'nb_inplace_floor_divide'),
	('__idiv__', 'nb_inplace_divide'),
	('__itruediv__', 'nb_inplace_true_divide'),
	('__imod_', 'nb_inplace_remainder'),
	('__ipow__', 'nb_inplace_power'),
	('__ilshift__', 'nb_inplace_lshift'),
	('__irshift__', 'nb_inplace_rshift'),
	('__iand__', 'nb_inplace_and'),
	('__ior__', 'nb_inplace_or'),
	('__ixor__', 'nb_inplace_xor'),
	('__int__', 'nb_int'),
	('__long__', 'nb_long'),
	('__float__', 'nb_float'),
	('__oct__', 'nb_oct'),
	('__hex__', 'nb_hex'),
	('__index__', 'nb_index'),
	('__coerce__', 'nb_coerce'),
	('__str__', 'tp_str'),
	('__repr__', 'tp_repr'),
	('__hash__', 'tp_hash'),
	('__nonzero__', 'nb_nonzero'),
	('__getattr__', 'tp_getattr'),
	('__setattr__', 'tp_setattr'),
	('__len__', 'sq_length'),
	('__iter__', 'tp_iter'),
	('__contains__', 'sq_contains'),
	('__call__', 'tp_call'),
	('__cmp__', 'tp_richcompare'),
	#('__eq__', ''),
	#('__ne__', ''),
	#('__lt__', ''),
	#('__gt__', ''),
	#('__le__', ''),
	#('__ge__', ''),
	# ('__round__', ''),
	# ('__floor__', ''),
	# ('__ceil__', ''),
	# ('__trunc__', ''),
	# ('__complex__', ''),
	# ('__trunc__', ''),
	# ('__unicode__', ''),
	# ('__format__', ''),
	# ('__dir__', ''),
	# ('__sizeof__', ''),
	# ('__delattr__', ''),
	# ('__getattribute__', 'tp_getattro'),
	# ('__getitem__', ''),
	# ('__setitem__', ''),
	# ('__delitem__', ''),
	# ('__reversed__', ''),
	# ('__missing__', ''),
	# ('__instancecheck__', ''),
	# ('__subclasscheck__', ''),
	# ('__radd__', ''),
	# ('__rsub__', ''),
	# ('__rmul__', ''),
	# ('__rfloordiv__', ''),
	# ('__rdiv__', ''),
	# ('__rtruediv__', ''),
	# ('__rmod__', ''),
	# ('__rdivmod__', ''),
	# ('__rpow__', ''),
	# ('__rlshift__', ''),
	# ('__rrshift__', ''),
	# ('__rand__', ''),
	# ('__ror__', ''),
	# ('__rxor__', ''),
	# ('__enter__', ''),
	# ('__exit__', ''),
	# ('__get__', ''),
	# ('__set__', ''),
	# ('__delete__', ''),
	# ('__copy__', ''),
	# ('__deepcopy__', ''),
	# ('__getinitargs__', ''),
	# ('__getnewargs__', ''),
	# ('__getstate__', ''),
	# ('__setstate__', ''),
	# ('__reduce__', ''),
	# ('__reduce_ex__', '')
]


class _typeobject(Structure):
	"""

	"""
	_originals_ = None
	_dirty_ = []

	def _buildsetter(self, target, key):
		def genericsetter(value=None, unsetting=False):
			if unsetting:
				self._dirty_.remove(key)
				setattr(target, key, self._originals_.get(key))
			else:
				if key not in self._dirty_:
					self._dirty_.append(key)
				typ = type(getattr(target, key))
				setattr(target, key, typ(value))
		return genericsetter

	def _pyname2cname_setter(self, methodname):
		global cname_map
		if hasattr(self, methodname):
			return self._buildsetter(self, methodname)
		def fakesetter(attr,unused): raise AttributeError(attr)
		for pyname, cname in cname_map:
			if pyname != methodname: continue
			if cname.startswith('tp_'):
				return self._buildsetter(self, cname)
			elif cname.startswith('nb_'):
				return self._buildsetter(self.tp_as_number.contents, cname)
			elif cname.startswith('sq_'):
				return self._buildsetter(self.tp_as_sequence.contents, cname)
			elif cname.startswith('mp_'):
				return self._buildsetter(self.tp_as_mapping.contents, cname)
		return fakesetter

	def _backup_originals(self):
		self._originals_ = odict()
		for fieldname, fieldtype in self._fields_:
			original = getattr(self, fieldname)
			if isinstance(original, _Pointer) and issubclass(original._type_, MethodMapping):
				self._originals_[fieldname] = odict()
				# noinspection PyUnresolvedReferences
				for field in original.contents.fieldnames:
					self._originals_[field] = getattr(original.contents, field)
			else:
				self._originals_[fieldname] = original

	def patch(self, fieldname, newfield):
		if self._originals_ is None:
			self._backup_originals()
		setter = self._pyname2cname_setter(fieldname)
		setter(newfield)

	def unpatch(self, fieldname = None):
		if self._originals_ is None: return
		if fieldname is None:
			for name in self._objects:
				unsetter = self._pyname2cname_setter(name)
				unsetter(unsetting=True)
			self._dirty_ = []
		else:
			unsetter = self._pyname2cname_setter(fieldname)
			unsetter(unsetting=True)

_typeobject_p = c_ptr(_typeobject)

newfunc = CFUNCTYPE(py_object, _typeobject_p, py_object, py_object)
allocfunc = CFUNCTYPE(py_object, _typeobject_p, Py_ssize_t)

_typeobject._fields_ = [
	('ob_refcnt', Py_ssize_t),
	('ob_type', py_object),
	('ob_size', Py_ssize_t),
	('tp_name', c_char_p),
	('tp_basicsize', Py_ssize_t),
	('tp_itemsize', Py_ssize_t),
	('tp_dealloc', destructor),
	('tp_print', printfunc),
	('tp_getattr', getattrfunc),
	('tp_setattr', setattrfunc),
	('tp_compare', cmpfunc),
	('tp_repr', reprfunc),
	('tp_as_number', PyNumberMethods_p),
	('tp_as_sequence', PySequenceMethods_p),
	('tp_as_mapping', PyMappingMethods_p),
	('tp_hash', hashfunc),
	('tp_call', ternaryfunc),
	('tp_str', reprfunc),
	('tp_getattro', getattrofunc),
	('tp_setattro', setattrofunc),
	('tp_as_buffer', PyBufferProcs_p),
	('tp_flags', c_long),
	('tp_doc', c_char_p),
	('tp_traverse', traverseproc),
	('tp_clear', inquiry),
	('tp_richcompare', richcmpfunc),
	('tp_weaklistoffset', Py_ssize_t),
	('tp_iter', getiterfunc),
	('tp_iternext', iternextfunc),
	('tp_methods', c_void_p),
	('tp_members', c_void_p),
	('tp_getset', c_void_p),
	('tp_base', c_ptr(_typeobject)),
	('tp_dict', py_object),
	('tp_descr_get', descrgetfunc),
	('tp_descr_set', descrsetfunc),
	('tp_dictoffset', Py_ssize_t),
	('tp_init', initproc),
	('tp_alloc', allocfunc),
	('tp_new', newfunc),
	('tp_free', freefunc),
	('tp_is_gc', inquiry),
	('tp_bases', py_object),
	('tp_mro', py_object),
	('tp_cache', c_void_p),
	('tp_subclasses', c_void_p),
	('tp_weaklist', c_void_p),
	('tp_del', c_void_p),
	('tp_version_tag', c_void_p)
]

PyTypeObject = _typeobject

class PyHeapTypeObject(Structure):
	"""
	PyTypeObject ht_type;
	 PyNumberMethods as_number;
	 PyMappingMethods as_mapping;
	 PySequenceMethods as_sequence;
	 PyBufferProcs as_buffer;
	 py_object ht_name,_p ht_slots;
	"""
	_fields_ = [
		('ht_type', PyTypeObject),
		('as_number', PyNumberMethods),
		('as_mapping', PyMappingMethods),
		('as_sequence', PySequenceMethods),
		('as_buffer', PyBufferProcs),
	]

def pytyp_from(export):
	try:
		return PyTypeObject.in_dll(pythonapi, export)
	except:
		return None

PyBaseObject_Type = pytyp_from('PyBaseObject_Type')
PyBaseString_Type = pytyp_from('PyBaseString_Type')
PyBool_Type = pytyp_from('PyBool_Type')
PyBuffer_Type = pytyp_from('PyBuffer_Type')
PyByteArrayIter_Type = pytyp_from('PyByteArrayIter_Type')
PyByteArray_Type = pytyp_from('PyByteArray_Type')
PyCFunction_Type = pytyp_from('PyCFunction_Type')
PyCObject_Type = pytyp_from('PyCObject_Type')
PyCallIter_Type = pytyp_from('PyCallIter_Type')
PyCapsule_Type = pytyp_from('PyCapsule_Type')
PyCell_Type = pytyp_from('PyCell_Type')
PyClassMethod_Type = pytyp_from('PyClassMethod_Type')
PyCode_Type = pytyp_from('PyCode_Type')
PyComplex_Type = pytyp_from('PyComplex_Type')
PyDictItems_Type = pytyp_from('PyDictItems_Type')
PyDictIterItem_Type = pytyp_from('PyDictIterItem_Type')
PyDictIterKey_Type = pytyp_from('PyDictIterKey_Type')
PyDictIterValue_Type = pytyp_from('PyDictIterValue_Type')
PyDictKeys_Type = pytyp_from('PyDictKeys_Type')
PyDictProxy_Type = pytyp_from('PyDictProxy_Type')
PyDictValues_Type = pytyp_from('PyDictValues_Type')
PyDict_Type = pytyp_from('PyDict_Type')
PyEllipsis_Type = pytyp_from('PyEllipsis_Type')
PyEnum_Type = pytyp_from('PyEnum_Type')
PyFile_Type = pytyp_from('PyFile_Type')
PyFloat_Type = pytyp_from('PyFloat_Type')
PyFrame_Type = pytyp_from('PyFrame_Type')
PyFrozenSet_Type = pytyp_from('PyFrozenSet_Type')
PyFunction_Type = pytyp_from('PyFunction_Type')
PyGen_Type = pytyp_from('PyGen_Type')
PyGetSetDescr_Type = pytyp_from('PyGetSetDescr_Type')
PyInt_Type = pytyp_from('PyInt_Type')
PyList_Type = pytyp_from('PyList_Type')
PyLong_Type = pytyp_from('PyLong_Type')
PyMemberDescr_Type = pytyp_from('PyMemberDescr_Type')
PyMemoryView_Type = pytyp_from('PyMemoryView_Type')
PyModule_Type = pytyp_from('PyModule_Type')
PyNullImporter_Type = pytyp_from('PyNullImporter_Type')
PyProperty_Type = pytyp_from('PyProperty_Type')
PyRange_Type = pytyp_from('PyRange_Type')
PyReversed_Type = pytyp_from('PyReversed_Type')
PySTEntry_Type = pytyp_from('PySTEntry_Type')
PySeqIter_Type = pytyp_from('PySeqIter_Type')
PySet_Type = pytyp_from('PySet_Type')
PySlice_Type = pytyp_from('PySlice_Type')
PyStaticMethod_Type = pytyp_from('PyStaticMethod_Type')
PyString_Type = pytyp_from('PyString_Type')
PySuper_Type = pytyp_from('PySuper_Type')
PyTraceBack_Type = pytyp_from('PyTraceBack_Type')
PyTuple_Type = pytyp_from('PyTuple_Type')
PyType_Type = pytyp_from('PyType_Type')
PyUnicode_Type = pytyp_from('PyUnicode_Type')
PyWrapperDescr_Type = pytyp_from('PyWrapperDescr_Type')

mymod = locals()
notnone = lambda s: s in mymod and mymod[s] is not None
__all__ = filter(notnone, [
	'PyTypeObject',
	'PyHeapTypeObject',
	'pytyp_from',
	'PatchableBuiltin',

	# Exported Types
	'PyBool_Type',
	'PyBuffer_Type',
	'PyByteArray_Type',
	'PyByteArrayIter_Type',
	'PyCell_Type',
	'PyCObject_Type',
	'PyCode_Type',
	'PyComplex_Type',
	'PyWrapperDescr_Type',
	'PyDictProxy_Type',
	'PyGetSetDescr_Type',
	'PyMemberDescr_Type',
	'PyProperty_Type',
	'PyDict_Type',
	'PyDictIterKey_Type',
	'PyDictIterValue_Type',
	'PyDictIterItem_Type',
	'PyDictKeys_Type',
	'PyDictItems_Type',
	'PyDictValues_Type',
	'PyEnum_Type',
	'PyReversed_Type',
	'PyFile_Type',
	'PyFloat_Type',
	'PyFrame_Type',
	'PyFunction_Type',
	'PyClassMethod_Type',
	'PyStaticMethod_Type',
	'PyGen_Type',
	'PyNullImporter_Type',
	'PyInt_Type',
	'PySeqIter_Type',
	'PyCallIter_Type',
	'PyList_Type',
	'PyLong_Type',
	'PyMemoryView_Type',
	'PyCFunction_Type',
	'PyModule_Type',
	'PyType_Type',
	'PyBaseObject_Type',
	'PySuper_Type',
	'PyCapsule_Type',
	'PyRange_Type',
	'PySet_Type',
	'PyFrozenSet_Type',
	'PySlice_Type',
	'PyEllipsis_Type',
	'PyBaseString_Type',
	'PyString_Type',
	'PySTEntry_Type',
	'PyTraceBack_Type',
	'PyTuple_Type',
	'PyUnicode_Type'
])

