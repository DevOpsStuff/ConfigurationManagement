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

- Simple to use -> 
- AgentLess (requires only Python and SSH ) - A Push Model
  Linux -> SSH, Windows -> WinRM
- Sensible Design -> All Modules are included. So integration is easy.
- Eg: Manual Vs ShellScript Vs Playbook

## Push Vs Pull Model

 - In push Model, We can controll the sequence. Need to be on the same subnet, So not that much scalable.
 - In pull Model, Moe scalable and flexiable.

## YAML Basics

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

 - IAAS
 - Keep Everything in Git

### Code Vs Data
    
   Code - Template/Tasks 
   ```
        Apache Application
        
        User: {{ user }}
        port: {{ port }}
        conn: {{ connec_tcp }}
   ```
   Data - Vars
   
   ```
       host vars/groups vars
       user: alice
       port: 8080
       connec_tcp: http
   ```
### Idempotentance and State management
   - Runs multiple times
   - Checks desired state vs Current states everytime.
   

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

### Directory Layout [BestPractices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html?highlight=best%20practices#best-practices)

### [Inventories](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#working-with-inventory)

 - Inventories are where you find the information about the hosts you will manage with Ansible
 - Static or Local Files (eg. /etc/ansible/hosts)
 - It's where you group the hosts that will be managed in ansible.
 - Can be Dynamic too. And provided via program
 - Can be called via "-i" options 
 
### [Modules](https://docs.ansible.com/ansible/latest/modules/modules_by_category.html#module-index)

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
    
### Play and Playbooks

 - A play is a task
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
 - A playbook is a standalone file Ansible runs to set up your servers
 - Roles can be thoufgt of as a playbok that splits in to multiple servers.
 - Ansible Galaxy is a repository for roles people have created a tasks.

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

### Planning (Connection from Server to clients Using SSH ways)
  - username
  - sudo or root
  - passwordless keys or ssh-agent

### Configuring Ansible Clients
   *master*
   ```
   $ cat /etc/hosts #(add client address)
   $ ssh-keygen 
   $ cd ~/.ssh
   $ ssh-copy-id -i .ssh/id_rsa.pub ansible@slave1
   $ ssh-copy-id -i .ssh/id_rsa.pub ansible@slave2
   $ ssh-copy-id -i .ssh/id_rsa.pub ansible@slave3
   ```
   *Clients*
   ```
   $ visudo
   add -> "ansible ALL=(ALL) NOPASSWD: ALL" on all ansible clients
   ```

# Adhoc Commands

- An ad-hoc command is something that you might type in to do something really quick, but don’t want to save for later.
- Ad-hoc commands can also be used to do quick things that you might not necessarily want to write a full playbook.
Let's see the examples of Ad-hoc commands.

 ```
   ansible all -m ping  -k
   ansible node1 -a "ls -l /var/log/messages" -k
 ```
 
 ##### Raw,shell,command #####
 
   *command*
   
      -  Doesn't use shell (Bash/sh)
      -  can't use pipes or redirects
      
   ```
   $ ansible Slave1 -b -m command -a 'echo "hello" > /root/hello.txt'
   ```
   
   *Shell*
   
      - Supports pipes and redirects
      - Can't get messed up by user settings
      
   ```
   $ anisble Slave1 -b -m shell -a 'echo "hello" > /root/hello.txt'
   ```
   *raw*
   
      - Just sends commands over SSH
      - Doesn't need Python
      
   ```
   $ ansible Slave1 -b -m raw -a 'echo "hello" >> /root/hello.txt'
   ```
   
   ###### Installing applications
   
     $ ansible node2 -m apt -a "name=elinks state=latest -k -b"  -> apt
     $ ansible node2 -m yum -a "name=elinks state=latest -k -b"  -> yum
     $ ansible node2 -m pkg -a "name=elinks state=latest -k -b"  -> pkg
  
   ###### Now ping in ansible playbook
  
      ---
      - hosts: all
        tasks:
         - ping: 
      
    
   ###### List hosts
   
    $ ansible node1 --list-hosts
   
   ###### facts 
    
    $ ansible -i hosts node1 -m setup -k -a "filter=ansible_default_ipv4"
    
   ###### setting up Host variables
   
    [node1]
    <ip> home_dir=/home/ansible
    $ ansible Slave1 -b -a "touch testfile" --become-user tempuser
    
   ###### Forking
   
    $ ansible -i hosts all -a "df -h" -k -f 100
    
   ###### Copying
    
    $ ansible -i hosts node1 -m copy -a "src={{home_dir}}/ping.yaml dest={{home_dir}}"
    
    
   ###### File
    
    $ ansible -i hosts node1 -m file -a "dest={{ home_dir }}/ping.yaml mode=600" -k
    $ ansible -i hosts slave1 -m file -a "path=/root/hello.txt state=absent"
    
    
   
 # [Inventories](https://docs.ansible.com/ansible/2.3/intro_inventory.html#list-of-behavioral-inventory-parameters)
   
   **Static Inventory**
   
   - Can be in any formats.
   - They won't change unless you make changes to them.
   - A lot of info can be used by ansible.
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
   *NOTE:* The Preferred behaviour is NOT to store in the main inventory file.
   
   - **Default Groups**
   
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
   
   - Test-based support, but has abilities to support Dynamic inventories.
   - You can pull the inventories from a cloud Provider,LDAP,Cobbler.
   - some cloud providers supported are EC2,RackSpace,Openstack.
   - Will accept any kind of executable file as an inventory file
        - `ansible-playbook playbook.yml -i ./dynamic.py`
        - `ansible all -i /etc/ansible/ec2.py -m ping`
    - If it is executable the ansible expects a json output.
    - You could create a binary or a script as long as it outputs the JSON to output.
   
