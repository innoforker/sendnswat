# sendnswat
# written in 2022 (code is kinda shit)

from bs4 import BeautifulSoup
import requests
import re
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import colorama
from sys import exit
from colorama import Fore, Back, Style
from os import system
import platform
from fake_useragent import UserAgent
from itertools import groupby
import validators

INTEGRATED_HEADERS = {
	'User-Agent': UserAgent().random
}

def clearScreen():
	if platform.system() == "Windows":
		system('cls')
	if platform.system() != "Windows":
		system('clear')

colorama.init()

def Gather_Mails(url):
	mail_list = []
	possible_tags = ['a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b', 'em', 'i', 'code', 'kbd', 'pre', 'abbr', 'bdo', 'blockquote', 'q', 'cite', 'p', 'td']
	try:
		REQUEST = requests.get(url, headers=INTEGRATED_HEADERS, timeout=10).text
		soup = BeautifulSoup(REQUEST, 'html.parser')
		for tag in possible_tags:
			mails = soup.findAll(tag)
			for mail in mails:
				regex = r'[\w.+-]+@[\w-]+\.[\w.-]+'
				if re.match(regex, mail.text):
					_mail = re.search(regex, mail.text).group(0).strip()
					if _mail not in mail_list:
						print(_mail)
						mail_list.append(_mail)
		mail_list = [el for el, _ in groupby(mail_list)]
		return mail_list
	except:
		pass
def Get_URLS(_url):
	try:
		req = requests.get(_url, headers=INTEGRATED_HEADERS, timeout=10).text
		soup = BeautifulSoup(req, 'html.parser')
		urls = soup.findAll('a')
		url_list = []
		site = ""
		conntype = ""
		if _url[:5] == 'https':
			conntype = 'https'
		else:
			conntype = 'http'
		site = _url.split(f'{conntype}://')[1].replace("/", "")
		for url in urls:
			if url["href"][0] != '/':
				if url["href"][:4] == 'http':
					url_list.append(url["href"])
			else:
				url_list.append(f'{conntype}://{site}{url["href"]}')
	except:
		return None
	else:
		url_list = [el for el, _ in groupby(url_list)]
		return url_list
clearScreen()
print(f'{Fore.YELLOW}WARNING: Use the protected vpn for doing illegal things. VPN must be without logs saving, only paid.{Style.RESET_ALL}\n')
URL_TO_SEND = input(f'{Fore.CYAN}Enter url to parse all mails /> {Style.RESET_ALL}')
isUrl = validators.url(URL_TO_SEND)
if isUrl != True:
	print(f'{Fore.RED}Fatal error!{Style.RESET_ALL}')
	exit(-1)
else:
	clearScreen()
	m2 = []
	print(f'{Fore.CYAN}Gathering mails...{Style.RESET_ALL}')
	urls = Get_URLS(URL_TO_SEND)
	if urls != None:
		for u in urls:
			ur = Gather_Mails(u)
			try:
				if len(ur) != 0:
					for x in Gather_Mails(u):
						m2.append(x)
			except Exception as e:
				print(e)
				pass
	ALL_MAILS = Gather_Mails(URL_TO_SEND)
	try:
		if len(ALL_MAILS) == 0 and len(m2) == 0:
			print(f'{Fore.RED}Mails were not found.{Style.RESET_ALL}')
		else:
			for MAIL in ALL_MAILS:
				m2.append(MAIL)
	except:
		pass
	else:
		if len(m2) != 0 and len(ALL_MAILS) != 0:
			yn = input('Start the mailing? Just press enter')
			clearScreen()
			email = input('Enter your email: ')
			password = input("Enter email's password: ")
			subject = input('Enter subject of your message: ')
			text = input('Enter text to send: ')
			msg = MIMEMultipart('alternative')
			msg["From"] = email
			msg["Subject"] = subject
			for lst in m2:
				msg["To"] = lst
				rltxt = MIMEText(text, 'plain')
				msg.attach(rltxt)
				server = smtplib.SMTP('smtp.gmail.com', 587)
				server.starttls()
				server.login(email, password)
				server.sendmail(email, lst, msg.as_string())
				print('[Sent]!')
			server.quit()
		else:
			exit(-1)