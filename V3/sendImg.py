import socket, time, pickle, requests, threading
from picamera import PiCamera
from picamera.array import PiRGBArray
from params import WIFI_IP, IMGREG_PORT

class sendImg:
  host=WIFI_IP
  port=IMGREG_PORT

  def __init__(self, host=WIFI_IP, port=IMGREG_PORT):
    self.host = host
    self.port = port
    self.count = 0

    # camera initialisation
    self.camera = PiCamera()
    self.camera.resolution = (640, 480)
    self.output = PiRGBArray(self.camera)

    # start camera preview to let camera warm up
    self.camera.start_preview()
    threading.Thread(target=time.sleep, args=(2,)).start()

  # this function takes a picture when commanded
  def takePic(self):
    self.camera.capture(self.output, 'bgr')
    frame = self.output.array
    data = pickle.dumps(frame)
    # send to Laptop via HTTP POST
    r = requests.post("http://192.168.16.133:8123", data=data) #static IP
    print("Image", self.count, "sent")
    self.output.truncate(0)
    self.count+=1
