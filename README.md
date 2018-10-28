# EZCTF

---

### Overview

EZCTF is meant to be an easy to setup Capture the Flag web appp. It leverages flask to do the brunt of the work as well as many other tools to simplify other complex workloads.

The following is included

1. ezctf-alpha
  * Original monolithic single file flask app. This was the starting point and prototype of functionality.

2. linted_ctf 
  * Split the CTF app from one file into modularized blue prints
  * Added in PyTest fixtures to test functionality and increase code coverage
  * Added much needed permission checks and error handling
  * Pretty complete but still needs improved secret handling

3. ezctf-ansible
  * Ansible roles apply the needed configuration to Linux systems that will host our app
  * Deploys our application to said servers
  * Has VagrantFile to replicate the above on your localhost for development and testing
  * Leverages SQLAlchemy to provision database for first run
  * Contains post deploy testing script using UnitTest and Selenium to verify the apps functions

4. ezctf-terraform
  * Provisions the AWS cloud where we will host our EZCTF infrastructure
  * Uses a backend provider so code is transportable
  * Demonstrates infrastructure as code
  * Still a work in progress
