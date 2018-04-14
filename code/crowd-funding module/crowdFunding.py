

import requests
import tweepy
from secrets import *




class justGiving():

    def __init__(self):

        self.Application_key = APPLICATION_KEY
        self.url = JUSTGIVING_URL 
        self.headers =  {'x-api-key':self.Application_key ,'Content-type':'application/json','Accept':'application/json'}




    def make_request(self,endpoint):

		

                
                url = self.url + '/' + endpoint

                

                try:

                    request = requests.get(url , headers = self.headers)

                except requests.exceptions.RequestException as e:
                    print(e)

                if (request.status_code == 200):

                        return request

		

    
    def get_amount_raised(self):
    
        endpoint = ''
        requested_data = self.make_request(endpoint)


        try:
            amount_raised = requested_data.json()['amountRaised']
            return amount_raised

        except AttributeError as e:
            print(e)
        

        return -1


    def get_donor_count(self):

    	endpoint = 'pledges'

    	requested_data = self.make_request(endpoint)


    	
        try:
    	    donor_count = requested_data.json()['totalCount']
            return donor_count

        except AttributeError as e:
            print(e)

    	return -1



    def get_donor_names(self):

        endpoint = 'pledges?pageSize=100'

        requested_data = self.make_request(endpoint)
        

        try: 
            pledges = requested_data.json()['pledges']

            donor_names =[]

            for pledge  in pledges:
    	        donor_names.append(pledge.get('donationName'))



            return donor_names
        except AttributeError as e:
            print(e)

        return -1




    def get_donations(self):

        endpoint = 'pledges?pageSize=100'

        requested_data = self.make_request(endpoint)

        try:
            pledges = requested_data.json()['pledges']

            donations = []

            for pledge in pledges:

        	    donation = []

        	    donation.append(pledge.get('donationName'))
        	    donation.append(pledge.get('donationAmount'))

        	    donations.append(donation)

            return donations
        except AttributeError as e:
            print(e)

        return -1



class main():

	def __init__(self):

		print('main')


		crowdfund = justGiving()

		print('amount raised ' , crowdfund.get_amount_raised())
		print('donor count ' , crowdfund.get_donor_count())
		print('donor names ' , crowdfund.get_donor_names())
		print('donations ' , crowdfund.get_donations())




if __name__ == "__main__":
        print ("starting...")
        main()











































