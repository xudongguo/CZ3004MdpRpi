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
#    self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    self.serversocket.bind((self.host, self.port))
#    self.serversocket.listen(1) #only connect up to 1 request

    # camera initialisation
    self.camera = PiCamera()
    self.camera.resolution = (640, 480)
    self.output = PiRGBArray(self.camera)

    # accept connection and extract IP address
#    (self.clientsocket, self.address) = self.serversocket.accept()
#    print("Connected to Image Reg PC")
#    self.cleanUp()

    # start camera preview to let camera warm up
    self.camera.start_preview()
    threading.Thread(target=time.sleep, args=(2,)).start()

  def connect(self):
    self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.serversocket.bind((self.host, self.port))
    self.serversocket.listen(1) #only connect up to 1 request

    (self.clientsocket, self.address) = self.serversocket.accept()
    print("Connected to Image Reg PC")
    self.cleanUp()

  def cleanUp(self):
    # free resources
    self.clientsocket.close()
    self.serversocket.close()

  def run(self):
    while True:
      self.camera.capture(self.output, 'bgr')
      img_arr = self.output.array
      data = pickle.dumps(img_arr)
      # send to PC/Laptop via HTTP POST
      r = requests.post("http://"+str(self.address[0])+":8123", data=data)
      print('Image', self.count , 'sent')
      self.output.truncate(0)
      self.count += 1
      time.sleep(0.5)

  # this functions take 2 pictures every time the robot moves
  def takePic(self):
    self.camera.capture(self.output, 'bgr')
    frame = self.output.array
    data = pickle.dumps(frame)
    # send to Laptop via HTTP POST
    #r = requests.post("http://"+str(self.address[0])+":8123", data=data)
    r = requests.post("http://192.168.16.133:8123", data=data) #static IP ver
    print("Image", self.count, "sent")
    self.output.truncate(0)
    self.count+=1
