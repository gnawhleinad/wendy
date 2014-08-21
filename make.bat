@echo off

if "%1" == "test" (
	vagrant up && vagrant ssh --command "temp=$(mktemp --directory) && rsync --recursive --exclude='.*' /vagrant/* $temp && chmod 644 $temp/test/*.py && cd $temp && nosetests --verbose"
	if errorlevel 1 exit /b 1
	goto end
)

if "%1" == "clean" (
	vagrant destroy --force
	if errorlevel 1 exit /b 1
	goto end
)

:end
