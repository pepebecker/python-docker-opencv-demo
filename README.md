## python-docker-opencv-demo

Instead of using webcam capture and GUI output, this sample
reads from a file and outputs to a new file.

First you need to initialize the project, for this run:

	$ make init

To enter the docker container run this:

	$ make enter

This will run a docker container and throw you into a bash shell,
in which you have to run this command to convert the video:

	$ make run