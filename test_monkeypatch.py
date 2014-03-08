# encoding: utf-8
"""
test_monkeypatch.py
TODO: Description

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://sam.zoy.org/wtfpl/COPYING for more details.
"""
import sys
from monkeypatch import PyString_Type

def strslash(self, other):
	return self + '/' + other

# Let's verify that this normally causes an error.
foo = 'foo'
Hello = 'Hello'
try:
	print foo / 'bar'
except:
	print 'Error occured when attempting: "print foo / \'bar\'":', sys.exc_info()[0]


# Patch over the __div__ method for the builtin string type.
PyString_Type.patch('__div__', strslash)

# And try our 
print Hello / 'World' / foo / 'bar'

# Unpatch our builtin type.
PyString_Type.unpatch('__div__')

# Due to a misunderstanding I had at the time of writing this, executing the following line after you have unpatched
# PyString_Type will result in a crash.
# print foo / 'bar'

print 'All done.'

