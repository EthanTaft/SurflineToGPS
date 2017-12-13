# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 01:50:52 2017

@author: Ethan
"""

import requests
import datetime
import pdb
import imaplib
import email
from twilio.rest import Client

#pdb.set_trace()
# Surfline API Base http://api.surfline.com/v1/forecasts/<subregion_id>


# Read emails for decision making in send_message()
def read_emails():
    
    FROM_EMAIL  = "#######"
    FROM_PWD    = "#######"
    SMTP_SERVER = "imap.gmail.com"
    
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL,FROM_PWD)
    mail.select("INBOX")
    result, data2 = mail.search(None, 
                                '(FROM "#######" SUBJECT "#######")')
    ids = data2[0]
    id_list = ids.split()
    latest_email_id = id_list[-1]
    result, email_data = mail.fetch(latest_email_id, "(RFC822)")
    
    raw_email = email_data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    
    email_text = list(email_message.walk())[1].get_payload()
    
    mail.close()
    
    return(email_text[0:2], email_text)
    
# Get data from surfline's API and send a text message
def send_message():
        
    if read_emails()[0] == "en":
        spot = [2158]
    elif read_emails()[0] == 'pr':
        spot = [2966]
    else:
        spot = [2158, 2966]
    
    ensenada = []
    punta_rosarito = []
    
    for spot_id in spot:
        
        # Make a get request
        response = requests.get("http://api.surfline.com/v1/forecasts/%s" %(spot_id))
        
        # Print the status code
        print(response.status_code) # if 200, everything went okay.
        
        # Get the jsondata and store as data
        data = response.json()
        
        # Get region names
        region = data["Location"]["subregionalias"]
        
        if region == "ensenada":
            surf_region = "EnSURF"
            per_region = "EnPER"
            wind_region = "EnWIND"
        else:
            surf_region = "PrSURF"
            per_region = "PrPER"
            wind_region = "PrPER"
        
        # Surf Data -----------------------------------------------------------
        surf_list = []

        for i in range(6): # 6 days out
            
            # Surf dates from JSON file from API
            surf_date = data["Surf"]["dateStamp"][i][0]
            
            # Get day information, i.e. mon
            surf_day = datetime.datetime.strptime(surf_date,
                                                  '%B %d, %Y %H:%M:%S').strftime('%a')
            
            # Get Height for today, mins and max, store in surf_height
            surf_min = data["Analysis"]["surfMin"][i]
            surf_max = data["Analysis"]["surfMax"][i]
            surf_height = "%s-%s" %(surf_min, surf_max)
            
            # Get surfText for today
            surf_text = data["Analysis"]["surfText"][i]
            
            # General height conditions
            gen_text = data["Analysis"]["generalText"][i].rstrip()
            
            # General swell conditions
            gen_cond = data["Analysis"]["generalCondition"][i]
            
            # Put day, height, and conditions into a string
            day_inf = "{}|{}|{}|{}|{}{}".format(surf_region, surf_day, 
                       surf_height, surf_text, gen_text, gen_cond)
           
            # Replace all ", " with "," and all ". " with "."
            day_inf = day_inf.replace(", ", ",").replace(". ", ".")
            surf_list.append(day_inf)
        
        # Direction and Period Data for swell directions 1 and 2 --------------
        dirper_list = []
        for k in range(6): # 8 days out, json indexed at 0 as well
            per_sentence = "%s|"%(per_region)
            for j in range(1, 3): # swell directions 1 and 2
                for i in range(4): # 3 times. 4AM, 10AM, 4PM
                    
                    # Swell period dates
                    per_date = data["Surf"]["dateStamp"][k][i]
                    
                    # Swell period days, i.e. Mon04AM
                    per_day = datetime.datetime.strptime(per_date,
                                                         "%B %d, %Y %H:%M:%S").strftime("%a%H%p")
                    
                    # Get direction in degrees
                    direc = data["Surf"]["swell_direction%s"%(j)][k][i]
                    
                    # Get period in seconds
                    period = data["Surf"]["swell_period%s"%(j)][k][i]
                    
                    # Put day, direction, and period into a string/sentence
                    day_time_per = "{},{},{}|".format(per_day, direc, period)
                    per_sentence = per_sentence + day_time_per
            
            # Append sentence to direction/period list
            dirper_list.append(per_sentence.rstrip(","))
        
        
        # Wind Data in knots --------------------------------------------------
        wind_list = []
        
        for i in range(6): # 8 days out
            wind_sentence = "%s|"%(wind_region)
            for j in range(8): # 8 times per day
                    
                # Get wind dates
                wind_date = data["Wind"]["dateStamp"][i][j]
                
                # Wind days/times i.e. Mon04AM
                wind_day = datetime.datetime.strptime(wind_date, 
                                                      "%B %d, %Y %H:%M:%S").strftime("%a%H%p")
                
                # Get wind speed in knots
                wind_speed = round(data["Wind"]["wind_speed"][i][j], 2)
                
                # Get wind direction
                wind_direc = int(round(data["Wind"]["wind_direction"][i][j], 0))
                
                # Put day, speed, and direction into a string, sentence
                wind = "{},{},{}|".format(wind_day, wind_speed,wind_direc)
                wind_sentence = wind_sentence + wind
            
            # Append sentence to wind list
            wind_list.append(wind_sentence.rstrip(","))
        
        # Put Results into a list based on region
        if region == "ensenada":
            ensenada.extend((surf_list, dirper_list, wind_list))
        else:
            punta_rosarito.extend((surf_list, dirper_list, wind_list))
            
            
    # Return based on spot input
    if spot == [2158]:
        return(ensenada)
    elif spot == [2966]:
        return(punta_rosarito)
    else:
        return(ensenada, punta_rosarito)



