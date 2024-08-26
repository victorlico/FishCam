from picamera import PiCamera
import time
from datetime import datetime
import os
import logging
import subprocess
import sys
import sounddevice as sd
import wave
import threading

def initVideoSettings():
    videoSettings = {
        'duration': 20,      # duração dos arquivos em segundos
        'resolution': (1280, 720),
        'frameRate': 10,      # taxa de quadros por segundo
        'quality': 20,        # 1 = melhor qualidade, 20 - qualidade ok, 30 = qualidade inferior
        'format': 'h264',     # 'h264', 'mjpeg'
        'exposure': 'night',  # 'auto', 'night', 'backlight'
        'AWB': 'auto',        # 'auto', 'cloudy', 'sunlight'
        'sharpness': 0,       # inteiro entre -100 e 100, auto: 0 
        'contrast': 0,        # inteiro entre -100 e 100, auto: 0 
        'brightness': 50,     # inteiro entre 0 e 100, auto: 0
        'saturation': 0,      # inteiro entre -100 e 100, auto: 0
        'ISO': 400,           # sensibilidade baixa: 100, alta sensibilidade: 400, 800, auto: 0
        'vflip': False
    }
    return videoSettings

def record_audio(audio_filename, duration, sample_rate=44100):
    def callback(indata, frames, time, status):
        if status:
            logging.warning(str(status))
        audio_file.writeframes(indata.copy())

    with wave.open(audio_filename, 'wb') as audio_file:
        audio_file.setnchannels(1)  # Mono
        audio_file.setsampwidth(2)  # 16 bits
        audio_file.setframerate(sample_rate)

        with sd.InputStream(samplerate=sample_rate, channels=1, callback=callback):
            sd.sleep(int(duration * 1000))  # duration in milliseconds

def captureVideo(outDir, iterFileName, videoSettings, flagname=''):
    curDir = os.getcwd()
    iterFile = open(os.path.join(curDir, iterFileName), 'r') 
    iterNumber = iterFile.read()
    if len(iterNumber) == 0:
        iterNumber = 1
    else:
        iterNumber = int(iterNumber)
    iterFile.close()

    now = datetime.now()
    timeStampStr = now.strftime("%Y%m%dT%H%M%S.%fZ")
    if len(flagname) > 0:
        flagname = '_' + flagname

    base_filename = os.path.join(outDir, str(iterNumber) + flagname + '_' + timeStampStr)
    videofilename = base_filename + '_' + str(videoSettings['resolution'][0]) + 'x' + str(videoSettings['resolution'][1]) + '_awb-' + videoSettings['AWB'] + '_exp-' + videoSettings['exposure'] + '_fr-' + str(videoSettings['frameRate']) + '_q-' + str(videoSettings['quality']) + '_sh-' + str(videoSettings['sharpness']) + '_b-' + str(videoSettings['brightness']) + '_c-' + str(videoSettings['contrast']) + '_i-' + str(videoSettings['ISO']) + '_sat-' + str(videoSettings['saturation']) + '.' + videoSettings['format']
    audio_filename = base_filename + '.wav'

    print(videofilename)
    logging.info(videofilename)

    # Iniciar a gravação de áudio em uma thread separada
    audio_thread = threading.Thread(target=record_audio, args=(audio_filename, videoSettings['duration']))
    audio_thread.start()

    # Captura do vídeo
    camera = PiCamera()
    camera.framerate = videoSettings['frameRate']
    camera.resolution = videoSettings['resolution']
    camera.exposure_mode = videoSettings['exposure']
    camera.awb_mode = videoSettings['AWB']
    camera.vflip = videoSettings['vflip']
    camera.sharpness = videoSettings['sharpness']
    camera.contrast = videoSettings['contrast']
    camera.brightness = videoSettings['brightness']
    camera.saturation = videoSettings['saturation']
    camera.iso = videoSettings['ISO']
    
    camera.start_recording(videofilename, format=videoSettings['format'], quality=videoSettings['quality'])
    camera.wait_recording(videoSettings['duration'])
    camera.stop_recording()
    camera.close()

    # Aguarde o término da gravação de áudio
    audio_thread.join()

    # Atualiza o arquivo de iteração
    iterFile = open(os.path.join(curDir, iterFileName), 'w')
    iterNumber += 1
    iterFile.write(str(iterNumber))
    iterFile.close()

# As outras funções permanecem as mesmas...
def isCameraOperational():
    try:
        camera = PiCamera()
        camera.close()
        return True
    except BaseException as e:
        logging.error(str(e))
        return False

