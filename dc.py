import os
import json
import base64
import zipfile
import hashlib
import platform
from io import BytesIO
import requests as req
req.urllib3.disable_warnings()
from colorama import Fore,Style
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor as exe

red    = Fore.RED
yellow = Fore.YELLOW
blue   = Fore.BLUE
white  = Fore.WHITE
bold   = Style.BRIGHT
green  = Fore.GREEN
dim    = Style.DIM
purple = Fore.MAGENTA
cyan   = Fore.CYAN
reset  = Style.RESET_ALL+white

def main():
	try:
		print(f"""{bold}{white}                        
      _           _ _           _    
     | |   {red}v2{white}    | | |  {red}priv8{white}  | |   
   __| | ___ ___ | | | _____  _| |_  
  / _` |/ __/ _ \| | |/ {purple}_{white} \ \/ / __| 
 | (_| | (_| (_) | | |  __/>  <| |_  
  \__,_|\___\___/|_|_|\___/_/\_\\\\__| {dim}{yellow}
  ----------------------------------{reset}
  Tool for grab domain by YutixCode

  [1] grab by registered date {yellow}(cubdomain.com)
  {reset}[2] grab by newly registered domains {yellow}(whoisdownload.com)
  {reset}[3] grab by newly registered domains {yellow}(whoisdatacenter.com)
  {reset}[4] grab newly gTLD domains {yellow}(dnpedia.com)
  {reset}[5] grab newly domains {yellow}(whoisextractor.in)
  {reset}[6] clean duplicate line in file
  {reset}[0] bug report
	""")
		aval = [1,2,3,4,0,5,6]
		menu = input(f"{cyan}>> {reset}choose > ")
		if menu == "1":
			print(f"{cyan}>> {reset}enter date > year-month-day")
			print(f"{cyan}>> {reset}example > 2022-03-30")
			Cubdomain(input(f"{cyan}>> {reset}date > "))
		elif menu == "2":
			print()
			Whoisdownload()
		elif menu == "3":
			print()
			Whoisdatacenter()
		elif menu == "4":
			print()
			DNpedia()
		elif menu == "0":
			print(f"{cyan}>> {reset}whatsapp > +6282321062760")
			exit(f"{cyan}>> {reset}telegram > @yutixverse")
		elif menu == "5":
			print()
			WhoisExtractor()
		elif menu == "6":
			print()
			Clearduplicate()
		elif menu not in aval:
			exit(f"{red}>> {reset}input error")
	except KeyboardInterrupt:
		exit(f"{red}>> {reset}exit")

class Clearduplicate:
	def __init__(self):
		try:
			tmp = []
			for i in os.listdir("."):
				if "txt" in i:
					tmp.append(i)
			for i in range(len(tmp)):
				print(f" {reset}[{i+1}] {cyan}{tmp[i]}")
			inp = int(input(f"\n{cyan}>> {reset}choose > "))
			if inp-1 in range(len(tmp)):
				self.clean(tmp[inp-1])
			else:
				exit(f"{red}>> {reset}enter the correct choice")
		except Exception as err:
			exit(f"{red}>> {reset}{err}")
	
	def clean(self,file):
		tmp = []
		with open(file) as io3:
			io4 = io3.readlines()
			for i in io4:
				tmp.append(i.strip())
			open(file,'w').write('')
		see = set()
		with open(file,'a') as io5:
			for lll in tmp:
				if lll not in see:
					io5.write(f'{lll}\n')
					see.add(lll)
		print(f'{cyan}>> {reset}total lines > {len(tmp)}')
		print(f'{cyan}>> {reset}duplicated > {red}{len(tmp)-len(see)}')
		exit(f'{cyan}>> {reset}filtered > {green}{len(see)}')

class Cubdomain:
	def __init__(self,tgl):
		if len(tgl) == 10:
			url = f'https://66.45.244.251/domains-registered-by-date/{tgl}/'
			raw = req.get(url+'1',headers={'Host':'www.cubdomain.com'},verify=False).text
			sup = bs(raw,"html.parser")
			if sup.find("title").text == "Error 404":
				print(f"{red}>> {reset}404 error - page not found")
				exit(f"{red}>> {reset}use different date")
			else:
				fname = f'{tgl}.txt'
				pages = int(sup.findAll("a",{"class":"page-link"})[5].text.strip())
				print(f"{cyan}>> {reset}total pages > {pages}{reset}")
				for page in range(pages):
					self.grab(url,page+1,fname)
				total = sum(1 for line in open(fname))
				exit(f"{cyan}>> {reset}saved {green}{total}{reset} domains in {yellow}{fname}")
		else:
			exit(f"{red}>> {reset}incorect date")
				
	def grab(self,url,page,fname):
		try:
			raw = req.get(f"{url}{page}",headers={'Host':'www.cubdomain.com'},verify=False).text
			sup = bs(raw,"html.parser")
			items = sup.findAll("div",{"class":"col-md-4"})
			for item in items:
				open(f"{fname}","a").write(f"{item.text.strip()}\n")
			print(end=f"{cyan}>> {reset}scraping page {page} \r")
		except Exception as err:
			exit(f"{red}>> {reset}{err}")

