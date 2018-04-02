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


def trigger_init():
    global PoopStatus
    print ("<<INITIALISING>>\n")
    PoopStatus.TotalPledged = 0
    PoopStatus.DisplayTotal = 0
    PoopStatus.DonorCount   = 0
    PoopStatus.DisplayCount = 0
    zero_display_count()    
    zero_display_total()    

def trigger_jackpot():
    print ("<JACKPOT>>\n")        

def trigger_credit():
    global PoopStatus
    print ( "Thankyou " + PoopStatus.LastDonorName +
            " for donating £" + PoopStatus.LastDonorAmount )

        
class mainThread (threading.Thread):
    
    def __init__( self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run( self ):
        global PoopStatus
        while True:
            if PoopStatus.Initialise == 1:
                trigger_init()
                PoopStatus.Initialise = 0
            if  PoopStatus.Jackpot == 1:
                trigger_jackpot()
                PoopStatus.Jackpot = 0

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
 
            #display client information
            #print ('Connected with ' + self.addr[0] + ':' + str(self.addr[1]))

            #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            self.threadCount += 1
            thread = clientThread(self.threadCount, self.conn)
            thread.start()
            thread.join()
        #s.close()


# Create new threads
main_thread          = mainThread(1)
main_thread.daemon   = True
socket_thread         = socketServerThread(2, '', 42001)
socket_thread.daemon = True

# Start new Threads
main_thread.start()
socket_thread.start()
#main_thread.join()   # DO NOT UNCOMMENT - BREAKS PYGAME
#socket_thread.join()   # DO NOT UNCOMMENT - BREAKS PYGAME


### STATIC SCOREBOARD BACKGROUND
scoreboard = Actor('scoreboard')
scoreboard.pos = 400, 125
scoreboard.costumes = ['scoreboard']
scoreboard.costume = 0
scoreboard.image = 'scoreboard'


### BACKGROUND IMAGES
background = Actor('bg-001')
background.pos = 400, 300
background.costumes = ['bg-001', 'bg-002', 'bg-003', 'bg-004', 'bg-005', 'bg-006', 'bg-007']
background.costume = 0
background.image = 'bg-001'


### DONOR COUNT NUMERALS
dcunits = Actor('0', anchor=('middle', 'bottom'))
dcunits.pos = 215, 190
dcunits.costumes = ['0','0-1-a','0-1-b','0-1-c',
                  '1','1-2-a','1-2-b','1-2-c',
                  '2','2-3-a','2-3-b','2-3-c',
                  '3','3-4-a','3-4-b','3-4-c',
                  '4','4-5-a','4-5-b','4-5-c',
                  '5','5-6-a','5-6-b','5-6-c',
                  '6','6-7-a','6-7-b','6-7-c',
                  '7','7-8-a','7-8-b','7-8-c',
                  '8','8-9-a','8-9-b','8-9-c',
                  '9','9-0-a','9-0-b','9-0-c']
dcunits.costume = 0
dcunits.current = 0
dcunits.image = '0'
dcunits.update = 0 # 0=static, 1=updating
dcunits.updateloops = 0

dctens = Actor('0', anchor=('middle', 'bottom'))
dctens.pos = 165, 190
dctens.costumes = ['0','0-1-a','0-1-b','0-1-c',
                  '1','1-2-a','1-2-b','1-2-c',
                  '2','2-3-a','2-3-b','2-3-c',
                  '3','3-4-a','3-4-b','3-4-c',
                  '4','4-5-a','4-5-b','4-5-c',
                  '5','5-6-a','5-6-b','5-6-c',
                  '6','6-7-a','6-7-b','6-7-c',
                  '7','7-8-a','7-8-b','7-8-c',
                  '8','8-9-a','8-9-b','8-9-c',
                  '9','9-0-a','9-0-b','9-0-c']
dctens.costume = 0
dctens.current = 0
dctens.image = '0'
dctens.update = 0
dctens.updateloops = 0

dchundreds = Actor('0', anchor=('middle', 'bottom'))
dchundreds.pos = 115, 190
dchundreds.costumes = ['0','0-1-a','0-1-b','0-1-c',
                  '1','1-2-a','1-2-b','1-2-c',
                  '2','2-3-a','2-3-b','2-3-c',
                  '3','3-4-a','3-4-b','3-4-c',
                  '4','4-5-a','4-5-b','4-5-c',
                  '5','5-6-a','5-6-b','5-6-c',
                  '6','6-7-a','6-7-b','6-7-c',
                  '7','7-8-a','7-8-b','7-8-c',
                  '8','8-9-a','8-9-b','8-9-c',
                  '9','9-0-a','9-0-b','9-0-c']
dchundreds.costume = 0
dchundreds.current = 0
dchundreds.image = '0'
dchundreds.update = 0
dchundreds.updateloops = 0


### TOTALISER NUMERALS
units = Actor('0', anchor=('middle', 'bottom'))
units.pos = 690, 190
units.costumes = ['0','0-1-a','0-1-b','0-1-c',
                  '1','1-2-a','1-2-b','1-2-c',
                  '2','2-3-a','2-3-b','2-3-c',
                  '3','3-4-a','3-4-b','3-4-c',
                  '4','4-5-a','4-5-b','4-5-c',
                  '5','5-6-a','5-6-b','5-6-c',
                  '6','6-7-a','6-7-b','6-7-c',
                  '7','7-8-a','7-8-b','7-8-c',
                  '8','8-9-a','8-9-b','8-9-c',
                  '9','9-0-a','9-0-b','9-0-c']
units.costume = 0
units.current = 0
units.image = '0'
units.update = 0 # 0=static, 1=updating
units.updateloops = 0

tens = Actor('0', anchor=('middle', 'bottom'))
tens.pos = 640, 190
tens.costumes = ['0','0-1-a','0-1-b','0-1-c',
                  '1','1-2-a','1-2-b','1-2-c',
                  '2','2-3-a','2-3-b','2-3-c',
                  '3','3-4-a','3-4-b','3-4-c',
                  '4','4-5-a','4-5-b','4-5-c',
                  '5','5-6-a','5-6-b','5-6-c',
                  '6','6-7-a','6-7-b','6-7-c',
                  '7','7-8-a','7-8-b','7-8-c',
                  '8','8-9-a','8-9-b','8-9-c',
                  '9','9-0-a','9-0-b','9-0-c']
tens.costume = 0
tens.current = 0
tens.image = '0'
tens.update = 0
tens.updateloops = 0

hundreds = Actor('0', anchor=('middle', 'bottom'))
hundreds.pos = 590, 190
hundreds.costumes = ['0','0-1-a','0-1-b','0-1-c',
                  '1','1-2-a','1-2-b','1-2-c',
                  '2','2-3-a','2-3-b','2-3-c',
                  '3','3-4-a','3-4-b','3-4-c',
                  '4','4-5-a','4-5-b','4-5-c',
                  '5','5-6-a','5-6-b','5-6-c',
                  '6','6-7-a','6-7-b','6-7-c',
                  '7','7-8-a','7-8-b','7-8-c',
                  '8','8-9-a','8-9-b','8-9-c',
                  '9','9-0-a','9-0-b','9-0-c']
hundreds.costume = 0
hundreds.current = 0
hundreds.image = '0'
hundreds.update = 0
hundreds.updateloops = 0

thousands = Actor('0', anchor=('middle', 'bottom'))
thousands.pos = 540, 190
thousands.costumes = ['0','0-1-a','0-1-b','0-1-c',
                  '1','1-2-a','1-2-b','1-2-c',
                  '2','2-3-a','2-3-b','2-3-c',
                  '3','3-4-a','3-4-b','3-4-c',
                  '4','4-5-a','4-5-b','4-5-c',
                  '5','5-6-a','5-6-b','5-6-c',
                  '6','6-7-a','6-7-b','6-7-c',
                  '7','7-8-a','7-8-b','7-8-c',
                  '8','8-9-a','8-9-b','8-9-c',
                  '9','9-0-a','9-0-b','9-0-c']
thousands.costume = 0
thousands.current = 0
thousands.image = '0'
thousands.update = 0
thousands.updateloops = 0

tenthousands = Actor('0', anchor=('middle', 'bottom'))
tenthousands.pos = 490, 190
tenthousands.costumes = ['0','0-1-a','0-1-b','0-1-c',
                  '1','1-2-a','1-2-b','1-2-c',
                  '2','2-3-a','2-3-b','2-3-c',
                  '3','3-4-a','3-4-b','3-4-c',
                  '4','4-5-a','4-5-b','4-5-c',
                  '5','5-6-a','5-6-b','5-6-c',
                  '6','6-7-a','6-7-b','6-7-c',
                  '7','7-8-a','7-8-b','7-8-c',
                  '8','8-9-a','8-9-b','8-9-c',
                  '9','9-0-a','9-0-b','9-0-c']
tenthousands.costume = 0
tenthousands.current = 0
tenthousands.image = '0'
tenthousands.update = 0
tenthousands.updateloops = 0

### MAIN CHARACTER SPRITE (RatVaark)
ratvaark = Actor('ratvaark01')
ratvaark.pos = 125, 410
ratvaark.costumes = ['ratvaark01', 'ratvaark02', 'ratvaark03','ratvaark04', 'ratvaark05', 'ratvaark06','ratvaark07','ratvaark06', 'ratvaark05', 'ratvaark04','ratvaark03', 'ratvaark02']
ratvaark.talk = ['ratvaarkup','ratvaarkdown']
ratvaark.costume = 0
ratvaark.framecount = 0
ratvaark.up = 0
ratvaark.talkframe = 0

### MAIN CHARACTER SPEECH BUBBLES (for donor credits)
speechbubble = Actor('speechbubblegone')
speechbubble.pos = 500, 335
speechbubble.costumes = ['speechbubblegone', 'speechbubbleleft', 'speechbubbleright']
speechbubble.credits = ['Hello.\nWelcome to the POOPICORN!\nI am RATVAARK',
                        'PROJECT CREATOR\nEmma Bearman\n@EmmaMBearman',
                        'MACHINE DESIGN\nAlfred Chow\n@Maker_of_Things',
                        'DISPLAY DESIGN\nLaurence Molloy\n@MolloyLaurence',
                        'DATA COLLECTION\nCatherine Jones\n@M_Fkill',
                        'PARTS SUPPLY\nTanya Fish\n@tanurai',
                        'ELECTRONICS CONTROL\nLes Pounder\n@biglesp',
                        'VAARKS & BISCUITS\nSue Archer\n@SueArcher6']
speechbubble.costume = 0
speechbubble.credit = -1


def draw():
    screen.fill((128, 0, 0))
    background.draw()
    scoreboard.draw()
    ratvaark.draw()
    dcunits.draw()
    dctens.draw()
    dchundreds.draw()
    units.draw()
    tens.draw()
    hundreds.draw()
    thousands.draw()
    tenthousands.draw()
    speechbubble.draw()
    CreditText = (  "Thankyou " + PoopStatus.LastDonorName +
                    "\nfor donating £" + str(PoopStatus.LastDonorAmount) )
    if speechbubble.costume == 1:
       screen.draw.text(CreditText,
                            center = (ratvaark.x - 260, ratvaark.y - 115),
                            width=285, fontsize=32,
                            color="#FFFFFF", gcolor="#66AA00", owidth=1.5, ocolor="black", alpha=0.8)
    elif speechbubble.costume == 2:
        screen.draw.text(CreditText,
                            center = (ratvaark.x + 285, ratvaark.y - 115),
                            width=285, fontsize=32,
                            color="#FFFFFF", gcolor="#66AA00", owidth=1.5, ocolor="black", alpha=0.8)


def update():
    global PoopStatus
    if PoopStatus.Initialise == 0:
        if ratvaark.talkframe == 1:
            ratvaark.talkframe += 1
            clock.schedule(ratvaark_speech_bubble,0.4)
            clock.schedule_interval(ratvaark_talk, 0.2)
        elif ratvaark.talkframe == 0:
            ratvaark_animate()
        if (PoopStatus.TotalPledged > PoopStatus.DisplayTotal) and units.update == 0:
            units.update = 1
            units.updateloops = 4
            update_distance = (PoopStatus.TotalPledged - PoopStatus.DisplayTotal) * 4
            if units.updateloops > 0:
                update_speed = min( max( (4/update_distance), 0.01 ), 0.1 )
                clock.schedule_interval(update_unit,update_speed)
        if (PoopStatus.DonorCount > PoopStatus.DisplayCount) and dcunits.update == 0:
            dcunits.update = 1
            dcunits.updateloops = 4
            if dcunits.updateloops > 0:
                clock.schedule_interval(update_dcunit,0.1)
        if (PoopStatus.DonorCredit == 1) and ratvaark.talkframe == 0:
            PoopStatus.DonorCredit = 0
            ratvaark.talkframe = 1


def zero_display_count():
    dcunits.costume    =  0
    dcunits.image      = '0'
    dctens.costume     =  0
    dctens.image       = '0'
    dchundreds.costume =  0
    dchundreds.image   = '0'


def zero_display_total():
    units.costume        =  0
    units.image          = '0'
    tens.costume         =  0
    tens.image           = '0'
    hundreds.costume     =  0
    hundreds.image       = '0'
    thousands.costume    =  0
    thousands.image      = '0'
    tenthousands.costume =  0
    tenthousands.image   = '0'


def update_dcunit():
    global PoopStatus
    dcunits.pos = 215, 190
    if dcunits.updateloops > 0:
        dcunits.costume += 1
        if dcunits.costume == len(dcunits.costumes) - 2:
            dctens.updateloops = 4
            clock.schedule_interval(update_dctens, 0.1)
        if dcunits.costume == len(dcunits.costumes):
            dcunits.costume = 0
        dcunits.image = dcunits.costumes[dcunits.costume]
        dcunits.updateloops -= 1
    else:
        clock.unschedule(update_dcunit)
        PoopStatus.DisplayCount += 1
        dcunits.update = 0


def update_dctens():
    dctens.pos = 165, 190
    if dctens.updateloops > 0:
        dctens.costume += 1
        if dctens.costume == len(dctens.costumes) - 2:
            dchundreds.updateloops = 4
            clock.schedule_interval(update_dchundreds, 0.1)
        if dctens.costume == len(dctens.costumes):
            dctens.costume = 0
        dctens.image = dctens.costumes[dctens.costume]
        dctens.updateloops -= 1
    else:
        clock.unschedule(update_dctens)


def update_dchundreds():
    dchundreds.pos = 115, 190
    if dchundreds.updateloops > 0:
        dchundreds.costume += 1
        if dchundreds.costume == len(dchundreds.costumes):
            dchundreds.costume = 0
        dchundreds.image = dchundreds.costumes[dchundreds.costume]
        dchundreds.updateloops -= 1
    else:
        clock.unschedule(update_dchundreds)


def update_unit():
    global PoopStatus
    units.pos = 690, 190
    if units.updateloops > 0:
        units.costume += 1
        if units.costume == len(units.costumes) - 2:
            tens.updateloops = 4
            clock.schedule_interval(update_tens, 0.1)
        if units.costume == len(units.costumes):
            units.costume = 0
        units.image = units.costumes[units.costume]
        units.updateloops -= 1
    else:
        clock.unschedule(update_unit)
        PoopStatus.DisplayTotal += 1
        units.update = 0


def update_tens():
    tens.pos = 640, 190
    if tens.updateloops > 0:
        tens.costume += 1
        if tens.costume == len(tens.costumes) - 2:
            hundreds.updateloops = 4
            clock.schedule_interval(update_hundreds, 0.1)
        if tens.costume == len(tens.costumes):
            tens.costume = 0
        tens.image = tens.costumes[tens.costume]
        tens.updateloops -= 1
    else:
        clock.unschedule(update_tens)


def update_hundreds():
    hundreds.pos = 590, 190
    if hundreds.updateloops > 0:
        hundreds.costume += 1
        if hundreds.costume == len(hundreds.costumes) - 2:
            thousands.updateloops = 4
            clock.schedule_interval(update_thousands, 0.1)
        if hundreds.costume == len(hundreds.costumes):
            hundreds.costume = 0
        hundreds.image = hundreds.costumes[hundreds.costume]
        hundreds.updateloops -= 1
    else:
        clock.unschedule(update_hundreds)


def update_thousands():
    thousands.pos = 540, 190
    if thousands.updateloops > 0:
        thousands.costume += 1
        if thousands.costume == len(thousands.costumes) - 2:
            tenthousands.updateloops = 4
            clockschedule_interval(update_tenthousands, 0.1)
        if thousands.costume == len(thousands.costumes):
            thousands.costume = 0
        thousands.image = thousands.costumes[thousands.costume]
        thousands.updateloops -= 1
    else:
        clock.unschedule(update_thousands)


def update_tenthousands():
    tenthousands.pos = 490, 190
    if tenthousands.updateloops > 0:
        tenthousands.costume += 1
        if tenthousands.costume == len(tenthousands.costumes):
            tenthousands.costume = 0
        tenthousands.image = tenthousands.costumes[tenthousands.costume]
        tenthousands.updateloops -= 1
    else:
        clock.unschedule(update_tenthousands)


def ratvaark_animate():
    ratvaark.framecount += 1
    if ratvaark.framecount % 8 == 0: 
        ratvaark_nod()
        ratvaark_walk()
        ratvaark_waddle()


def ratvaark_speech_bubble():
    if ratvaark.x > 375:
        speechbubble.x = ratvaark.x - 225
        speechbubble.y = ratvaark.y - 75
        speechbubble.costume = 1
        speechbubble.image = speechbubble.costumes[speechbubble.costume]
    else:
        speechbubble.x = ratvaark.x + 250
        speechbubble.y = ratvaark.y - 75
        speechbubble.costume = 2
        speechbubble.image = speechbubble.costumes[speechbubble.costume]
    

def ratvaark_talk():
    if ratvaark.costume >= len(ratvaark.talk):
        ratvaark.costume = 0
    ratvaark.image = ratvaark.talk[ratvaark.costume]
    ratvaark.costume += 1
    ratvaark.talkframe += 1
    if ratvaark.talkframe == 20:
        clock.unschedule(ratvaark_talk)
        ratvaark.talkframe = 0
        speechbubble.costume = 0
        speechbubble.image = speechbubble.costumes[speechbubble.costume]


def ratvaark_walk():
    ratvaark.x += 8
    if ratvaark.x > 700:
        background.costume += 1
        if background.costume >= len(background.costumes):
            background.costume = 0
        background.image = background.costumes[background.costume]
        ratvaark.x = 125


def ratvaark_nod():
    ratvaark.costume += 1
    if ratvaark.costume == len(ratvaark.costumes):
        ratvaark.costume = 0
    ratvaark.image = ratvaark.costumes[ratvaark.costume]


def ratvaark_waddle():
    if ratvaark.up == 0:
        ratvaark.y += 8
        ratvaark.up += 1
    elif ratvaark.up == 1:
        ratvaark.y += 4
        ratvaark.up += 1
    elif ratvaark.up == 2:
        ratvaark.y += 2
        ratvaark.up += 1        
    else:
        ratvaark.y -= 14
        ratvaark.up = 0
