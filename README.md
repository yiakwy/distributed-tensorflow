Distributed Tensorflow Building
===============================

This project aimed to provid necessary files needed to build [distributed tensorflow](http://yiakwy.github.io/blog/2017/05/13/Tiny-Distributed-Tensorflow-&-OCI-Series2) for CentOS users.

The content includes:

- Dockerfile for gRPC version
- Dockerfile.devel \(provided by google\) for "Tensorflow-Serving"
- nvdocker.install shell script, to install CUDA gpu supported Docker Engine
- test files for distributed testing
- A pyton script to boost a server inside Docker Container

## INSTALL
First, check your OS version,

> cat /etc/centos-release # 7.x
 
It should be CentOS 7+, because docker drops support for CentOS 6. Now, the latest version of CenOS is 7.3

In the default OS configuration, you have yum \(executed by system python\), python2.7 installed. To configure, you need nettools, git and docker.

Second step, execute shell codes:
```
sudo yum makecache fast
yum install -y \\
    yum-utils \\
    git \\
    vim

mkdir Github && cd Github
git clone https://github.com/yiakwy/distributed-tensorflow.git
cd ~
```
Third step, Install Docker and execute it

> curl -# -O https://download.docker.com/linux/centos/7/x86\_64/stable/Packages/docker-ce-17.03.1.ce-1.el7.centos.x86\_64.rpm
> sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
> sudo yum-config-manager --enable docker-ce-edge
> sudo yum makecache fast
> sudo yum install docker-\* -y
> sudo systemctl start docker && docker run hello-world

### beside the default version of Docker
It will typically take one half an hour to install the software. The link is continuously updated by relevant companies. So if you want to install specific version of Docker, you might need to consult Docker repositories in **yum**.

## BUG SHOOTING
### Amazon EC2 Connection Refusion
Since authentication required by Amazon EC2 Cloud, requrests referred by Github\(Github-Cloud hosted in Amazon EC2 platform\) will be refused due to lack of signature.

The current solution is downloading the file directly and scp to remote servers. "get-pip" has already been included in the repository but if you encounter more such errors, please download scripts by yourself.

### To Support GPU processing
Before you install nvdocker, you must uninstall all the old versions of docker

> sudo yum remove docker \\
                  docker-common \\
                  container-selinux \\
                  docker-selinux \\
                  docker-engine

``` shell
sudo sh nvdocker.install
```

### "Tensorflow-Serving"


