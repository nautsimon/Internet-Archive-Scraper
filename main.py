import sys
from random import randint
import time
from time import sleep
import os
import pandas as pd
from pandas import ExcelFile
import shutil
import requests
from selenium import webdriver


email = "simonm@uchicago.edu"
password = "Abc123456"
awardName = input("what is the name of the Award?")
startIndex = input("start at certain index?")
browser = webdriver.Firefox()

#Login to Internet Archive
browser.get("https://archive.org/account/login")
email_input = browser.find_element_by_xpath('/html/body/div[1]/main/div/div/div[2]/section[2]/form/label[1]/input')
email_input.send_keys(email)
password_input = browser.find_element_by_xpath('/html/body/div[1]/main/div/div/div[2]/section[2]/form/label[2]/div/input')
password_input.send_keys(password)
browser.find_element_by_xpath('/html/body/div[1]/main/div/div/div[2]/section[2]/form/input[3]').click()
sleep(randint(1,2))
leftImgPath = '/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div[2]/div[2]/div[1]/div[1]/img[2]' #for first to0
rightImgPath = '/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div[2]/div[2]/div[1]/div[1]/img[1]' #for last too


def getImages(imgPath, imgXPath):
	sleep(1)
	try:
		imgPath = imgPath.encode("utf-8")
	except:
		print("already a string")

	try:
		browser.find_element_by_xpath(imgXPath).get_attribute("src")
	except:
		sleep(2)
		try:
			browser.find_element_by_xpath(imgXPath).get_attribute("src")
		except:
			print("Alt")
			imgXPath = imgXPath.split("img[")[-1]
			if("2" in imgXPath):
				imgXPath = "/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[6]/img"
			else:
				imgXPath = "/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[5]/img"

	imgStartTime = time.time()
	urlImg = browser.find_element_by_xpath(imgXPath).get_attribute("src")
	urlImg = urlImg.split("scale=")
	try:
		urlImg = str(urlImg[0]) + "scale=1" + str(urlImg[1])[1:]
	except:
		print("transparent")

	cookie = browser.execute_script("return document.cookie")
	headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Connection': 'keep-alive', 'Cookie': cookie, 'Upgrade-Insecure-Requests': '1', 'Cache-Control': 'max-age=0'}
	session = requests.Session()
	response = session.get(urlImg, headers=headers, stream=True)
	try:
		print(imgPath.decode("utf-8").split("/")[-1], "downloaded in",  round(time.time() - imgStartTime, 2), "seconds", end="\r")
	except:
		print(imgPath, " downloaded in ",  round(time.time() - imgStartTime, 2), " seconds")

	if response.status_code == 200:
		
    		with open(imgPath, 'wb') as f:
        		response.raw.decode_content = True
        		shutil.copyfileobj(response.raw, f)  
		
	else:
		try:
		  	borrowButtPath = browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[2]/button')
		except:
			sleep(4)
			try:
		  		borrowButtPath = browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[2]/button')

			except:
				print("trying alt method...")
				try:
		  			borrowButtPath = browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[2]/div[1]/button[1]')
				except:
					print("No borrowing toggle. Trying page manipulation...")
					borrowButtPath = ""
		try:
			buttText = borrowButtPath.text
		except:
			print("=====No Borrow Function=====")
			
		if("Borrow" in buttText or "borrow" in buttText or "rent" in buttText):
				if "unavailable" not in buttText:			
					print("Borrowing...")				
					borrowButtPath.click()
					borrowing = True
					sleep(10)	
		else:
			print("Borrowing function not availible")	
			



#Loading and prepping dataframe
df = pd.read_excel("./resources/" + awardName +"Excel.xlsx", encoding="utf-8")
df = df.drop_duplicates(subset="ID", keep="first")

#Create home dir
try:
	os.mkdir("../" + awardName)
			
except OSError as error:
	print(awardName, "dir already exists")

