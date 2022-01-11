# TNC-LCD
A spi LCD for the TNC-X on a RPI, Shows the last 3 MHEARD and IP address

Written in Python 3 it reads from /var/ax25/mheard/mheard.dat parses the data in memory before writing to the LCD.

It uses Cron to trigger it once every 60 seconds then ends.
MHEARDD is started from RC.LOCAL as is the Beacon and the KISS Attachment
