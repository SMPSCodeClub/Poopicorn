import crowdFunding 
from PoopDisplay import PoopDisplay
import poop_tweet

import time
import pickle
import random




class main():
        def __init__(self):
                #The time between checking for crowdfunding updates
                self.time_delay = 60
                self.tweet_text = ['The latest total is  ','Wow! we have raised ',  'The total so far is ', 'Thankyou to all our donors, we have raised ']
                self.total_file = 'total_file.txt'
                self.total_crowfund_url = 'https://www.justgiving.com/crowdfunding/playfulanywhere'

        def run_machine(self):
                current_time = time.time()

                #Get the current Crowdfunding total
                crowdfund = crowdFunding.justGiving()

                total = str(crowdfund.get_amount_raised())
                
                
                print('total = ', total)

                #Save the total raised to a file

                with open(self.total_file, 'w+') as total_File_Object:
                        

                        total_File_Object.write(total)

                total_File_Object.close()
    	
                while(1):


                        if time.time() > current_time + self.time_delay:
                
                                #Get the current Crowdfunding data
                                crowdfund = crowdFunding.justGiving()
                
                                total = str(crowdfund.get_amount_raised())
                                
                
                                donations = crowdfund.get_donations()
                
                                latest_donation = donations[0]
                
                                latest_donor_name = latest_donation[0]
                
                                latest_donor_amount = latest_donation[1]
                                

                                #open the saved total file

                                cached_total = 0

                                with open(self.total_file, 'r') as total_File_Object:
                                

                                    cached_total = total_File_Object.read()
        
                                total_File_Object.close()

                                print('cached total = ' + cached_total)
                



                                #compare this with the cached amount
                                #Do all the updates if the total amount has increased

                                if total > cached_total:

                                        #ACTIVATE THE MOTOR
                                        print('activating the motor')
                                        



                                        ## END OF MOTOR ACTIVATE


                                        #ACTIVATE THE LEDS
                                        print('activate the LEDs')


                                        ##END OF ACTIVATE THE LEDS



                                        #UPDATE THE DISPLAY
                                        print('updating display')
                                        display = PoopDisplay()
                                        display.connect()
                                        display.initialise()

                                        display.Update(total, donors)

                                        display.credit(latest_donor_name , latest_donor_amount )

                                        ## END OF DISPLAY UPDATE
                                        



                                        #Send to twitter
                                        print('Sending tweet')
                                        tweet = poop_tweet.PoopTweet()


                                        if latest_donor_name


                                        

                                        tweet.send_tweet(random.choice(self.tweet_text) + '£' + str(total) +' our latest donation is £' +  str(latest_donor_amount) +  ' donated by ' + latest_donor_name +
                                                         ' help us bring more play to Leeds by donating at  '+ self.total_crowfund_url )



                                        #Save the new total to file
                                        with open(self.total_file, 'w+') as total_File_Object:
                                                

                                                total_File_Object.write(total)
                        
                                        total_File_Object.close()

                                #Update the current time
                                current_time = time.time()


                                        




if __name__ == "__main__":
    print ("starting main...")
    poopicornMain = main()
    poopicornMain.run_machine()







