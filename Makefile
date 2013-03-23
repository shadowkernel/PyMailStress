.PHONY: test tags clean

test:
	./main.py

tags:
	etags *.py

clean:
	rm -rf *.pyc lib/*.pyc
