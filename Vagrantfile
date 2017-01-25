# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

current_dir    = File.dirname(File.expand_path(__FILE__))
configs        = YAML.load_file("#{current_dir}/vars.yml")


VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = 'azure'
  config.vm.network "public_network"
  config.vm.network "private_network",ip: "192.168.33.101"
  config.vm.define "localhost" do |l|
    l.vm.hostname = "localhost"
  end

  config.vm.provider :azure do |azure, override|
    azure.mgmt_certificate = File.expand_path(configs['mgmt_certificate_path']) 
    azure.mgmt_endpoint = 'https://management.core.windows.net'
    azure.subscription_id = configs['subscription_id']
    azure.vm_image = 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_5-LTS-amd64-server-20160809.1-en-us-30GB'
    azure.vm_name = configs['vm_name']
    azure.vm_user = configs['vm_user']
    azure.cloud_service_name = configs['vm_name']  
    azure.vm_password = configs['vm_password']
    azure.vm_location = 'West Europe' 
    azure.ssh_port = '22'
    azure.tcp_endpoints = '80:80'
  end   

  config.ssh.username = configs['vm_user']
  config.ssh.password = configs['vm_password']


  config.vm.provision "ansible" do |ansible|
    ansible.sudo = true
    ansible.playbook = "provision.yml"
    ansible.verbose = "v"
    ansible.host_key_checking = false
  end

end

