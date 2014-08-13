#!/bin/bash

mkdir -p /var/lib/jenkins/plugins

wget https://updates.jenkins-ci.org/latest/jquery.hpi
wget https://updates.jenkins-ci.org/latest/simple-theme-plugin.hpi
wget https://updates.jenkins-ci.org/latest/scm-api.hpi
wget https://updates.jenkins-ci.org/latest/git-client.hpi
wget https://updates.jenkins-ci.org/latest/git.hpi
mv *.hpi /var/lib/jenkins/plugins

touch known_hosts && ssh-keyscan -H github.com >> known_hosts && chown root:root known_hosts && mv known_hosts /root/.ssh

mkdir -p /var/lib/jenkins/userContent

cd /var/lib/jenkins/userContent && git clone https://github.com/kevinburke/doony.git && cd -
cd /var/lib/jenkins/userContent/doony && git checkout 1.6 && cd -
touch org.codefirst.SimpleTheeDecorator.xml
cat > org.codefirst.SimpleThemeDecorator.xml << CAN_WE_FIX_IT
<org.codefirst.SimpleThemeDecorator plugin="simple-theme-plugin@0.3">
  <cssUrl>http://localhost:8080/userContent/doony/doony.css</cssUrl>
  <jsUrl>http://localhost:8080/userContent/doony/doony.js</jsUrl>
</org.codefirst.SimpleThemeDecorator>
CAN_WE_FIX_IT
mv org.codefirst.SimpleThemeDecorator.xml /var/lib/jenkins

chown -R jenkins:jenkins /var/lib/jenkins

exec su jenkins -c "java -jar /usr/share/jenkins/jenkins.war"
