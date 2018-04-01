import pygame
import threading
import time
import socket
import sys
import re

class PoopStatus:
    def __init__(self):
        self.Screenwidth     = 800
        self.ScreenHeight    = 600
        self.FrameCount      =   0
        self.DonorCount      =   0
        self.DisplayCount    =   0
        self.TotalPledged    =   0
        self.DisplayTotal    =   0
        self.LastDonorName   =  ''
        self.LastDonorAmount =   0
        self.DonorCredit     =   0
        self.Initialise      =   0
        self.Jackpot         =   0
        
PoopStatus = PoopStatus()
exitFlag = 0
        
class clientThread (threading.Thread):
    def __init__(self, threadID, connection):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.conn = connection

    def run ( self ):
        #Function for handling connections. This will be used to create threads
        global PoopStatus

        #infinite loop so that function do not terminate and thread do not end.
        while True:
         
            #Receiving from client
            data = self.conn.recv(1024).decode().rstrip()

            total_pledged = re.search('(?<=total_pledged )\d+$', data)
            donor_count   = re.search('(?<=donor_count )\d+$'  , data)
            donor_name    = re.search('(?<=donor_name ).*$'    , data)
            donor_amount  = re.search('(?<=donor_amount )\d+$' , data)
            donor_credit  = re.search('donor_credit'           , data)
            initialise    = re.search('initialise'             , data)
            jackpot       = re.search('jackpot'                , data)
                        
            if initialise:
                #print ('INITIALISING...')
                    PoopStatus.Initialise = 1

            if jackpot:
                #print ('JACKPOT!')
                    PoopStatus.Jackpot = 1


            if total_pledged:
                if int(total_pledged.group(0)) > PoopStatus.TotalPledged:
                    PoopStatus.TotalPledged = int(total_pledged.group(0))
                    print ("TOTAL = " + str(PoopStatus.TotalPledged))


            if donor_count:
                if int(donor_count.group(0)) > PoopStatus.DonorCount:
                    PoopStatus.DonorCount = int(donor_count.group(0))
                    print ("COUNT = " + str(PoopStatus.DonorCount))

            if donor_name:
                PoopStatus.LastDonorName = donor_name.group(0)

            if donor_amount:
                PoopStatus.LastDonorAmount = donor_amount.group(0)

            if donor_credit:
                PoopStatus.DonorCredit = 1

            if data:
                #print ("[" + data + "]")
                self.conn.sendall(data.encode('UTF-8'))
            else: 
                break
          
        #came out of loop
        self.conn.close()


class socketServerThread (threading.Thread):
    def __init__( self, threadID, host, portNumber ):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.host = host
        self.portNumber = portNumber
        self.conn = ''
        self.addr = ''
        self.threadCount = threadID

    def run( self ): 
        # socket configuration
        HOST = self.host       # '' = symbolic name, meaning all available interfaces
        PORT = self.portNumber # Arbitrary non-privileged port

        try:
            #create an AF_INET, STREAM socket (TCP)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as msg:
            print ('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
            sys.exit();

        print ('Socket Created')

        try:
            s.bind((HOST, PORT))
        except socket.error as msg:
            print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()
     
        print ('Socket bind complete')

        s.listen(10)
        print ('Socket now listening')

        #now keep talking with the client
        while 1:
            #wait to accept a connection - blocking call
            self.conn, self.addr = s.accept()
 
            #start new client thread
            self.threadCount += 1
            thread = clientThread(self.threadCount, self.conn)
            thread.start()
            thread.join()
        s.close()


# Create new threads
thread1 = socketServerThread(2, '', 42002)
thread1.daemon = True

# Start new Threads
thread1.start()
#thread1.join()

### BACKGROUND IMAGES
background = Actor('bg-001')
background.pos = 400, 300

def draw():
    screen.fill((128, 0, 0))
    background.draw()