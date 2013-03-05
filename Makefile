.PHONY: test tags clean

test:
	./main.py -c etc/163.conf -u etc/userdb.txt -m etc/model.conf

tags:
	etags *.py

clean:
	rm -rf *.pyc
