# Configuration Management

We'll learn about Ansible stuff

# What is Ansible?
It is an Automation tool for IT setup. It's Main Use Cases

* Provisioning
* Configuration Management
* Deployment
* Orchestration
* Part of Continuous Delivery/Deployment

# Why Ansible?

- Simple to use
- AgentLess (requires only Python and SSH )
- Sensible Design
- Eg: Manual Vs ShellScript Vs Playbook

# YAML Basics

- Key : Value Pair
- "---" starts with for yaml file
- Spaces and Indent are Very important. And YAML Don't accepts Tab Key.
- Eg:
```
    ---
    hosts: nginx
    user: ansible
    gather_facts: no
    tasks:
      - name: "Echoing..."
        shell: "echo 'helloworld'"
```

# Old CM and Bash manual Deployment Problems

# Overview

- Inventories
- Modules
- variables
- Facts
- Playbooks and play
- Configuration Files
- Templates
- Roles
- Vault
- Galaxy 

### Inventories

 - Static or Local Files (eg. /etc/ansible/hosts)
 - Can be Dynamic too. And provided via program
 - Can be called via "-i" options 
 
### Modules

 - Modules (also referred to as “task plugins” or “library plugins”) are discrete unites of code
 - Can be used from the command line or in a playbook task.
 ```
    ansible webservers -m service -a "name=httpd state=started"
    ansible webservers -m ping
 ```
 - Ansible `ansible-doc yum` will list details of yum modules (Eg. `ansible-doc -l`)
 
 ### variables
 
  - Allows you to customize the behaviour of the systems.
  - Variable names should be letters, numbers, and underscores. Variables should always start with a letter.
  - Reference variables in your playbooks using the Jinja2 templating system
  Eg.
  ```
     My amp goes to {{ max_amp_value }}
  ```
  
### Ansible Facts

 - It is a way of gathering data from systems.
 - Can be used in the playbooks
 - By default is enabled, but can be disabled in playbook.
 - speeding up
   ```
    - hosts: webserver
      gather_facts: no
    ```
    
### Playbooks

 - A playbook is a task
 - Playbooks are Instruction manuals, the hosts are the raw materials
 - A Playbook is made of individual  plays.
 - Playbook are in YAML format

### ConfigFiles

 - The default is "/etc/ansible/ansible.cfg"
 - You can enable or disable options in the config files.
 - The config file is read when a playbook is run.
 - You can use config files other than default location.  But, the order as follows,
     * ANSIBLE_CONFIG (environment variable if set)
     * ansible.cfg (in the current directory)
     * ~/.ansible.cfg (in the home directory)
     * /etc/ansible/ansible.cfg
     
### Templates

 - It contains all your configuration parameters.
 - There is a ansible module called template.
 - A template is definition and set of parameters for running ansible Job.
 - Job templates are usefull to execute to same job many times.

### Handlers

 - A task in a Playbook can trigger an handler.
 - Used to handle error conditions.
 - Called at the end of play.
 - Can have multiple task trigger an handler.
 
### Roles

### Ansible Vault
 - It keeps sensitive data
 - A secure store.
 - Password and Encrypted files.
 
# Ansible Installation 

To set up an Ansible, I've used one master and two/three more nodes. Pre-requisites tools are
 * Vagrant
 * Virtual box
 * Python 2.6 or above
 * Openssh

For more details about vagrant tool. Follow this link
