## MonkeyPatch

Simple proof of concept using ctypes to monkeypatch class members on Python builtin types. Included is an example that patches the str type to make the following valid:

	python```
	>>> bar = 'bar'
	>>> print 'foo' / bar
	foo/bar
	```

There's a few issues that arise after you unpatch the built-in types. At the time of writing this, I had some misunderstandings of how ctypes implemented some of its functionality. (This has been sitting in my "sandbox" folder for ages now, so I don't see there being much hope that this will receive any further commits.)