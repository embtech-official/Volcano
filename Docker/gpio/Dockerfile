ARG IMAGE_ARCH=linux/arm64v8
ARG IMAGE_NAME=arm64v8-gpiod
ARG DOCKER_REGISTRY=torizonextras

FROM --platform=$IMAGE_ARCH ${DOCKER_REGISTRY}/$IMAGE_NAME

RUN apt -y update && apt -y upgrade
RUN apt install -y \
        vim      \
        nano      \
        python3    \
        libgpiod2 \
        gpiod \
        python3-pip \
        && apt-get clean \
        && apt-get autoremove \
        && rm -rf /var/lib/apt/lists/*

RUN pip3 install gpiod
RUN usermod -aG gpio torizon
