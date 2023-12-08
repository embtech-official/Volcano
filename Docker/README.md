# Building Docker Container:

## Step 1:

From the command-line, in your development PC, login to the Docker CLI:

```bash
docker login
```

Follow the prompt with your Docker Hub credentials. Visit [Docker Hub page](https://hub.docker.com/) to create a Docker ID if you don't have credentials.

## Step 2:

#### Enable Arm emulation

Arm emulation makes it possible to run Arm instructions on Intel x86-64 architectures. That is, you can run binaries compiled for the Arm instruction set on an x86 computer.

To enable this emulation to be used with Docker, run the following command:

```bash
docker run --rm -it --privileged torizon/binfmt
```

## Step 3:

Enter the  folder you have the Dockerfile and build the image:

```bash
docker build --pull -t <username>/<name-of-image> .
```

Note that :

- `<username>` your Docker Hub username.

- `<name-of-image>`  name you want to give to the image in your docker hub

## Step 4:

Upload the image to your Docker Hub:

```
$ docker push <username>/<name-of-image>
```

Now your custom container image is accessible from Docker Hub.
