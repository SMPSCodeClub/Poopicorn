from PoopDisplayPython import PoopDisplay # import the PoopDisplay class definitionn


display= PoopDisplay()    # instantiate a PoopDisplay object
display.connect()         # connect to Scratch (
display.initialise()      # initialise numerals & sprites

display.test(2,100,5)   # simulate a set of donation updates
                        # (£2 received from 100 donors, 5 donations per seond)

totalPledged = 500
pledgeCount  = 200
display.update(totalPledged,pledgeCount)  # update Scratch display


display.credit("Ermintrude", 50)          # trigger an on-screen donor mention
display.jackpot()                         # trigger jackpot animation