#Collect books
for index, row in df.iterrows():
	if (index >= int(startIndex)):	
		book = row["ID"]	
		if (book != "no ID"):
			start_time = time.time()
			borrowing = False 
			print("\nAward Name:", awardName)
			print("Book ID:", book)
			print("Excel Index:", index)
			
			#Navigate to page
			browser.get("https://archive.org/details/" + str(book) + "/mode/2up")
			sleep(randint(5, 7))			
			
			#Book borrowing
			try:
		  		borrowButtPath = browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[2]/button')
			except:
				sleep(4)
				try:
		  			borrowButtPath = browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[2]/button')
					


				except:
					print("trying alt method...")
					try:
		  				borrowButtPath = browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[2]/div[1]/button[1]')
					except:
						print("No borrowing toggle. Trying page manipulation...")
						borrowButtPath = ""
			try:
				buttText = borrowButtPath.text
			except:
				print("=====No Borrow Function=====")
				continue

			#Verify Author
			try:
				webAuthorName = browser.find_element_by_xpath('/html/body/div[1]/main/div[4]/div/div/div[2]/dl').text
				authorName = row["Author"].split(" ")
				if (authorName[0].encode("utf-8").lower() in webAuthorName.encode("utf-8").lower() or authorName[-1].encode("utf-8").lower() in webAuthorName.encode("utf-8").lower()):
					print("=====Author name verified=====")
				else:
					print("=====Author name mismatch, Continuing to next ID=====")
					continue
			except:
				print("!Alert! Could not perform Author verification")
				
			#Find number of pages in book			
			try:	
				if(borrowing): 
					page_num = browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div[2]/div[2]/div[4]/div/div[4]/span').text
				else:                                               
					page_num = browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div[2]/div[2]/div[4]/div/div[4]/span').text
			except:
				print("No page toggle. Trying again...")
				try:
					sleep(3)
					if(borrowing):
						page_num = browser.find_element_by_css_selector('.BRcurrentpage').text
					else:
						page_num = browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div[2]/div[2]/div[4]/div/div[4]/span').text
				
				except:
					print("=====Webpage Failure=====")
					continue 
			####Borrow###
			if("Borrow" in buttText or "borrow" in buttText or "rent" in buttText):
				if "unavailable" not in buttText:			
					print("Borrowing...")				
					borrowButtPath.click()
					borrowing = True
					sleep(10)
					
			else:
				print("Borrowing function not availible")	
				continue
			#####Internal Config#####
		
			#Create save dir name
			try:
				lastName = row["Author"].split(" ")
			except:
				print("=====No Author Value=====")
				continue
			fileName = str(row["Year"]) + "_"+ awardName.lower()+"_"+ row["Award"].lower() +"_" + str(lastName[-1]) 


			#Create save dir path
			if(awardName == "caldecott" or awardName == "newbery"):
				dir_name = "../" + awardName +"_ia/" + fileName
			else:
				dir_name = "../" + awardName + "/" + fileName
			try:
				os.mkdir(dir_name.encode("utf-8"))
			except OSError as error:
				print(error)

			#Create saved image name			
			try:
				page_num = int(page_num.split(' / ')[1])/2
			except:
				page_num = int(page_num.split(' of ')[-1])/2
			page_num = int(page_num)
			print("Number of pages: ", page_num*2)
			#####Internal Config#####
			
			#Get every scan in the book
			for page in range(0, page_num+1):
				if page >=0:
					leftnum = page*2
					rightnum = (page*2) + 1
					firstImg = dir_name + "/" + book + "_1.jpg"
					leftImg = dir_name + "/" + book + "_" + str(leftnum) + ".jpg"
					rightImg = dir_name + "/" + book + "_" + str(rightnum) + ".jpg"
					
					if (page == 0):
						print("First Page")
						getImages(firstImg, leftImgPath)
					elif (page == page_num):
						print("Final Page")
						getImages(leftImg, leftImgPath)
					else:	
						print("Middle Page")
						getImages(leftImg, leftImgPath)
						getImages(rightImg, rightImgPath)


					#Navigate to next page
					try:
						browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div[2]/div[2]/div[4]/div[2]/div[3]/button[2]').click()
					except:
						sleep(3)
						try: 
							browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div[2]/div[2]/div[4]/div[2]/div[3]/button[2]').click()
						except:
							print("overclicked")
							continue
			#Return book
			print("")
			print("Returning book...")
			if(borrowing):				
				browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/button').click()
				sleep(randint(5, 7))			
				try:
		  			browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[2]/button').click()
				except:
					try:
						browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/button[1]').click()
					
					except:
						print("Return button not found")

				sleep(5)
				
			
			print(book, "downloaded in:", round((time.time() - start_time)/60, 2), "minutes")
		else:
			print("\n=====No ID=====")
			print("Excel Index: ", index)
#df.to_excel("FINAL_"+awardName +".xlsx")
print("Completed downloading books for", awardName)
#130
#alex 94 95

	


