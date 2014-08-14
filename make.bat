@echo off

if "%1" == "test" (
	vagrant up && vagrant ssh --command "temp=$(mktemp --directory) && rsync --recursive --exclude='.*' /vagrant/* $temp && chmod 644 test/*.py && sudo chgrp --recursive vagrant /var/lib/jenkins && sudo chmod --recursive g+w /var/lib/jenkins && cd $temp && nosetests --verbose"
	if errorlevel 1 exit /b 1
	goto end
)

if "%1" == "clean" (
	vagrant destroy --force
	if errorlevel 1 exit /b 1
	goto end
)

:end
