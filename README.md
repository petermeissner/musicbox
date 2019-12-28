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


# VSCode Debug Config

```JSON
{
  // Use IntelliSense to learn about possible attributes.
  // Hover to view descriptions of existing attributes.
  // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      // IMPORTANT PART to make pygame work without actual display
      "env": {"DISPLAY": '0.0'}
    }
  ]
}
```


# Audio Comment Telling Children What they are about to Hear

Free online text-to-speach (mp3) service:

https://notevibes.com/de/
