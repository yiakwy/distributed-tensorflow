Distributed Tensorflow Building
===============================

![net-topology](/net-topology.png)

This project aimed at providing necessary files needed to build [distributed tensorflow](http://yiakwy.github.io/blog/2017/05/13/Tiny-Distributed-Tensorflow-&-OCI-Series2) for CentOS users.

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

In the default OS configuration, you have yum \(executed by system python\), python2.7 installed. To configure, you need net-tools, git and docker.

Second step, execute shell codes:
```
yum install -y \
    yum-utils \
    git \
    vim

mkdir Github && cd Github
git clone https://github.com/yiakwy/distributed-tensorflow.git
cd ~
```
Third step, Install Docker and execute it

```shell
curl -# -O https://download.docker.com/linux/centos/7/x86_64/stable/Packages/docker-ce-17.03.1.ce-1.el7.centos.x86_64.rpm
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum-config-manager --enable docker-ce-edge
sudo yum makecache fast
sudo yum install docker-ce-\* -y
sudo systemctl start docker && docker run hello-world
# make sure docker run as non-root user
sudo groupadd docker
sudo usermod -aG docker $USER
```

or run equivalently 

> sh ~/Github/distributed-tensorflow/docker.install

### beside the default version of Docker
It will typically take half an hour to install the software. The link is continuously updated by relevant maintainers. So if you want to install specific version of Docker, you might need to consult Docker repositories in [**yum**](https://docs.docker.com/engine/installation/linux/centos/#install-docker).

## Distributed Tensorflow with grpc
You can either pull image from [Yiak](https://hub.docker.com/r/yiakwy/tensorflow-distributed/) or run following commands to build by yourself. But I recommend to build it by yourself, becuase you might have several things to configure locally

### Run server inside a container for Router - Nodes framework:
Expose ports you want and configure router accordingly. Run docker in the following manner:

> docker run -p 4000:9001 -p 4001:9002 $USER/tensorflow-distributed

Then your server can be visited outside the world

### Test
cd tests you can try whatever you want!
![test-ex](/test-ex.png)

## BUG SHOOTING
### Amazon EC2 Connection Refusion
Since authentication required by Amazon EC2 Cloud, requrests being referred by Github\(Github-Cloud hosted in Amazon EC2 platform\) will be refused due to lack of signature.

The current solution is downloading the file directly and scp to remote servers. "get-pip" has already been included in the repository but if you encounter more such errors, please download scripts by yourself.

## To Support GPU processing
Before you install nvdocker, you must uninstall all the old versions of docker

``` shell
sudo yum remove docker \
                docker-common \
                container-selinux \
                docker-selinux \
                docker-engine
```

Then 

``` shell
sudo sh nvdocker.install
```

## "Tensorflow-Serving"

Optionally you can use dockerfile provided by google, but with dependencies on Ubuntu, CentOS will use significant time to build it.

### For people in China
You cannot download bazel without "Amazon signature client referred by github". Since bazel is very large \(
cannot uploaded to github \), the plausible way to download bazel is

> download: bazel-0.4.5-installer-linux-x86_64.sh

then

> sudo scp -i ~/.ssh/PrivateKey -P RouterPort  ~/GitHub/distributed-tensorflow/bazel-0.4.5-installer-linux-x86_64.sh root@RouterHost:~/Github/distributed-tensorflow/   

### build
```
cd ~/Github/distributed-tensorflow/
# $USER is your DockerHub username !
docker build --pull -t yiakwy/tensorflow-serving-devel -f Dockerfile.devel .
```
Google tensorfow-serving use babel to build and export models, which consumes nearly 10 GB memories in runtime.

run the following commands to run container

> docker run -it ${your dockerhub usernaem}/tensorflow-serving-devel

then run 
``` shell
git clone --recurse-submodules https://github.com/tensorflow/serving
cd serving/tensorflow
./configure
cd ..
bazel test tensorflow_serving/...
```

