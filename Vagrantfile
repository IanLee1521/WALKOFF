# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    # config.vm.box = "ubuntu/xenial64"  # -- Ubuntu 16.04
    config.vm.box = "ubuntu/bionic64"  # -- Ubuntu 18.04

    config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"

    config.vm.provider "virtualbox" do |vb|
        vb.cpus = 2
        vb.memory = 4096
    end

    # Force synced_folder to be via rsync. If NFS, WALKOFF won't start properly
    config.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__exclude: ".git/"

    config.vm.provision "shell", inline: <<-SHELL
        apt-get update
        apt-get install -y git npm python python-pip

        # From: https://nsacyber.github.io/WALKOFF/tutorials/build/Install_Tutorial.html
        cd /vagrant

        python setup_walkoff.py

        python walkoff.py --host 0.0.0.0 --port 5000
    SHELL
end
