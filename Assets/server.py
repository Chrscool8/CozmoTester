# Created by Youssef Elashry to allow two-way communication between Python3 and Unity to send and receive strings

# Feel free to use this in your individual or commercial projects BUT make sure to reference me as: Two-way communication between Python 3 and Unity (C#) - Y. T. Elashry
# It would be appreciated if you send me how you have used this in your projects (e.g. Machine Learning) at youssef.elashry@gmail.com

# Use at your own risk
# Use under the Apache License 2.0

# Example of a Python UDP server

# Created by Youssef Elashry to allow two-way communication between Python3 and Unity to send and receive strings

# Feel free to use this in your individual or commercial projects BUT make sure to reference me as: Two-way communication between Python 3 and Unity (C#) - Y. T. Elashry
# It would be appreciated if you send me how you have used this in your projects (e.g. Machine Learning) at youssef.elashry@gmail.com

# Use at your own risk
# Use under the Apache License 2.0
import UnityEngine;

class UdpComms():
    def __init__(self,udpIP,portTX,portRX,enableRX=False,suppressWarnings=True):
        """
        Constructor
        :param udpIP: Must be string e.g. "127.0.0.1"
        :param portTX: integer number e.g. 8000. Port to transmit from i.e From Python to other application
        :param portRX: integer number e.g. 8001. Port to receive on i.e. From other application to Python
        :param enableRX: When False you may only send from Python and not receive. If set to True a thread is created to enable receiving of data
        :param suppressWarnings: Stop printing warnings if not connected to other application
        """

        import socket

        self.udpIP = udpIP
        self.udpSendPort = portTX
        self.udpRcvPort = portRX
        self.enableRX = enableRX
        self.suppressWarnings = suppressWarnings # when true warnings are suppressed
        self.isDataReceived = False
        self.dataRX = None

        # Connect via UDP
        self.udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # internet protocol, udp (DGRAM) socket
        self.udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allows the address/port to be reused immediately instead of it being stuck in the TIME_WAIT state waiting for late packets to arrive.
        self.udpSock.bind((udpIP, portRX))

        # Create Receiving thread if required
        if enableRX:
            import threading
            self.rxThread = threading.Thread(target=self.ReadUdpThreadFunc, daemon=True)
            self.rxThread.start()

    def __del__(self):
        self.CloseSocket()

    def CloseSocket(self):
        # Function to close socket
        self.udpSock.close()

    def SendData(self, strToSend):
        # Use this function to send string to C#
        self.udpSock.sendto(bytes(strToSend,'utf-8'), (self.udpIP, self.udpSendPort))

    def ReceiveData(self):
        """
        Should not be called by user
        Function BLOCKS until data is returned from C#. It then attempts to convert it to string and returns on successful conversion.
        An warning/error is raised if:
            - Warning: Not connected to C# application yet. Warning can be suppressed by setting suppressWarning=True in constructor
            - Error: If data receiving procedure or conversion to string goes wrong
            - Error: If user attempts to use this without enabling RX
        :return: returns None on failure or the received string on success
        """
        if not self.enableRX: # if RX is not enabled, raise error
            raise ValueError("Attempting to receive data without enabling this setting. Ensure this is enabled from the constructor")

        data = None
        try:
            data, _ = self.udpSock.recvfrom(1024)
            data = data.decode('utf-8')
        except WindowsError as e:
            if e.winerror == 10054: # An error occurs if you try to receive before connecting to other application
                if not self.suppressWarnings:
                    print("Are You connected to the other application? Connect to it!")
                else:
                    pass
            else:
                raise ValueError("Unexpected Error. Are you sure that the received data can be converted to a string")

        return data

    def ReadUdpThreadFunc(self): # Should be called from thread
        """
        This function should be called from a thread [Done automatically via constructor]
                (import threading -> e.g. udpReceiveThread = threading.Thread(target=self.ReadUdpNonBlocking, daemon=True))
        This function keeps looping through the BLOCKING ReceiveData function and sets self.dataRX when data is received and sets received flag
        This function runs in the background and updates class variables to read data later

        """

        self.isDataReceived = False # Initially nothing received

        while True:
            data = self.ReceiveData()  # Blocks (in thread) until data is returned (OR MAYBE UNTIL SOME TIMEOUT AS WELL)
            self.dataRX = data # Populate AFTER new data is received
            self.isDataReceived = True
            # When it reaches here, data received is available

    def ReadReceivedData(self):
        """
        This is the function that should be used to read received data
        Checks if data has been received SINCE LAST CALL, if so it returns the received string and sets flag to False (to avoid re-reading received data)
        data is None if nothing has been received
        :return:
        """

        data = None

        if self.isDataReceived: # if data has been received
            self.isDataReceived = False
            data = self.dataRX
            self.dataRX = None # Empty receive buffer

        return data


#import UdpComms as U
import time

# Create UDP socket to use for sending (and receiving)
sock = UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)

from multiprocessing import Process
import os

def countloop():
    i = 0

    while True:
        UnityEngine.Debug.Log('hello world')
        sock.SendData('Sent from Python: ' + str(i)) # Send this string to other application
        i += 1

        data = sock.ReadReceivedData() # read data

        if data != None: # if NEW data has been received since last ReadReceivedData function call
            print(data) # print new received data

        time.sleep(1)

        if i > 3:
            break

pid = os.fork()
if (pid == 0): # The first child.
    os.chdir("/")
    os.setsid()
    os.umask(0)
    pid2 = os.fork()
    if (pid2 == 0):  # Second child
        countloop()
    else:
        sys.exit()    #First child exists
else:         # Parent Code
    sys.exit()   # Parent exists


#if __name__ == '__main__':
#p1 = Process(target=countloop)
#p1.start()
#p1.join()