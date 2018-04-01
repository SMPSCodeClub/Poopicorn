import socket
import time
import sys

class PoopDisplay:

    # optional host & port values
    # defaults to localhost/42001 (local Scratch program)
    def __init__(self, host=None, port=None):
        if host is None:
            self.host = 'localhost'
        else:
             self.host = host 
        if port is None:
            self.port = 42002
        else:
             self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.total_pledged = 0
        self.donor_count = 0

    def connect(self):
        pass # deprecated method - connection (and disconnection) now occurs within sendCMD
    
    # create the TCP connection
    def sendCMD(self, cmd):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
        except Exception as msg:
            print ("Can't connect to Scratch. Have you started Scratch AND enabled remote sensors? %s " % msg )
            sys.exit(1)
        try:
            cmd = cmd
            self.socket.sendall(cmd.encode('UTF-8'))
            
            # Look for the response
            amount_received = 0
            amount_expected = len(cmd)

            while amount_received < amount_expected:
                data = self.socket.recv(1024)
                amount_received += len(data)
                print('received ' + data.decode())
        finally:
            self.socket.close()

    # zeros all numeric readings &
    # sends a signal to the display to trigger sprite initialisation
    def initialise(self):
        self.update(0, 0)
        self.sendCMD( 'initialise' )
        self.total_pledged = 0
        self.donor_count = 0
        
    # pass latest totals to the display
    # ARGUMENTS:
    #   total_pledged: amount of crowdfunding money raised so far
    #                  (rounded DOWN to nearest whole number of pounds)
    #   donor_count:   number of people who have pledged money
    def update (self, total_pledged=None, donor_count=None):
        if total_pledged is not None:
            self.sendCMD( 'total_pledged '  + str(total_pledged) )
            self.total_pledged = total_pledged            
        if donor_count is not None:
            self.sendCMD( 'donor_count '  + str(donor_count)  )
            self.donor_count = donor_count

    # pass latest totals to the display
    # ARGUMENTS:
    #   donor_name
    #   donor_amount (int - ££)
    def credit (self, donor_name, donor_amount):
            self.sendCMD( 'donor_name '  + str(donor_name)   )
            self.sendCMD( 'donor_amount '  + str(donor_amount) )
            self.sendCMD( 'donor_credit' )

    # simulates a set of donations coming in from a number of donors at a given frequency
    # default setting is £10 donations, 10 donors, once per second
    def test (self, donation_size=None, number_of_donors=None, frequency=None):
        # set up defaults for absent/silent parameters
        if donation_size is None:
            donation_size = 10
        if number_of_donors is None:
            number_of_donors = 10
        if frequency is None or frequency < 1:
            frequency = 1            
        donors = 0
        for x in range(0, number_of_donors):
            self.sendCMD( 'total_pledged '  + str(donors * donation_size) )
            self.sendCMD( 'donor_count '  + str(donors)     )
            donors = donors + 1
            time.sleep(1/frequency) # can never be zero divisor (frequency > 1)
    
    # send a signal to the display to trigger a jackpot animation
    # to co-incide with a marble waterfall
    def jackpot(self):
        self.sendCMD( 'jackpot' )
        