from SimpleCV import *
import pyaudio
import sounddevice as sd
class AudioRecorder:
    def __init__(self):
        self.pAudio = pyaudio.PyAudio()
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.RECORD_SECONDS = 0.25
        self.CHUNK = 2 ** 11
        self.recentRecording = []

    def getVolumeUnits(self):
        data = self.getRecentRecording()
        peak = np.average(np.abs(data)) * 2
        bars = int(50 * peak / 2 ** 16)
        return bars

    def getRecentRecording(self):
        ##        return self.recentRecording
        return np.fromstring(self.recentRecording.read(self.CHUNK), dtype=np.int16)

    def record(self):
        # Learn what your OS+Hardware can do
        ##        defaultCapability = self.pAudio.get_default_host_api_info()
        ##        print defaultCapability
        ##
        ##        # See if you can make it do what you want
        ##        isSupported = self.pAudio.is_format_supported(input_format=self.FORMAT, input_channels=1, rate=self.RATE, input_device=0)
        ##        print isSupported
        ##        self.recentRecording = sd.rec(self.RECORD_SECONDS *  self.RATE,channels=1)
        try:
            self.recentRecording = self.pAudio.open(format=self.FORMAT, channels=1, rate=self.RATE, input=True,
                                                    frames_per_buffer=self.CHUNK)
            print("recording audio")
        except:
            print("not recording audio")

    def stop(self):
        self.recentRecording.stop_stream()
        self.recentRecording.close()
        self.pAudio.terminate()