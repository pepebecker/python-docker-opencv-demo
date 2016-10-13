## python-docker-opencv-demo

Instead of using webcam capture and GUI output, this sample
reads from a file and outputs to a new file.

To build the container:

    $ git clone https://github.com/brianshaler/python-docker-opencv-demo.git
    $ cd python-docker-opencv-demo
    $ docker build -t pdocv .

Now you can `docker run [opts] pdocv [cmd]`. For example:

    $ docker run --rm -v $(pwd)/data:/data pdocv python ./main.py ./video/input.webm /data/output.webm

The above command creates/links local directory `./data` to
`/data` inside the container (`-v $(pwd)/output:/data`), and
processes the project's sample video (`video/input.webm`) and
outputs it to `./data/output.webm` in the project directory.

If you want to modify main.py, either make changes and run
`docker build -t pdocv .` again, OR link your working copy
with `-v $(pwd):/usr/src/app` (before or after the other `-v`
used above, but MUST be *after* `docker run` and *before*
`pdocv`). Then, your current copy of `main.py` would be used
instead of the one in the image.

e.g. Make a change to `main.py` in your project directory,
run:

    $ docker run --rm -v $(pwd):/usr/src/app pdocv python ./main.py ./video/input.webm ./data/output2.webm

(note: `./data ` is a relative path in this example, since
`/data` was not mounted)

You should then see your changes reflected on in the video
located at `./data/output2.webm`.
