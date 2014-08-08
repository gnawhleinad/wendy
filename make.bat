@echo off

if "%1" == "test" (
	vagrant up && vagrant ssh --command "sudo su jenkins -c 'temp=$(mktemp --directory) && rsync --recursive --exclude=".*" /vagrant/* $temp && cd $temp && chmod 644 test/*.py && nosetests --verbose'"
	if errorlevel 1 exit /b 1
	goto end
)

if "%1" == "clean" (
	vagrant destroy --force
	if errorlevel 1 exit /b 1
	goto end
)

:end
