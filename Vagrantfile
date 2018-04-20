Vagrant::DEFAULT_SERVER_URL.replace('https://vagrantcloud.com')
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

 #Multiple machine config

 config.vm.define "ansible", primary: true do |master|
    master.vm.box = "ubuntu/trusty64"
    master.vm.hostname = "master"
    master.vm.synced_folder ".","/ansible"
    master.vm.network "private_network", type: "dhcp"
    master.vm.network "public_network",use_dhcp_assigned_default_route: true
    master.vm.provision "shell", privileged: false, inline: <<-EOF
       set -e
       sudo apt-get update && sudo apt-get install -y \
         git \
         python-setuptools \
         python-dev \
         gcc \
         libffi-dev \
         libssl-dev 
       sudo apt-get install -y software-properties-common
       sudo apt-add-repository ppa:ansible/ansible
       sudo apt-get update
       sudo apt-get install -y ansible
       sudo useradd ansible -m
       echo "ansible\nansible\nansible" | sudo passwd ansible
       echo "cd /ansible" >> ~/.profile
     EOF
 end

 config.vm.define "Node_01" do |node1|
    node1.vm.box = "ubuntu/trusty64"
    node1.vm.hostname = "node1"
    node1.vm.network "private_network", type: "dhcp"
    node1.vm.provision "shell", privileged: false, inline: <<-EOF
       set -e
       sudo useradd ansible -m
       echo "ansible\nansible\nansible" | sudo passwd ansible
    EOF
 end

 config.vm.define "Node_02" do |node2|
    node2.vm.box = "ubuntu/trusty64"
    node2.vm.hostname = "node2"
    node2.vm.network "private_network", type: "dhcp"
    node2.vm.provision "shell", privileged: false, inline: <<-EOF
       set -e
       sudo useradd ansible -m
       echo "ansible\nansible\nansible" | sudo passwd ansible
    EOF
 end

 config.vm.define "Node_03" do |node3|
    node3.vm.box = "ubuntu/trusty64"
    node3.vm.hostname = "node3"
    node3.vm.network "private_network", type: "dhcp"
    node3.vm.provision "shell", privileged: false, inline: <<-EOF
       set -e
       sudo useradd ansible -m
       echo "ansible\nansible\nansible" | sudo passwd ansible
    EOF
 end

 config.vm.define "Node_04" do |node4|
    node4.vm.box = "nrel/CentOS-6.5-x86_64"
    node4.vm.hostname = "node4"
    node4.vm.network "private_network", type: "dhcp"
    node4.vm.provision "shell", privileged: false, inline: <<-EOF
       set -e
       sudo useradd ansible -m
       echo "ansible\nansible\nansible" | sudo passwd ansible
    EOF
 end
end
