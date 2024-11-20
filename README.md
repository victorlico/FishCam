# FishCam: A Low-Cost Open Source Autonomous Camera for Aquatic Research  

## Description  
These are all the scripts needed to run the FishCam. See the HardwareX paper [here](https://www.sciencedirect.com/science/article/pii/S2468067220300195).  

**Citation:**  
Mouy, X., Black, M., Cox, K., Qualley, J., Mireault, C., Dosso, S., and Juanes, F., 2020. “FishCam: A low-cost open source autonomous camera for aquatic research,” *HardwareX* 8, e00110. [https://doi.org/10.1016/j.ohx.2020.e00110](https://doi.org/10.1016/j.ohx.2020.e00110).  

## Authors  
- Xavier Mouy (1,2)  
- Morgan Black (3)  
- Kieran Cox (3)  
- Jessica Qualley (3)  
- Callum Mireault (4)  
- Stan Dosso (1)  
- Francis Juanes (3)  

**Affiliations:**  
1. School of Earth and Ocean Sciences, University of Victoria, 3800 Finnerty Road, Victoria, BC, V8P 5C2, Canada.  
2. JASCO Applied Sciences, 2305 4464 Markham Street, Victoria, BC, V8Z 7X8, Canada.  
3. Biology Department, University of Victoria, 3800 Finnerty Road, Victoria, BC, V8P 5C2, Canada.  
4. Geography Department, Memorial University, P.O. Box 4200, St. John's, NL, A1C 5S7, Canada.  

## Abstract  
The "FishCam" is a low-cost (< 500 USD) autonomous camera system to record underwater videos and images. Composed of accessible components, it allows customizable ON/OFF scheduling. Its 8-megapixel camera captures high-resolution images (3280x2464) and videos. An optional buzzer circuit synchronizes video data with passive acoustic recorders. Field-tested along Vancouver Island's east coast in 2019, the FishCam recorded up to 212 hours over 14 days, enabling fish species identification and behavioral observations. The system is low-cost, easily reproducible, and ideal for ecological research, educational projects, and citizen science initiatives.  

![Graphical Abstract](https://ars.els-cdn.com/content/image/1-s2.0-S2468067220300195-ga1.jpg "Graphical Abstract")  

---

## Installation Instructions  

### Step 1: Update the OS  
```bash
sudo apt-get update  
sudo apt-get upgrade
```  

### Step 2: Install Dependencies  

#### (a) Install Python 3  
```bash
sudo apt-get install python3
```  

#### (b) Install the Python Picamera library  
```bash
sudo apt-get install python3-picamera
```  

#### (c) Install the Python GPIO library  
```bash
sudo apt-get install python3-rpi.gpio
```  

#### (d) Install the Crontab job scheduler  
```bash
sudo apt-get install cron
```  

#### (e) Install Git  
```bash
sudo apt-get install git
```  

#### (f) Install Audio Recording Dependencies  
```bash
sudo apt-get install python3-pip  
sudo apt-get install python3-scipy libportaudio2  
pip3 install sounddevice soundfile
```  

### Step 3: Download FishCam Scripts from GitHub  
```bash
cd /home/pi/Desktop/  
git clone https://github.com/xaviermouy/FishCam.git.  # Notice the "." at the end
```  
The **FishCam** folder will appear on the Desktop, containing all necessary scripts.  

### Step 4: Install WittyPi Software  
```bash
wget http://www.uugear.com/repo/WittyPi2/installWittyPi.sh  
sudo sh installWittyPi.sh
```  
When prompted:  
- Type `y` to remove the fake-hwclock.  
- Type `n` to skip installing Qt5.  

### Step 5: Restart the Raspberry Pi  
```bash
sudo reboot
```  

### Step 6: Configure the Raspberry Pi  
1. Open the configuration tool:  
   ```bash
   sudo raspi-config
   ```  
2. Adjust the following settings:  
   - **Change User Password:** Update your password in **Change User Password**.  
   - **Network Options:** Set the hostname to `fishcam01` in **Hostname**.  
   - **Boot Options:** In **Desktop/CLI**, select **Desktop Auto Login**.  
   - **Time Zone:** Set to UTC in **Localisation Options > Change Time Zone**, then select **None** and **GMT**.  
   - **Interfacing Options:** Enable the **Camera (CSI interface)** and **SSH connection**.  
   - **Advanced Options:** Expand the filesystem by selecting **Expand Filesystem**.  
3. Select **Finish** to exit.  

### Step 7: Optional - Backup SD Card  
Shutdown the Raspberry Pi and use software like Win32 Disk Imager to create a backup image of the SD card.  

---

## Additional Configuration  

### 1. Automatic Start of Recordings  
Use Crontab to start video recording on reboot:  
```bash
crontab -e
```  
In the Nano editor:  
- Add the following line:  
  ```bash
  @reboot sh /home/pi/Desktop/FishCam/script/camStartup.sh &
  ```  
- Save changes (`CTRL + O`, press Enter) and exit (`CTRL + X`).  
Verify the Crontab schedule with:  
```bash
crontab -l
```  

### 2. Set FishCam ID  
1. Navigate to the script folder:  
   ```bash
   cd /home/pi/Desktop/FishCam/script/
   ```  
2. Edit the **FishCamID.config** file:  
   ```bash
   nano FishCamID.config
   ```  
3. Set the FishCam ID (default is **FishCam01**), save, and close.  

### 3. Adjust Camera Settings  
Edit the **captureVideo.py** script to modify camera settings:  
```bash
nano /home/pi/Desktop/FishCam/script/captureVideo.py
```  
Adjust parameters in the `initVideoSettings()` function. Refer to the [Picamera documentation](https://picamera.readthedocs.io) for more details.  
