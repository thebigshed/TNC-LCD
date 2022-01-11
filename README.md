# TNC-LCD
A spi LCD for the TNC-X on a RPI, Shows the last 3 MHEARD and IP address

Written in Python 3 it reads from /var/ax25/mheard/mheard.dat parses the data in memory before writing to the LCD.

It uses Cron to trigger it once every 60 seconds then ends.
MHEARDD is started from RC.LOCAL as is the Beacon and the KISS Attachment

CRON-ENTRY
  Shows what I added to via 'crontab -e' to kick the python code
  
Config.txt & cmdline.txt
  shows the settings I used to enable the TNC on serial0 and enable the I2C port to talk to the display
  
/etc/rc.local
  shows the attachment of the TNC, starting of MHEARD deamon and the beaconing. You will need to edit this to add your callsign, location and anything else you require.
  
