# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "wendy-dev"

  config.vm.provider "virtualbox" do |v, override|
    v.gui = false
    v.customize ["modifyvm", :id, "--memory", 2048]
    v.customize ["modifyvm", :id, "--cpus", 1]
  end

  $script = <<SCRIPT
touch /home/vagrant/.bash_aliases && echo "alias python=python3" > /home/vagrant/.bash_aliases
sudo apt-get update -qq && sudo apt-get install -y python3-pip
sudo pip3 install nose
sudo apt-get update -qq && sudo apt-get install -y libxml2-dev libxslt1-dev lib32z1-dev && sudo pip3 install lxml

sudo apt-get update -qq && sudo apt-get install -y openjdk-7-jre-headless

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
sudo sh -c "echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"
sudo apt-get update -qq && sudo apt-get install -y lxc-docker && sudo pip3 install docker-py
sudo usermod -a -G docker vagrant && sudo su -l vagrant

(cd /vagrant/test/util && sudo docker build -t wendy/dev .)
mkdir -p /var/lib/jenkins
SCRIPT

  config.vm.provision "shell", inline: $script
end
