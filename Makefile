.PHONY: test
test:
	./PyMailStress.py -c 163.conf -u userdb.txt -m 1hr.conf

tags:
	etags *.py

.PHONY: clean
clean:
	rm -rf *.pyc