# Ansible PlayBooks

   - Playbooks are written in YAML
   - Playbooks should be idompotent. So you should be able to rerun them multiple times without problems. For instance, if a file is going to be overwritten and cause problems you should check first and not change it.
   - Plays are the individual tasks that are performed inside a playbook and a playbook is made up of one or more plays
   - Playbooks describe a set of steps in a process
   - They can be broken out to roles and templates
   - Playbooks are more efficient for multiple tasks

### Modules

   - Modules documentation.
   - Ansible ships with No. of Modules which can be exectuted directly on the remote machine.
   - Commonly Used Modules
   
         * Package Module (Instead of apt,yum,apt_repository)
         
         * File and Directories
                 - file,lineinfile,blockinfile,copy,fetch,template,and stat, Script.
                 
         * System
                 - service, user, group,cron,hostname,authorized_key,iptables,modprobe,
                   kernel_blacklist,gluster_volume,lvm,and zfs.
                   
         * Various Useful
                 - raw,synchronize,get_url,unarchive,ec2,and rds
                 
 ### ControlFlow,Conditionals and Error Handling
 
**Conditionals**

   - "When" and with "not when" , more examples [here](https://gist.github.com/marcusphi/6791404)
   
**Loops**
   - Ansible loop types. To see a full list [click here](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html)
       
   - loops with "with_items" and dict with "With_dict", More loop types
   
          - with_file: Evaluated a list of file
          - with_fileglob: Evaluated a list of files based on glob pattern
          - with_sequence and with_random_choice
       
**Handlers**
  - Handlers are just like tasks,but runs only when notifies
      
        tasks:
        - name: Install nginx
          package: name=nginx state=latest
          notify:
              - start nginx
          
          handlers:
              name: start nginx
              service: name=nginx state=started
         
 **Error Handling**
   - Error Handling and Tags

 ### Templates
 
   - Templates use the template module. The module can take variables that you have defined and replace those in files. The use is to  replace the information and then send that information to the target server.
   - Templates are processed by the Jinja2 templating language. Documentation about this language can be found here:                          http://jinja.pocoo.org/docs
   *Example:*
   
   - Here is what is in the template file called `template.j2`.
       
       
            <p>
            Hello there 
            <p>
     
   - Here is a sample playbook that uses that template:
      
     ```
       ---
        - hosts: databases
          become: yes
          vars:
               description: "{{ ansible_hostname }}"
          tasks:
           - name: write the index file
             template: src=template.j2 dest=/var/www/html/index.ht ml
             notify:
              - restart httpd
           - name: ensure apache is running
             service: name=httpd state=running
          handlers:
          - name: restart httpd
            service: name=httpd state=restarted
            ServerName = {{description}}
        ```
   - Here is the contents of the `/var/www/html/index.html` file once the playbook has run:
   
        ```
        <p>
        Hello there <p>
        ServerName = server
        ```
   - For this particular server, the hostname is 'server'.
   
# Roles:

  - Roles in Ansible use the idea of using include files and combines them to form reusable sections.
  - It allows you to reuse portions of your code easier. You break up the playbook into sections and when the playbook is run it pulls       all the sections together and runs against your target hosts
  - Ansible roles must be in a particular format to work as expected. You need a folder and subfolders to be in a specified format.
  - As an example, if we create a folder called Roles and we want to store our roles in there then we would create the fodler for the       project and its subfolders as needed. The ansible-galaxy command can be used to create the correct format as shown below
  - Starting in the Roles directory. The command `ansible-galaxy init apache` will create the following tree and files:
     ```
     apache/
        ├── defaults
        │ └── main.yml
        ├── files
        ├── handlers
        │ └── main.yml
        ├── meta
        │ └── main.yml
        ├── README.md
        ├── tasks
        │ └── main.yml
        ├── templates
        ├── tests
        │ ├── inventory
        │ └── test.yml
        └── vars
        └── main.yml
     ```
  - We would edit the files as required for the portions that our project needs. For instance, we would edit the `apache/tasks/main.yml`     file to put in the tasks that are required. We would edit the `apache/vars/main.yml` to put in any variables that are needed and so     on.
  - If you don't need a section then it's not used. So, for instance, if we put no data into `handlers/main.yml`, then it would be ignored when the role is run.
  
