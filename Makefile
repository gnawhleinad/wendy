all: clean test

clean: 
	vagrant destroy --force

.PHONY: test
test: 
	vagrant up && \
	vagrant ssh --command 'sudo su jenkins -c \
	  "temp=$$(mktemp --directory) && \
	   rsync --recursive --exclude='.*' /vagrant/* $$temp && \
	   cd $$temp && \
	   nosetests --verbose"'
