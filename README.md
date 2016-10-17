## python-docker-opencv-demo

Instead of using webcam capture and GUI output, this sample
reads from a file and outputs to a new file.

Before you start make sure you have a directory
called `data` in the root directory of the the project.

To enter the docker container run this:

	$ make enter

This will run a docker container and thow you into a bash shell,
in which you have to run this command to convert the video:

	$ make run