class Whoisdownload:
	def __init__(self):
		try:
			tmp = []
			raw = req.get("https://whoisdownload.com/newly-registered-domains",verify=False).text
			sup = bs(raw,"html.parser").find("tbody")
			dat = sup.findAll("td")
			for i in range(1,len(dat),4):
				cdate = dat[i-1].find("b").text
				count = dat[i].text
				tmp.append(f"{cdate}|{count}")
			for i in range(len(tmp)):
				date,count = tmp[i].split("|")
				print(f" {reset}[{i+1}] {purple}{date} {reset}- {cyan}{count} {reset}domains")
			inp = int(input(f"\n{cyan}>> {reset}choose > "))
			if inp-1 in range(len(tmp)):
				self.dl(tmp[inp-1].split("|")[0])
			else:
				exit(f"{red}>> {reset}enter the correct choice")
		except Exception as err:
			exit(f"{red}>> {reset}{err}")
	
	def dl(self,date):
		print(f"{cyan}>> {reset}downloading data")
		key = base64.b64encode(bytes(f"{date}.zip", 'utf-8')).decode('ascii')
		url = f"https://whoisdownload.com/download-panel/free-download-file/{key}/nrd/home"
		fnm = f"{date}.txt"
		con = req.get(url).content
		par = zipfile.ZipFile(BytesIO(con))
		ser = par.namelist()[0]
		par.extract(ser)
		os.rename(ser,fnm)
		tot = sum(1 for line in open(fnm))
		exit(f"{cyan}>> {reset}saved {green}{tot}{reset} domains in {yellow}{fnm}")

class Whoisdatacenter:
	def __init__(self):
		try:
			tmp = []
			url = "https://whoisdatacenter.com/free-data/"
			raw = req.get(url).text
			par = bs(raw,"html.parser").find("table").findAll("tr")
			for i in range(3,len(par)-1):
				tmp.append(par[i].a.text)
			for i in range(len(tmp)):
				print(f"  {reset}[{i+1}] {cyan}{tmp[i].replace('-domains.zip','')}")
			inp = int(input(f"\n{cyan}>> {reset}choose > "))
			if inp-1 in range(len(tmp)):
				self.download(url,tmp[inp-1])
			else:
				exit(f"{red}>> {reset}enter the correct choice")
		except Exception as err:
			exit(f"{red}>> {reset}{err}")
	
	def download(self,host,path):
		url = f"{host}{path}"
		fnm = f"{path.replace('-domains.zip','')}.txt"
		con = req.get(url).content
		par = zipfile.ZipFile(BytesIO(con))
		ser = par.namelist()[0]
		par.extract(ser)
		os.rename(ser,fnm)
		tot = sum(1 for line in open(fnm))
		exit(f"{cyan}>> {reset}saved {green}{tot}{reset} domains in {yellow}{fnm}")

