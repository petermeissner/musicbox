# Jukebox 

Source code for a 5 buttons mp3 jukebox running on a raspberry pi that I build for my boys (5 and 4 years old) for christmas 2019. 


# CRON Setup 

Add the follwoing line to get the script started at boot up.

```bash
@reboot export DISPLAY=:0.0 && cd /home/pi && nohup python3 /home/pi/musicbox/music_box.py &
```

- `@reboot` ensures that the line will be run at each reboot
- `export DISPLAY=:0.0` since I use `{pygame}` and it has problems with beeing run headless I add this line to make it work without `sudo` and without a display. 
- `nohup` is used so that the line finishes immediately although `music_box.py` actually is an infinite loop.
