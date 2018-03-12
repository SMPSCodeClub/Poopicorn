from PoopDisplay import PoopDisplay # import the PoopDisplay class definitionn


display= PoopDisplay()    # instantiate a PoopDisplay object
display.connect()         # connect to Scratch (
display.initialise()      # initialise numerals & sprites

display.test(2,100,5)   # simulate a set of donation updates
                        # (£2 received from 100 donors, 5 donations per seond)

totalPledged = 200
pledgeCount  = 100
display.update(totalPledged,pledgeCount)  # update Scratch display

display.jackpot()                         # trigger jackpot animation