class DNpedia:
	def __init__(self):
		tmp = []
		url = "https://whoisdatacenter.com/free-data/"
		raw = req.get(url).text
		par = bs(raw,"html.parser").find("table").findAll("tr")
		for i in range(3,len(par)-1):
			tmp.append(par[i].a.text.replace('-domains.zip',''))
		for i in range(len(tmp)):
			print(f"  {reset}[{i+1}] {cyan}{tmp[i]}")
		inp = int(input(f"\n{cyan}>> {reset}choose > "))
		if inp-1 in range(len(tmp)):
			self.scrape(tmp[inp-1])
		else:
			exit(f"{red}>> {reset}enter the correct choice")
			
	def scrape(self,date):
		print()
		try:
			tmp = []
			url = "https://dnpedia.com/tlds/ajax.php"
			hdr = {"x-requested-with":"XMLHttpRequest"}
			prm = f"cmd=tlds&columns=zone,ZoneAdded,zoneid&ecf=zonedate&ecv={date}&zone=1&_search=false&rows=1000&page=1&sidx=zcount&sord=desc"
			raw = req.get(url,headers=hdr,params=prm).json()
			if raw["records"] > 0:
				dat = raw["rows"]
				for i in dat:
					tld = i["zone"]
					tot = i["ZoneAdded"]
					tid = i["zoneid"]
					if tot > 200:
						print(f"   {reset}{tld} {dim}- {reset}{cyan}{tot} {reset}domains")
						tmp.append({"zone":tld,"zoneid":tid})
					else:
						pass
				print(f"\n{cyan}>> {reset}enter domain, example > com")
				dom = input(f"{cyan}>> {reset}domain > ")
				for i in tmp:
					if i['zone'] == dom:
						row = req.get(url,headers=hdr,params=f"cmd=added&columns=name&ecf=zoneid,thedate&ecv={i['zoneid']},{date}&zone={dom}&_search=false&rows=2000&page=1&sidx=length&sord=asc").json()
						if row['records'] > 1:
							print(f"{cyan}>> {reset}total domains > {row['records']}")
							print(f"{cyan}>> {reset}total pages > {row['total']}")
							for x in range(row['total']):
								self.grab(x+1,date,dom,i['zoneid'])
						else:
							print(f"{red}>> {reset}sorry, the date you entered is too old")
							print(f"{red}>> {reset}domains on this date has been deleted")
							print(f"{red}>> {reset}use a different date")
				fil = f"{date}_{dom}.txt"
				try:
					tot = sum(1 for line in open(fil))
				except FileNotFoundError:
					exit(f"{red}>> {reset}enter the avaliable gTLD domain")
				uas = row['records']-tot
				
				print(f"{cyan}>> {reset}filtered {red}{uas} {reset}non-ascii domains")
				exit(f"{cyan}>> {reset}saved {green}{tot}{reset} domains in {yellow}{fil}")
			else:
				print(f"{red}>> {reset}no trace on that date")
				print(f"{red}>> {reset}use a different date")
				exit()
		except Exception as err:
			print(f"{red}>> {reset}{err}")
	
	def grab(self,page,date,dom,zid):
		row = req.get("https://dnpedia.com/tlds/ajax.php",headers={"x-requested-with":"XMLHttpRequest"},params=f"cmd=added&columns=name&ecf=zoneid,thedate&ecv={zid},{date}&zone={dom}&_search=false&rows=2000&page={page}&sidx=length&sord=asc").json()
		rows = row["rows"]
		fnam = f"{date}_{dom}.txt"
		unix = []
		for item in rows:
			name = item["name"]
			if name.isascii():
				open(fnam,"a").write(f'{name}\n')
			else:
				unix.append(name)
		print(end=f"{cyan}>> {reset}scraping page {page} \r")


class WhoisExtractor:
	def __init__(self):
		try:
			#"WHMCSxjLcDnvnTBrK=g3p549h3dnf0av9j29j230vmch" #contoh
			#"WHMCSxjLcDnvnTBrK=dnjthkm9ihp4nc42lvsp21hv8e" #ekse
			hdr = {"cookie":"WHMCSxjLcDnvnTBrK=dnjthkm9ihp4nc42lvsp21hv8e"}
			cek = req.get("https://www.whoisextractor.in/index.php/user/profile",headers=hdr).text
			if bs(cek,"html.parser").title.text == "Login - Whoisextractor":
				exit(f"{red}>> {reset}cookie die")
			else:
				tmp = []
				raw = req.get("https://www.whoisextractor.in/newly-registered-domains/",headers=hdr).text
				sup = bs(raw,"html.parser")
				for item in sup.tbody.findAll("tr"):
					data = item.findAll("td")
					date = data[0].text.split(" ")[3]
					coun = data[2].text
					link = data[4].a["href"].split("=")[1]
					tmp.append(f"{date}|{coun}|{link}")
				for i in range(len(tmp)):
					date,count,link = tmp[i].split("|")
					print(f" {reset}[{i+1}] {yellow}{date} {reset}- {cyan}{count} {reset}domains")
				inp = int(input(f"\n{cyan}>> {reset}choose > "))
				if inp-1 in range(len(tmp)):
					self.download(tmp[inp-1],hdr)
				else:
					exit(f"{red}>> {reset}enter the correct choice")
		except Exception as err:
			exit(f"{red}>> {reset}{err}")
	
	def download(self,data,hdr):
		print(f"{cyan}>> {reset}downloading data")
		date,count,hash = data.split("|")
		url = f"https://www.whoisextractor.in/get/?id={hash}"
		fnm = f"{date}.txt"
		con = req.get(url,headers=hdr).content
		par = zipfile.ZipFile(BytesIO(con))
		ser = par.namelist()[0]
		par.extract(ser)
		os.rename(ser,fnm)
		tot = sum(1 for line in open(fnm))
		exit(f"{cyan}>> {reset}saved {green}{tot}{reset} domains in {yellow}{fnm}")

def auth():
	if platform.system() != 'Windows':
		print(end=f"{yellow}>> {reset}authenticating ... \r")
		key = hashlib.md5(f'yutixcode-{os.uname().release}'.encode()).hexdigest()
		try:
			url = f"https://raw.githubusercontent.com/Yutixcode/Yutixcode/master/dcollext/{key}"
			raw = req.get(url).status_code
			if raw == 200:
				pass
			else:
				print(f"{red}>> {reset}Access denied, You do not have permission")
				exit(f"{red}>> {reset}Your ID: {green}{key}")
		except Exception as er:
			print(f"{red}>> {reset}Someting errors")
			exit(f"{red}>> {reset}{er}")
		main()
	else:
		exit(f"{red}>> {reset}sorry, not support for Windows")

if __name__=="__main__":
	main()
