# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    #config.vm.box = "ubuntu/xenial64"  # -- Ubuntu 16.04
    config.vm.box = "ubuntu/bionic64"  # -- Ubuntu 18.04

    config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"

    config.vm.provider "virtualbox" do |vb|
        vb.cpus = 2
        vb.memory = 4096
    end

    config.vm.provision "shell", inline: <<-SHELL
        apt-get update
        apt-get install -y git npm python3-pip

        # From: https://nsacyber.github.io/WALKOFF/tutorials/build/Install_Tutorial.html
        cd /vagrant
        python3 setup_walkoff.py

        python3 walkoff.py
    SHELL
end
