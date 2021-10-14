FROM tensorflow/tensorflow:1.7.0-devel

MAINTAINER Jerome WAX "xblaster@lo2k.net"

WORKDIR /tensorflow

ADD src .

RUN git pull
CMD cd /tensorflow && ./train.sh
