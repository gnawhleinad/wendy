all: clean test

clean: 
	vagrant destroy --force

.PHONY: test
test: 
	vagrant up && \
	vagrant ssh --command \
	  'temp=$$(mktemp --directory) && \
	   rsync --recursive --exclude=".*" /vagrant/* $$temp && \
	   sudo chgrp --recursive vagrant /var/lib/jenkins && \
	   sudo chmod --recursive g+w /var/lib/jenkins && \
	   cd $$temp && \
	   nosetests --verbose'
