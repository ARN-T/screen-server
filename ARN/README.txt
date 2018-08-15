run by:
start screen by typing "screen"
go to home folder (one folder up from start folder)
type "sudo bash network-monitor.sh &"
start the python file
press Ctrl + A then D to detach the screen session

Stop by:
typ "screen -ls" to view all screen sessions
type "screen -D -r *sessin name*" to attach to the session running the process
press Ctrl + C to stop the process

Required libraries:
Pillow
spidev
freetype

compile c-library with 
g++ -shared -o output_map.so output.c
