# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "wendy-dev"

  config.vm.provider "virtualbox" do |v, override|
    v.gui = false
    v.customize ["modifyvm", :id, "--memory", 512]
    v.customize ["modifyvm", :id, "--cpus", 1]
  end

  config.vm.network :forwarded_port, guest: 8080, host: 8080

  $script = <<SCRIPT
touch /home/vagrant/.bash_aliases && echo "alias python=python3" > /home/vagrant/.bash_aliases
sudo apt-get update && sudo apt-get install -y python3-pip
sudo pip3 install nose

wget -q -O - http://pkg.jenkins-ci.org/debian-stable/jenkins-ci.org.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins-ci.org/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update && sudo apt-get install -y jenkins

wget https://updates.jenkins-ci.org/latest/jquery.hpi
wget https://updates.jenkins-ci.org/latest/simple-theme-plugin.hpi
wget https://updates.jenkins-ci.org/latest/scm-api.hpi
wget https://updates.jenkins-ci.org/latest/git-client.hpi
wget https://updates.jenkins-ci.org/latest/git.hpi
sudo mv *.hpi /var/lib/jenkins/plugins

sudo apt-get install -y git
touch known_hosts && ssh-keyscan -H github.com >> known_hosts && sudo chown root:root known_hosts && sudo mv known_hosts /root/.ssh

cd /var/lib/jenkins/userContent && sudo git clone https://github.com/kevinburke/doony.git && cd -
cd /var/lib/jenkins/userContent/doony && sudo git checkout 1.6 && cd -
touch org.codefirst.SimpleThemeDecorator.xml
cat > org.codefirst.SimpleThemeDecorator.xml << CAN_WE_FIX_IT
<org.codefirst.SimpleThemeDecorator plugin="simple-theme-plugin@0.3">
  <cssUrl>http://localhost:8080/userContent/doony/doony.css</cssUrl>
  <jsUrl>http://localhost:8080/userContent/doony/doony.js</jsUrl>
</org.codefirst.SimpleThemeDecorator>
CAN_WE_FIX_IT
sudo chown jenkins:jenkins org.codefirst.SimpleThemeDecorator.xml
sudo mv org.codefirst.SimpleThemeDecorator.xml /var/lib/jenkins

sudo service jenkins restart
SCRIPT

  config.vm.provision "shell", inline: $script
end
