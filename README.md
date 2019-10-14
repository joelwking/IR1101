# IR1101
Notes for building a **Hello World** application in a container for the Cisco IR1101 (Industrial Router)

## Requirements
These instructions require [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](https://www.vagrantup.com/downloads.html) to be installed on your laptop. Visit the download links to download and install the binary for your system of choice.

## Deploy the Build Environment

Create a directory on your laptop (e.g. `~/Documents/WWT/projects/IR1101/`) and create / save a copy of the `library/Vagrantfile` [Vagrantfile](https://raw.githubusercontent.com/joelwking/IR1101/master/library/Vagrantfile) in that directory.

Issue `vagrant up` to build a VM. When the VM has been provisioned, `vagrant ssh` to connect to the deployed VM.

*NOTE:*  this example uses Ubuntu for the development environment, which is problematic installing Docker, [Reference: Instructions to avoid the "Docker Repository Does Not Have a Release File on Running apt-get update on Ubuntu" issue.](
https://stackoverflow.com/questions/41133455/docker-repository-does-not-have-a-release-file-on-running-apt-get-update-on-ubun/45881841) was referenced when creating the Vagrantfile. The Vagrantfile contains the commands to install Docker, simply test.

Test the Docker installation by issuing:
```
docker run hello-world
```
The Docker *hello-world* container should execute and complete successfully, verifying the installation.

### Clone this repository
To download the sample configuration files and setup a directory structure, clone this repository:
```bash 
git clone https://github.com/joelwking/IR1101.git
cd IR1101/library
```
Examine and become familiar with the configuration files.

## Configuration Files
The `/library` directory contains sample configuration files for creating the build environment and creating a package for installation and deployment on the IR1101. 

 * Vagrantfile: Used to instantiate an ephemeral virtual machine to build the package
 * package.yaml: Configuration file used to build the package
 * hello.py: Sample *Hello World* Python application
 * Dockerfile: Sample Dockerfile to create the Docker image

## Reference Instructions
The Cisco has provide these instructions to [Build and Deploy a Docker IOx Package for the IR1101 ARM Architecture](https://www.cisco.com/c/en/us/support/docs/routers/1101-industrial-integrated-services-router/214383-build-and-deploy-a-docker-iox-package-fo.html#anc10) and are used as the basis for the following steps. 

### Build the IOx Package for IR1101
Review [instructions](https://www.cisco.com/c/en/us/support/docs/routers/1101-industrial-integrated-services-router/214383-build-and-deploy-a-docker-iox-package-fo.html#anc10) in Part 1: Step 1. 

The IOx package is licensed software which requires a Cisco login and contract to download Assuming you have downloaded and saved the file, copy the file to the VM. For example, copy `ioxclient_1.9.2.0_linux_amd64.tar.gz` to the `library` directory.

```bash
scp administrator@192.168.56.104:/tmp/ioxclient_1.9.2.0_linux_amd64.tar.gz ioxclient_1.9.2.0_linux_amd64.tar.gz
```
Expand the file:
```bash
tar -xvzf ioxclient_1.9.2.0_linux_amd64.tar.gz
```
Export the path to the file(s):
```bash
export PATH=$PATH:/home/vagrant/IR1101/library/ioxclient_1.9.2.0_linux_amd64
```
Execute the client code to verify installation.
```bash
ioxclient -v
```
### Install the QEMU User Emulation Packages
Review [instructions](https://www.cisco.com/c/en/us/support/docs/routers/1101-industrial-integrated-services-router/214383-build-and-deploy-a-docker-iox-package-fo.html#anc10) in Part 1: Step 3.

```bash
sudo apt-get install qemu-user qemu-user-static
```
Verify this file exists: `ls -al /usr/bin/qemu-*static | grep aarch64`

### Test if an aarch64/ARV64v8 Container Runs on x86 Linux Machine
Review [instructions](https://www.cisco.com/c/en/us/support/docs/routers/1101-industrial-integrated-services-router/214383-build-and-deploy-a-docker-iox-package-fo.html#anc10) in Part 1: Step 4.

```bash
vagrant@ubuntu-xenial:~/IR1101/library$ docker run -v /usr/bin/qemu-aarch64-static:/usr/bin/qemu-aarch64-static --rm -ti arm64v8/alpine:3.7
Unable to find image 'arm64v8/alpine:3.7' locally
3.7: Pulling from arm64v8/alpine
40223db5366f: Pull complete
Digest: sha256:07d69855442f842117e85f24b58ba7cdd54166281d48fa05c58b6b79599d2181
Status: Downloaded newer image for arm64v8/alpine:3.7
/ # uname -a
Linux 64248448fc64 4.4.0-142-generic #168-Ubuntu SMP Wed Jan 16 21:00:45 UTC 2019 aarch64 Linux
/ # exit
```

### Build the Docker Image
Copy `qemu-aarch64-static` to the directory from where you will build the container:

```bash
cd ~/IR1101/library/
cp /usr/bin/qemu-aarch64-static .
```
The `Dockerfile` is configured to build an image which executes `hello.py`. Review the `Dockerfile` and Python program files in `~/IR1101/library/`. The docker build command builds the Docker image using the `Dockerfile` and python program located in the `library` directory. 

```bash
docker build -t iox_aarch64_hello .
```
Run the image to verify it will execute successfully on this system:
```bash
docker run -ti iox_aarch64_hello
```
You can issue a CTL + c to generate a *KeyboardInterrupt* which stops the container.

### Build the IOx Package
Review [instructions](https://www.cisco.com/c/en/us/support/docs/routers/1101-industrial-integrated-services-router/214383-build-and-deploy-a-docker-iox-package-fo.html#anc10) in Part 1: Step 7.

Save the image to a tar archive named `rootfs.tar`.

```bash
docker save -o rootfs.tar iox_aarch64_hello
```
The package descriptor file `package.yaml` is present in `~/IR1101/library/` and references `rootfs.tar`. 

**Note:** the default input file is `package.yaml` not `package.yml`!

Use `ioxclient` to build the IOx package for IR1101:
```bash
ioxclient package .
```
This command creates a file `~/IR1101/library/package.tar`.

Move or copy `package.tar` to your laptop or system where you can run a web browser. This file will need be uploaded to the IR1101 using the **Cisco IOx Local Manager**.

## Part 2. Configure the IR1101 for IOx
Review [instructions](https://www.cisco.com/c/en/us/support/docs/routers/1101-industrial-integrated-services-router/214383-build-and-deploy-a-docker-iox-package-fo.html#anc10) in Part 2. Follow these instructions to load and deploy the application on the IR1101.

At a minimum, you will need to enable **iox** and define the **VirtualPortGroup0** interface configured on the IR1101.

```
iox
!
interface VirtualPortGroup0
 ip address 192.0.2.1 255.255.255.0
 ip nat inside
 ip virtual-reassembly
!
interface GigabitEthernet0/0/0
 ip nat outside
 ip virtual-reassembly
```

## References

* Building IoT Apps with Node-RED: https://developer.cisco.com/meraki/build/exploring-meraki-and-spark-apis-with-node-red/
* Application Hosting on the Catalyst 9K https://github.com/joelwking/cat9k-soar

## Author
joel.king@wwt.com GitHub/GitLab @joelwking
