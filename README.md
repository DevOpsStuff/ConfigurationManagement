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

### Problems in Bash Scripts and Old CM

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
       - Eg.
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

For more details about vagrant tool. Follow this [link](Vagrant.md)

```
  vagrant init
   // Remove the VagrantFile and Replace it with given VagrantFile.
  vagrant up // it will download the associated images from vagrantCloud.
  vagrant ssh
```

![Ansible](https://github.com/DevOpsStuff/ConfigurationManagement/blob/master/Ansiblediagram.PNG)

# Adhoc Commands

- An ad-hoc command is something that you might type in to do something really quick, but don’t want to save for later.
- Ad-hoc commands can also be used to do quick things that you might not necessarily want to write a full playbook.
Let's see the examples of Ad-hoc commands.

 ```
   ansible all -m ping  -k
   ansible node1 -a "ls -l /var/log/messages" -k
   
   #Installing applications
   ansible node2 -m apt -a "name=elinks state=latest -k -b"
   
   # Now ping in ansible playbook
   
   ---
   - hosts: all
     tasks:
        - ping: 
     
    # List hosts
    ansible node1 --list-hosts
    
    #facts 
    ansible -i hosts node1 -m setup -k -a "filter=ansible_default_ipv4"

    #setting up Host variables
    [node1]
    <ip> home_dir=/home/ansible
    
    #Forking
    ansible -i hosts all -a "df -h" -k -f 100
    
    #Copying
    ansible -i hosts node1 -m copy -a "src={{home_dir}}/ping.yaml dest={{home_dir}}"
    
    #File ##Important
    ansible -i hosts node1 -m file -a "dest={{ home_dir }}/ping.yaml mode=600" -k
   
   ```
   
 # Inventories
   **STATIC Inventory**
   - Can be in any formats
   ```
       badwolf.example.com:5309
       jumper ansible_port=5555 ansible_host=192.0.2.50
   ```
   
   *NOTE:*  Ansible 2.0 has deprecated the “ssh” from ansible_ssh_user, ansible_ssh_host, and ansible_ssh_port to become ansible_user, ansible_host, and ansible_port. If you are using a version of Ansible prior to 2.0, you should continue using the older style variables (ansible_ssh_*). These shorter variables are ignored, without warning, in older versions of Ansible.
       
    ```
       # Adding Hosts can be done via Patterns.
       [webservers]
       www[01:50].example.com
       
       [databases]
       db-[a:f].example.com
    ```
   You can also select the connection type and user on a per host basis:
   
   ```
   [targets]
   localhost              ansible_connection=local
   other1.example.com     ansible_connection=ssh        ansible_user=mpdehaan
   other2.example.com     ansible_connection=ssh        ansible_user=mdehaan
   ```
   Group Variable for Hosts
   ```
   [atlanta]
   host1
   host2

   [atlanta:vars]
   ntp_server=ntp.atlanta.example.com
   proxy=proxy.atlanta.example.com
   ```
   NOTE: The Preferred behaviour is NOT to store in the main inventory file.
   
   - Default Groups
     There are two default groups: all and ungrouped. all contains every host.ungrouped contains all hosts that don’t have another group aside from all. Every host will always belong to at least 2 groups. Though all and ungrouped are always present, they can be implicit and not appear in group listings like group_names.
     
   - Host and Group Variables can be stored in the individual files relative to the inventory file.
   - Assuming the inventory file path is: `/etc/ansible/hosts`. Following applies.
   
        - if the host names 'mainhost', and is in the groups 'India' and 'Canada', then the variables in the YAML files at the following  locations will be made available to the host. NOTE: Can optionally end in '.yml' or 'yaml'
          
   ```
   /etc/ansible/group_vars/India # can optionally end in '.yml', '.yaml', or '.json'
   /etc/ansible/group_vars/Canada
   /etc/ansible/host_vars/mainhost
   ```
  
   **Dynamic Inventories**
   
   - Test-based support, but has abilities to support Dynamic inventoriess.
   - You can pull the inventories from a cloud Provider,LDAP,Cobbler.
   - some cloud providers supported are EC2,RackSpace,Openstack.
   - Will accept any kind of executable file as an inventory file
        - `ansible-playbook playbook.yml -i ./dynamic.py`
        - `ansible all -i /etc/ansible/ec2.py -m ping`
    - If it is executable the ansible expects a json output.
    - You could create a binary or a script as long as it outputs the JSON to output.
   

