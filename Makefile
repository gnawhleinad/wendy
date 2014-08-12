all: clean test

clean: 
	vagrant destroy --force

.PHONY: test
test: 
	vagrant up && \
	vagrant ssh --command \
	  'temp=$$(mktemp --directory) && \
	   rsync --recursive --exclude=".*" /vagrant/* $$temp && \
	   cd $$temp && \
	   sudo chown --recursive jenkins:jenkins $$temp && \
	   sudo -E su jenkins --command "nosetests --verbose"'
