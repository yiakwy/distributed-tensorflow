FROM centos:7

MAINTAINER LEI WANG <yiak.wy@gmail.com>

RUN yum install -y \
	net-tools \
	git \
	curl
COPY ./requirements.txt ./requirements.txt
RUN curl -# -O https://bootstrap.pypa.io/get-pip.py && \
	python get-pip.py && \
	pip install --upgrade --index https://pypi.mirrors.ustc.edu.cn/simple/ -r requirements.txt

RUN pip install --upgrade --index https://pypi.mirrors.ustc.edu.cn/simple/ tensorflow 

# install gRPC

RUN pip install --index https://pypi.mirrors.ustc.edu.cn/simple/ enum34 futures mock six && \
    pip install --index https://pypi.mirrors.ustc.edu.cn/simple/ --pre 'protobuf>=3.0.0a3' && \
    pip install -i https://testpypi.python.org/simple --pre grpcio

RUN mkdir Server && mkdir tests
COPY ./Server/*.* ./Server/
COPY ./tests/*.* ./tests/

EXPOSE 9001
EXPOSE 9002

RUN echo "Running Tensorflow server in background" && \ 
    echo "For more Tensorflow-Serving services, please refer to the " && \
    # python Server/tensorflowServer.py
    nohup python Server/tensorflowServer.py > log 2>&1 &

CMD ["python", "Server/tensorflowServer.py"]