def captureVideo_loop(outDir,iterFileName,iterations=0, videoSettings=0,flagname=''):  
    # Load default settings if nothing else provided
    if videoSettings == 0:
        videoSettings = initVideoSettings()   
    # Loop
    if iterations == 0:  # Indefinite loop if no iterations provided
        loop= True
        while loop:
            captureVideo(outDir,iterFileName,videoSettings,flagname=flagname)
    elif iterations > 0:  # Finite loop if iterations provided
        for it in range(iterations):
            captureVideo(outDir,iterFileName,videoSettings,flagname=flagname)


def captureVideo_test(outDir,iterFileName,duration=10,flagname=''):    
    
    # Test brightness
    videoSettings = initVideoSettings()   
    videoSettings['duration'] = duration
    paramVals = range(40,105,5)
    for param in paramVals:        
        videoSettings['brightness'] = param
        captureVideo_loop(outDir,iterFileName,iterations=1,videoSettings=videoSettings,flagname=flagname)     
    
    # Test contrast
    videoSettings = initVideoSettings()   
    videoSettings['duration'] = duration
    paramVals = range(-20,120,20)        
    for param in paramVals:        
        videoSettings['contrast'] = param
        captureVideo_loop(outDir,iterFileName,iterations=1,videoSettings=videoSettings,flagname=flagname)
    
    # Test saturation
    videoSettings = initVideoSettings()   
    videoSettings['duration'] = duration
    paramVals = range(-100,120,20)        
    for param in paramVals:        
        videoSettings['saturation'] = param
        captureVideo_loop(outDir,iterFileName,iterations=1,videoSettings=videoSettings,flagname=flagname)
        
    # Test sharpness
    videoSettings = initVideoSettings()   
    videoSettings['duration'] = duration
    paramVals = range(-100,120,20)        
    for param in paramVals:        
        videoSettings['sharpness'] = param
        captureVideo_loop(outDir,iterFileName,iterations=1,videoSettings=videoSettings,flagname=flagname)

    # Test ISO
    videoSettings = initVideoSettings()   
    videoSettings['duration'] = duration    
    paramVals = [100,200,320,400,500,640,800]    
    for param in paramVals:        
        videoSettings['ISO'] = param
        captureVideo_loop(outDir,iterFileName,iterations=1, videoSettings=videoSettings,flagname=flagname) 

    # Test exposure
    videoSettings = initVideoSettings()   
    videoSettings['duration'] = duration    
    paramVals = ['auto', 'night','backlight']    
    for param in paramVals:        
        videoSettings['exposure'] = param
        captureVideo_loop(outDir,iterFileName,iterations=1,videoSettings=videoSettings,flagname=flagname) 
    # Test AWB
    videoSettings = initVideoSettings()   
    videoSettings['duration'] = duration    
    paramVals = ['auto', 'cloudy', 'sunlight']    
    for param in paramVals:        
        videoSettings['AWB'] = param
        captureVideo_loop(outDir,iterFileName,iterations=1,videoSettings=videoSettings,flagname=flagname) 


def main():
    # Parâmetros
    outDir = r'../data'
    logDir = r'../logs'
    iterFileName = r'iterator.config'
    FishCamIDFileName = r'FishCamID.config'
    BuzzerEnabled = True
    BuzzerIterationPeriod = -1

    # Iniciar logs
    if os.path.isdir(logDir) == False:
        os.mkdir(logDir)
    logging.basicConfig(filename=os.path.join(logDir, time.strftime('%Y%m%dT%H%M%S') + '.log'), level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logging.info('Video acquisition started')
    if os.path.isdir(outDir) == False:
        os.mkdir(outDir)
    try:
        curDir = os.getcwd()  # obter diretório de trabalho atual
        FishCamIDFile = open(os.path.join(curDir, FishCamIDFileName), 'r')  # abrir arquivo ID do FishCam para nomes de arquivos de saída
        FishCamID = FishCamIDFile.read()
        iterFile = open(os.path.join(curDir, iterFileName), 'r')  # abrir arquivo de iteração para nomes de arquivos de saída
        iterNumber = iterFile.read()
        subFolderName = iterNumber
        outDir = os.path.join(outDir, subFolderName)
        if os.path.isdir(outDir) == False:
            os.mkdir(outDir)

        BuzzerIdx = 0
        while True:
            if BuzzerIdx == 0 and BuzzerEnabled:
                camOK = isCameraOperational()  # verifica se a câmera está funcionando
                print(camOK)
                if camOK == True:  # ativa o buzzer apenas se a câmera estiver funcionando (necessário para verificação pré-implantação)
                    logging.info('Buzzer turned ON')
                    pid = subprocess.Popen([sys.executable, 'runBuzzer.py'])

            captureVideo_loop(outDir, iterFileName, iterations=0, flagname=FishCamID)  # configurações padrão

            BuzzerIdx += 1
            if BuzzerIdx == BuzzerIterationPeriod:
                BuzzerIdx = 0

    except BaseException as e:
        logging.error(str(e))

if __name__ == '__main__':
    main()
