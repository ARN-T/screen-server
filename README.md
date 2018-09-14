# Screen Server readme

## Connecting to the screen server (RaspberryPi)
Open [https://gitforwindows.org/](Git Bash) and run `ssh pi@130.229.153.55`. Sign in with `SkFkLaPa5Pl`

### Running
1. Start screen by typing `screen`
2. Go to `tavla.git/tavla/ARN`
3. Start the python file with `sudo python main.py`
4. Press `Ctrl + A` then `D` to detach the screen session
5. Exit environment by running `exit`

### Stoping
1. Type `screen -ls` to view all screen sessions
2. Type `screen -D -r *sessin name*` to attach to the session running the process
3. Press Ctrl + C to stop the process

#### Required libraries
..* Pillow
..* spidev
..* freetype

compile c-library with
g++ -shared -o output_map.so output.c
