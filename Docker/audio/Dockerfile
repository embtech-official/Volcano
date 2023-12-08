ARG IMAGE_ARCH=linux/arm64v8
ARG IMAGE_NAME=arm64v8-gpiod
ARG DOCKER_REGISTRY=torizonextras

FROM --platform=$IMAGE_ARCH ${DOCKER_REGISTRY}/$IMAGE_NAME

RUN apt -y update && apt -y upgrade
RUN apt install -y \
        vim      \
        nano      \
        python3    \
        libasound2 \
        libasound2-dev \
        alsa-utils \
        libsndfile1-dev \
        && apt-get clean \
        && apt-get autoremove \
        && rm -rf /var/lib/apt/lists/*

RUN usermod -aG audio torizon
