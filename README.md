# FishCam: A low-cost open source autonomous camera for aquatic research

## Description:
These are all the scripts needed to run the FishCam. See HardwareX paper [here](https://www.sciencedirect.com/science/article/pii/S2468067220300195).

Mouy, X., Black, M., Cox, K., Qualley, J., Mireault, C., Dosso, S., and Juanes, F., 2020. “FishCam: A low-cost open source autonomous camera for aquatic research,” HardwareX 8, e00110. https://doi.org/10.1016/j.ohx.2020.e00110. 

## Authors
Xavier Mouy (1,2), Morgan Black (3), Kieran Cox (3), Jessica Qualley (3), Callum Mireault (4), Stan Dosso (1), and Francis Juanes (3)

1. School of Earth and Ocean Sciences, University of Victoria, 3800 Finnerty Road, Victoria, BC, V8P 5C2, Canada.
2. JASCO Applied Sciences, 2305 4464 Markham Street, Victoria, BC, V8Z 7X8, Canada.
3. Biology department, University of Victoria, 3800 Finnerty Road, Victoria, BC, V8P 5C2, Canada.
4. Geography Department, Memorial University, P.O. Box 4200, St. John's, NL, A1C 5S7, Canada.

## Abstract
We describe the "FishCam", a low-cost (< 500 USD) autonomous camera package to record videos and images underwater. The system is composed of easily accessible components and can be programmed to turn ON and OFF on customizable schedules. Its 8-megapixel camera module is capable of taking 3280 x 2464-pixel images and videos. An optional buzzer circuit inside the pressure housing allows synchronization of the video data from the FishCam with passive acoustic recorders. Ten FishCam deployments were performed along the east coast of Vancouver Island, British Columbia, Canada, from January to December 2019. Field tests demonstrate that the proposed system can record up to 212 hours of video data over a period of at least 14 days. The FishCam data collected allowed us to identify fish species and observe species interactions and behaviors. The FishCam is an operational, easily reproducible and inexpensive camera system that can help expand both the temporal and spatial coverage of underwater observations in ecological research. With its low cost and simple design, it has the potential to be integrated into educational and citizen science projects, and to facilitate learning the basics of electronics and programming.

![alt text](https://ars.els-cdn.com/content/image/1-s2.0-S2468067220300195-ga1.jpg "Graphical abstract")


Open a terminal window and type the following commands:
(a)
Ensure the OS is up to date:
•
sudo apt-get update
•
sudo apt-get upgrade
(b)
Install Python 3:
•
sudo apt-get install python3
(c)
Install the python picamera library:
•
sudo apt-get install python3-picamera
(d)
Install the python GPIO library:
•
sudo apt-get install python3-rpi.gpio
(e)
Install the crontab job scheduling tool:
•
sudo apt-get install cron
(f)
Install Git to download the FishCam scripts from GitHub:
•
sudo apt-get install git
(g)
Download the FishCam scripts from GitHub:
•
cd/home/pi/Desktop/
•
git clone https://github.com/xaviermouy/FishCam.git.(notice the “. ” at the end)
•
A folder named “FishCam” should now be on the Desktop and have the scripts to run the FishCam.
(h)
Install the WittyPi software:
•
wget http://www.uugear.com/repo/WittyPi2/installWittyPi.sh
•
sudo sh installWittyPi.sh
•
When prompted, type y to remove fake-hwclock, and n to not install Qt5
11.
Restart the Raspberry Pi to apply all the changes.
12.
Once Raspbian has restarted, open a terminal window and type sudo raspi-config to configure the Raspberry Pi:
(a)
If not done already, change your user password in the menu Change User Password.
(b)
In the menu Network Options select Hostname, and change it to fishcam01. Other hostnames can be chosen, but it has to be explicit enough to be easily identifiable on a network.
(c)
In the menu Change Boot Options and Desktop/CLI, select Desktop Auto Login.
(d)
To set FishCam time to UTC, in the menu Localisation Options, select Change Time Zone, then None, and GMT.
(e)
In the menu Interfacing Options set the Camera (CSI camera interface) and SSH connection to enabled.
(f)
Ensure the entire microSD card is used by selecting Expand Filesystem in the menu Advanced Options.
(g)
Select Finish to exit raspi-config.
13.
At this point all the necessary software are installed.
14.
Optional: shut down the Raspberry Pi, take the microSD card out and connect it to your computer. Use free software such as Win32 Disk Imager to take an image of the microSD card with all the software installed. The image file created may be used to set up another FishCam without having to go through all the installation steps described above.
6.2 Automatic start of the recordings
The crontab job scheduler is used to start acquiring video when the FishCam is powered ON (i.e. rebooted). Open a terminal window and type the following commands:
1.
Edit the job schedule by typing: crontab -e
2.
The first time you run crontab you will be prompted to select an editor. Choose Nano by pressing Enter.
3.
Once the schedule is open in Nano:
(a)
Scroll down with the down-arrow key to the bottom of the document and type
@ reboot sh/home/pi/Desktop/FishCam/script/camStartup.sh &
(b)
Save the changes by pressing CTRL  + O, then press Enter to confirm.
(c)
Exit Nano by pressing CTRL  + X.
4.
Verify that the schedule has been saved:
crontab -l
5.
Close terminal
6.3 FishCam ID
If you are using several FishCams, it may be useful to assign a unique ID to each of them. This ID will be used at the beginning of the filename of each video being recorded. To modify the FishCam ID:
1.
Go to the folder /home/pi/Desktop/FishCam/script/
2.
Open the file FishCamID.config with a text editor.
3.

sudo apt-get install python3-pip
sudo apt-get install python3-scipy libportaudio2
pip3 install sounddevice soundfile
Type the FishCam ID, save, and close the text editor. By default FishCam ID is set to FishCam01.
6.4 Camera settings
All the camera settings are defined in the python script captureVideo.py located in the folder /home/pi/Desktop/FishCam/script/. To change the settings, open the script captureVideo.py with a text editor and adjust the parameters defined in the function initVideoSettings(). For more information about the different parameters, refer to the documentation of the picamera library (https://picamera.readthedocs.io).
