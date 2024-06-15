# Python script for Amazon product availability checker
# importing libraries
from lxml import html
import requests
from time import sleep
import time
import schedule
import smtplib 


receiver_email_id = "EMAIL_ID_OF_USER"


def check(url):
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
	
	
	page = requests.get(url, headers = headers) 
	for i in range(20):
		
		sleep(3) 
		
		
		doc = html.fromstring(page.content)
		
		
		XPATH_AVAILABILITY = '//div[@id ="availability"]//text()'
		RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
		AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
		return AVAILABILITY

	
def sendemail(ans, product):
	GMAIL_USERNAME = "chaitanyasingj0412@gmail.com"
	GMAIL_PASSWORD = "Sand0412@@@@@"
	
	recipient = receiver_email_id
	body_of_email = ans
	email_subject = product + ' product availability'
	
	
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	
	
	s.starttls() 
	
	
	s.login(GMAIL_USERNAME, GMAIL_PASSWORD) 
	
	
	headers = "\r\n".join(["from: " + GMAIL_USERNAME,
						"subject: " + email_subject,
						"to: " + recipient,
						"mime-version: 1.0",
						"content-type: text/html"])

	content = headers + "\r\n\r\n" + body_of_email
	s.sendmail(GMAIL_USERNAME, recipient, content)
	s.quit() 


def ReadAsin():
	
	Asin = 'B077PWK5BT'
	url = "https://www.amazon.in/AVVATAR-WHEY-PROTEIN-Unflavoured-Fresh/dp/B09K3BXLBC/ref=pd_ci_mcx_mh_mcx_views_1?pd_rd_w=Nm7O7&content-id=amzn1.sym.8d778d03-46f9-4c13-9e9c-08bc8c339f2c%3Aamzn1.symc.ca948091-a64d-450e-86d7-c161ca33337b&pf_rd_p=8d778d03-46f9-4c13-9e9c-08bc8c339f2c&pf_rd_r=WFD7EHY58TM2V3B3849V&pd_rd_wg=A2Iz8&pd_rd_r=52aa9d91-45e5-49f4-9500-c024da1bac8b&pd_rd_i=B09K3BXLBC" + Asin
	print ("Processing: "+url)
	ans = check(url)
	arr = [
		'Only 1 left in stock.',
		'Only 2 left in stock.',
		'In stock.']
	print(ans)
	if ans in arr:
		
		sendemail(ans, Asin) 


def job():
	print("Tracking....") 
	ReadAsin()

schedule.every(1).minutes.do(job)

while True:
	
	
	schedule.run_pending() 
	time.sleep(1)
