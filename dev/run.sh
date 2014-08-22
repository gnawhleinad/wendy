#!/bin/bash

start=${1:-false}
restart=${2:-false}

sudo mkdir -p /var/lib/jenkins/plugins

wget https://updates.jenkins-ci.org/latest/jquery.hpi
wget https://updates.jenkins-ci.org/latest/simple-theme-plugin.hpi
wget https://updates.jenkins-ci.org/latest/scm-api.hpi
wget https://updates.jenkins-ci.org/latest/git-client.hpi
wget https://updates.jenkins-ci.org/latest/git.hpi
sudo mv *.hpi /var/lib/jenkins/plugins

touch known_hosts && ssh-keyscan -H github.com >> known_hosts && sudo chown root:root known_hosts && sudo mv known_hosts /root/.ssh

sudo mkdir -p /var/lib/jenkins/userContent

(cd /var/lib/jenkins/userContent && sudo git clone https://github.com/kevinburke/doony.git)
(cd /var/lib/jenkins/userContent/doony && sudo git checkout 1.6)
touch org.codefirst.SimpleTheeDecorator.xml
cat > org.codefirst.SimpleThemeDecorator.xml << CAN_WE_FIX_IT
<org.codefirst.SimpleThemeDecorator plugin="simple-theme-plugin@0.3">
  <cssUrl>http://localhost:8080/userContent/doony/doony.css</cssUrl>
  <jsUrl>http://localhost:8080/userContent/doony/doony.js</jsUrl>
</org.codefirst.SimpleThemeDecorator>
CAN_WE_FIX_IT
sudo mv org.codefirst.SimpleThemeDecorator.xml /var/lib/jenkins

if $start; then
	chown -R jenkins:jenkins /var/lib/jenkins
	exec su jenkins -c "java -Dhudson.diyChunking=false -jar /usr/share/jenkins/jenkins.war"
fi

if $restart; then
	sudo service jenkins restart
fi
