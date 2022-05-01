from configparser import ConfigParser
from copy import copy
from csv import DictWriter
from datetime import datetime
from requests import get, post
from sys import exit
from time import sleep
from xml.etree import ElementTree

from email_alert import EmailAction

# searching URL (get)
# exampleUrl = "https://api.namecheap.com/xml.response?" \
#              "ApiUser=apiexample&" \
#              "ApiKey=52b4c87ef7fd49cb96a915c0db68124&" \
#              "UserName=apiexample&" \
#              "Command=namecheap.domains.check&" \
#              "ClientIp=192.168.1.109&" \
#              "DomainList=us.xyz"
examplePost = (
    "https://api.namecheap.com/xml.response?"
    "ApiUser=apiexample&"
    "ApiKey=56b4c87ef4fd49cb96d915c0db68194&"
    "UserName=apiexample&"
    "Command=namecheap.domains.create&"
    "ClientIp=192.168.1.109&"
    "DomainName=aa.us.com&"
    "Years=1&"
    "AuxBillingFirstName=John&"
    "AuxBillingLastName=Smith&"
    "AuxBillingAddress1=8939%20S.cross%20Blv&"
    "AuxBillingStateProvince=CA&"
    "AuxBillingPostalCode=90045&"
    "AuxBillingCountry=US&"
    "AuxBillingPhone=+1.6613102107&"
    "AuxBillingEmailAddress=john@gmail.com&"
    "AuxBillingOrganizationName=NC&"
    "AuxBillingCity=CA&"
    "TechFirstName=John&"
    "TechLastName=Smith&"
    "TechAddress1=8939%20S.cross%20Blvd&"
    "TechStateProvince=CA&"
    "TechPostalCode=90045&"
    "TechCountry=US&"
    "TechPhone=+1.6613102107&"
    "TechEmailAddress=john@gmail.com&"
    "TechOrganizationName=NC&"
    "TechCity=CA&"
    "AdminFirstName=John&"
    "AdminLastName=Smith&"
    "AdminAddress1=8939%cross%20Blvd&"
    "AdminStateProvince=CA&"
    "AdminPostalCode=9004&"
    "AdminCountry=US&"
    "AdminPhone=+1.6613102107&"
    "AdminEmailAddress=joe@gmail.com&"
    "AdminOrganizationName=NC&"
    "AdminCity=CA&"
    "RegistrantFirstName=John&"
    "RegistrantLastName=Smith&"
    "RegistrantAddress1=8939%20S.cross%20Blvd&"
    "RegistrantStateProvince=CS&"
    "RegistrantPostalCode=90045&"
    "RegistrantCountry=US&"
    "RegistrantPhone=+1.6613102107&"
    "RegistrantEmailAddress=jo@gmail.com&"
    "RegistrantOrganizationName=NC&"
    "RegistrantCity=CA&"
    "AddFreeWhoisguard=yes&"
    "WGEnabled=yes&"
    "IsPremiumDomain=False"
)


def gen_create_info(domain):
    # input domain and output domain and data for POST to purchase domain
    url = "https://api.namecheap.com/xml.response"
    config = ConfigParser()
    config.read("conf.ini")
    username = config["namecheap"]["username"]
    apikey = config["namecheap"]["apikey"]
    ip = config["namecheap"]["ip"]
    fname = config["personal"]["fname"]
    lname = config["personal"]["lname"]
    addr = config["personal"]["addr"]
    state = config["personal"]["state"]
    country = config["personal"]["country"]
    phone = config["personal"]["phone"]
    email = config["personal"]["email"]
    org = config["personal"]["org"]
    city = config["personal"]["city"]
    zipc = config["personal"]["zipc"]
    data = {
        "ApiUser": username,
        "ApiKey": apikey,
        "UserName": username,
        "ClientIp": ip,
        "Command": "namecheap.domains.create",
        "DomainName": domain,
        "Years": 1,
        "AuxBillingFirstName": fname,
        "AuxBillingLastName": lname,
        "AuxBillingAddress1": addr,
        "AuxBillingStateProvince": state,
        "AuxBillingPostalCode": zipc,
        "AuxBillingCountry": country,
        "AuxBillingPhone": phone,
        "AuxBillingEmailAddress": email,
        "AuxBillingOrganizationName": org,
        "AuxBillingCity": city,
        "TechFirstName": fname,
        "TechLastName": lname,
        "TechAddress1": addr,
        "TechStateProvince": state,
        "TechPostalCode": zipc,
        "TechCountry": country,
        "TechPhone": phone,
        "TechEmailAddress": email,
        "TechOrganizationName": org,
        "TechCity": city,
        "AdminFirstName": fname,
        "AdminLastName": lname,
        "AdminAddress1": addr,
        "AdminStateProvince": state,
        "AdminPostalCode": zipc,
        "AdminCountry": country,
        "AdminPhone": phone,
        "AdminEmailAddress": email,
        "AdminOrganizationName": org,
        "AdminCity": city,
        "RegistrantFirstName": fname,
        "RegistrantLastName": lname,
        "RegistrantAddress1": addr,
        "RegistrantStateProvince": state,
        "RegistrantPostalCode": zipc,
        "RegistrantCountry": country,
        "RegistrantPhone": phone,
        "RegistrantEmailAddress": email,
        "RegistrantOrganizationName": org,
        "RegistrantCity": city,
        "AddFreeWhoisguard": "yes",
        "WGEnabled": "yes",
        "IsPremiumDomain": False,
    }
    return url, data


def dictify(r, root=True):
    if root:
        return {r.tag: dictify(r, False)}
    d = copy(r.attrib)
    if r.text:
        d["_text"] = r.text
    for x in r.findall("./*"):
        if x.tag not in d:
            d[x.tag] = []
        d[x.tag].append(dictify(x, False))
    return d


def generate_4letters_com():
    b = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    output = ""
    for n1 in b:
        for n2 in b:
            for n3 in b:
                for n4 in b:
                    output += f"{n1}{n2}{n3}{n4}.com,"
    outList = output.split(",")
    return outList


def generate_3letters_1number_com():
    num = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    b = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    output = ""
    for n1 in b:
        for n2 in b:
            for n3 in b:
                for n4 in num:
                    # n1 = n1 if n1 != 0 else 1
                    output += f"{n1}{n2}{n3}{n4}.com,"
    outList = output.split(",")
    return outList


def generate_4letters_numbers_com():
    b = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    output = ""
    for n1 in b:
        for n2 in b:
            for n3 in b:
                for n4 in b:
                    # n1 = n1 if n1 != 0 else 1
                    output += f"{n1}{n2}{n3}{n4}.com,"
    outList = output.split(",")
    return outList


def generate_3letters_org_net():
    b = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    output = ""
    for n1 in b:
        for n2 in b:
            for n3 in b:
                output += f"{n1}{n2}{n3}.org,"
                output += f"{n1}{n2}{n3}.net,"
    outList = output.split(",")
    return outList


def generate_3letters_numbers_com():
    b = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    output = ""
    for n1 in b:
        for n2 in b:
            for n3 in b:
                output += f"{n1}{n2}{n3}.com,"
    outList = output.split(",")
    return outList


def generate_3letters_numbers_org_net():
    b = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    output = ""
    for n1 in b:
        for n2 in b:
            for n3 in b:
                output += f"{n1}{n2}{n3}.org,"
                output += f"{n1}{n2}{n3}.net,"
    outList = output.split(",")
    return outList


def generate_2letters_numbers_org_net():
    b = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    output = ""
    for n1 in b:
        for n2 in b:
            output += f"{n1}{n2}.org,"
            output += f"{n1}{n2}.net,"
    outList = output.split(",")
    return outList


def gen_2l1n_org_net():
    combos = "aa1,1aa,aa2,2aa,aa3,3aa,aa4,4aa,aa5,5aa,aa6,6aa,aa7,7aa,aa8,8aa,aa9,9aa,aa0,0aa,bb1,1bb,bb2,2bb,bb3,3bb,bb4,4bb,bb5,5bb,bb6,6bb,bb7,7bb,bb8,8bb,bb9,9bb,bb0,0bb,cc1,1cc,cc2,2cc,cc3,3cc,cc4,4cc,cc5,5cc,cc6,6cc,cc7,7cc,cc8,8cc,cc9,9cc,cc0,0cc,dd1,1dd,dd2,2dd,dd3,3dd,dd4,4dd,dd5,5dd,dd6,6dd,dd7,7dd,dd8,8dd,dd9,9dd,dd0,0dd,ee1,1ee,ee2,2ee,ee3,3ee,ee4,4ee,ee5,5ee,ee6,6ee,ee7,7ee,ee8,8ee,ee9,9ee,ee0,0ee,dd1,1dd,dd2,2dd,dd3,3dd,dd4,4dd,dd5,5dd,dd6,6dd,dd7,7dd,dd8,8dd,dd9,9dd,dd0,0dd,ff1,1ff,ff2,2ff,ff3,3ff,ff4,4ff,ff5,5ff,ff6,6ff,ff7,7ff,ff8,8ff,ff9,9ff,ff0,0ff,gg1,1gg,gg2,2gg,gg3,3gg,gg4,4gg,gg5,5gg,gg6,6gg,gg7,7gg,gg8,8gg,gg9,9gg,gg0,0gg,hh1,1hh,hh2,2hh,hh3,3hh,hh4,4hh,hh5,5hh,hh6,6hh,hh7,7hh,hh8,8hh,hh9,9hh,hh0,0hh,ii1,1ii,ii2,2ii,ii3,3ii,ii4,4ii,ii5,5ii,ii6,6ii,ii7,7ii,ii8,8ii,ii9,9ii,ii0,0ii,jj1,1jj,jj2,2jj,jj3,3jj,jj4,4jj,jj5,5jj,jj6,6jj,jj7,7jj,jj8,8jj,jj9,9jj,jj0,0jj,kk1,1kk,kk2,2kk,kk3,3kk,kk4,4kk,kk5,5kk,kk6,6kk,kk7,7kk,kk8,8kk,kk9,9kk,kk0,0kk,ll1,1ll,ll2,2ll,ll3,3ll,ll4,4ll,ll5,5ll,ll6,6ll,ll7,7ll,ll8,8ll,ll9,9ll,ll0,0ll,mm1,1mm,mm2,2mm,mm3,3mm,mm4,4mm,mm5,5mm,mm6,6mm,mm7,7mm,mm8,8mm,mm9,9mm,mm0,0mm,nn1,1nn,nn2,2nn,nn3,3nn,nn4,4nn,nn5,5nn,nn6,6nn,nn7,7nn,nn8,8nn,nn9,9nn,nn0,0nn,oo1,1oo,oo2,2oo,oo3,3oo,oo4,4oo,oo5,5oo,oo6,6oo,oo7,7oo,oo8,8oo,oo9,9oo,oo0,0oo,pp1,1pp,pp2,2pp,pp3,3pp,pp4,4pp,pp5,5pp,pp6,6pp,pp7,7pp,pp8,8pp,pp9,9pp,pp0,0pp,qq1,1qq,qq2,2qq,qq3,3qq,qq4,4qq,qq5,5qq,qq6,6qq,qq7,7qq,qq8,8qq,qq9,9qq,qq0,0qq,rr1,1rr,rr2,2rr,rr3,3rr,rr4,4rr,rr5,5rr,rr6,6rr,rr7,7rr,rr8,8rr,rr9,9rr,rr0,0rr,ss1,1ss,ss2,2ss,ss3,3ss,ss4,4ss,ss5,5ss,ss6,6ss,ss7,7ss,ss8,8ss,ss9,9ss,ss0,0ss,tt1,1tt,tt2,2tt,tt3,3tt,tt4,4tt,tt5,5tt,tt6,6tt,tt7,7tt,tt8,8tt,tt9,9tt,tt0,0tt,uu1,1uu,uu2,2uu,uu3,3uu,uu4,4uu,uu5,5uu,uu6,6uu,uu7,7uu,uu8,8uu,uu9,9uu,uu0,0uu,vv1,1vv,vv2,2vv,vv3,3vv,vv4,4vv,vv5,5vv,vv6,6vv,vv7,7vv,vv8,8vv,vv9,9vv,vv0,0vv,ww1,1ww,ww2,2ww,ww3,3ww,ww4,4ww,ww5,5ww,ww6,6ww,ww7,7ww,ww8,8ww,ww9,9ww,ww0,0ww,xx1,1xx,xx2,2xx,xx3,3xx,xx4,4xx,xx5,5xx,xx6,6xx,xx7,7xx,xx8,8xx,xx9,9xx,xx0,0xx,yy1,1yy,yy2,2yy,yy3,3yy,yy4,4yy,yy5,5yy,yy6,6yy,yy7,7yy,yy8,8yy,yy9,9yy,yy0,0yy,zz1,1zz,zz2,2zz,zz3,3zz,zz4,4zz,zz5,5zz,zz6,6zz,zz7,7zz,zz8,8zz,zz9,9zz,zz0,0zz"
    comboList = combos.split(",")
    domainList = []
    for item in comboList:
        domainList.append(f"{item}.org")
        domainList.append(f"{item}.net")
    return domainList


def gen_2l1n_com():
    combos = "aa1,1aa,aa2,2aa,aa3,3aa,aa4,4aa,aa5,5aa,aa6,6aa,aa7,7aa,aa8,8aa,aa9,9aa,aa0,0aa,bb1,1bb,bb2,2bb,bb3,3bb,bb4,4bb,bb5,5bb,bb6,6bb,bb7,7bb,bb8,8bb,bb9,9bb,bb0,0bb,cc1,1cc,cc2,2cc,cc3,3cc,cc4,4cc,cc5,5cc,cc6,6cc,cc7,7cc,cc8,8cc,cc9,9cc,cc0,0cc,dd1,1dd,dd2,2dd,dd3,3dd,dd4,4dd,dd5,5dd,dd6,6dd,dd7,7dd,dd8,8dd,dd9,9dd,dd0,0dd,ee1,1ee,ee2,2ee,ee3,3ee,ee4,4ee,ee5,5ee,ee6,6ee,ee7,7ee,ee8,8ee,ee9,9ee,ee0,0ee,dd1,1dd,dd2,2dd,dd3,3dd,dd4,4dd,dd5,5dd,dd6,6dd,dd7,7dd,dd8,8dd,dd9,9dd,dd0,0dd,ff1,1ff,ff2,2ff,ff3,3ff,ff4,4ff,ff5,5ff,ff6,6ff,ff7,7ff,ff8,8ff,ff9,9ff,ff0,0ff,gg1,1gg,gg2,2gg,gg3,3gg,gg4,4gg,gg5,5gg,gg6,6gg,gg7,7gg,gg8,8gg,gg9,9gg,gg0,0gg,hh1,1hh,hh2,2hh,hh3,3hh,hh4,4hh,hh5,5hh,hh6,6hh,hh7,7hh,hh8,8hh,hh9,9hh,hh0,0hh,ii1,1ii,ii2,2ii,ii3,3ii,ii4,4ii,ii5,5ii,ii6,6ii,ii7,7ii,ii8,8ii,ii9,9ii,ii0,0ii,jj1,1jj,jj2,2jj,jj3,3jj,jj4,4jj,jj5,5jj,jj6,6jj,jj7,7jj,jj8,8jj,jj9,9jj,jj0,0jj,kk1,1kk,kk2,2kk,kk3,3kk,kk4,4kk,kk5,5kk,kk6,6kk,kk7,7kk,kk8,8kk,kk9,9kk,kk0,0kk,ll1,1ll,ll2,2ll,ll3,3ll,ll4,4ll,ll5,5ll,ll6,6ll,ll7,7ll,ll8,8ll,ll9,9ll,ll0,0ll,mm1,1mm,mm2,2mm,mm3,3mm,mm4,4mm,mm5,5mm,mm6,6mm,mm7,7mm,mm8,8mm,mm9,9mm,mm0,0mm,nn1,1nn,nn2,2nn,nn3,3nn,nn4,4nn,nn5,5nn,nn6,6nn,nn7,7nn,nn8,8nn,nn9,9nn,nn0,0nn,oo1,1oo,oo2,2oo,oo3,3oo,oo4,4oo,oo5,5oo,oo6,6oo,oo7,7oo,oo8,8oo,oo9,9oo,oo0,0oo,pp1,1pp,pp2,2pp,pp3,3pp,pp4,4pp,pp5,5pp,pp6,6pp,pp7,7pp,pp8,8pp,pp9,9pp,pp0,0pp,qq1,1qq,qq2,2qq,qq3,3qq,qq4,4qq,qq5,5qq,qq6,6qq,qq7,7qq,qq8,8qq,qq9,9qq,qq0,0qq,rr1,1rr,rr2,2rr,rr3,3rr,rr4,4rr,rr5,5rr,rr6,6rr,rr7,7rr,rr8,8rr,rr9,9rr,rr0,0rr,ss1,1ss,ss2,2ss,ss3,3ss,ss4,4ss,ss5,5ss,ss6,6ss,ss7,7ss,ss8,8ss,ss9,9ss,ss0,0ss,tt1,1tt,tt2,2tt,tt3,3tt,tt4,4tt,tt5,5tt,tt6,6tt,tt7,7tt,tt8,8tt,tt9,9tt,tt0,0tt,uu1,1uu,uu2,2uu,uu3,3uu,uu4,4uu,uu5,5uu,uu6,6uu,uu7,7uu,uu8,8uu,uu9,9uu,uu0,0uu,vv1,1vv,vv2,2vv,vv3,3vv,vv4,4vv,vv5,5vv,vv6,6vv,vv7,7vv,vv8,8vv,vv9,9vv,vv0,0vv,ww1,1ww,ww2,2ww,ww3,3ww,ww4,4ww,ww5,5ww,ww6,6ww,ww7,7ww,ww8,8ww,ww9,9ww,ww0,0ww,xx1,1xx,xx2,2xx,xx3,3xx,xx4,4xx,xx5,5xx,xx6,6xx,xx7,7xx,xx8,8xx,xx9,9xx,xx0,0xx,yy1,1yy,yy2,2yy,yy3,3yy,yy4,4yy,yy5,5yy,yy6,6yy,yy7,7yy,yy8,8yy,yy9,9yy,yy0,0yy,zz1,1zz,zz2,2zz,zz3,3zz,zz4,4zz,zz5,5zz,zz6,6zz,zz7,7zz,zz8,8zz,zz9,9zz,zz0,0zz"
    comboList = combos.split(",")
    domainList = []
    for item in comboList:
        domainList.append(f"{item}.com")
    return domainList


def gen_domain_strings(inlist):
    """Takes input list of separated domains and groups them into strings of 50"""
    domainString = ""
    outList = []
    count = 0
    for item in inlist:
        if count < 50:
            domainString += f"{item},"
            count += 1
        elif count == 50:
            outList.append(domainString)
            domainString = ""
            count = 0
    return outList


# response = get(url)
# tree = ElementTree.fromstring(response.content)

if __name__ == "__main__":
    # print(domainString)
    # print(url)
    while True:
        config = ConfigParser()
        config.read("conf.ini")
        username = config["namecheap"]["username"]
        apikey = config["namecheap"]["apikey"]
        ip = config["namecheap"]["ip"]

        outList0 = generate_2letters_numbers_org_net()
        outList1 = generate_4letters_com()
        outList2 = generate_4letters_numbers_com()
        outList3 = generate_3letters_numbers_org_net()
        outList4 = generate_3letters_org_net()
        outList5 = generate_3letters_numbers_com()
        outList6 = generate_3letters_1number_com()
        outStrings0 = gen_domain_strings(outList0)
        outStrings1 = gen_domain_strings(outList1)
        outStrings2 = gen_domain_strings(outList2)
        outStrings3 = gen_domain_strings(outList3)
        outStrings4 = gen_domain_strings(outList4)
        outStrings5 = gen_domain_strings(outList5)
        outStrings6 = gen_domain_strings(outList6)
        # TEST
        # outStringsM = outStrings3 + outStrings0 + outStrings6 + outStrings1 + outStrings5
        # below for prod (auto-purchase) of only high-value unicorn domains (com 3 letters
        # PROD
        # 2 letters/numbers org,net, 3 letters numbers com, 4 letters com
        outStringsM = outStrings0 + outStrings5 + outStrings1
        resultList = []
        fileTime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        outfile = r"X:\domainAPIResults-{}.csv".format(fileTime)
        cols = [
            "Domain",
            "Available",
            "ErrorNo",
            "IsPremiumName",
            "PremiumRegistrationPrice",
        ]
        with open(outfile, "w", newline="") as csvfile:
            writer = DictWriter(csvfile, fieldnames=cols)
            writer.writeheader()

        purchased = 0
        for item in outStringsM:
            #print(
            #    "Requesting...", datetime.now().isoformat(timespec="seconds"), end=" - "
            #)
            # checkUrl = f"https://api.namecheap.com/xml.response?ApiUser={username}&ApiKey={apikey}&UserName={username}&Command=namecheap.domains.check&ClientIp={ip}&DomainList={item}"
            checkUrl = f"https://api.namecheap.com/xml.response"
            checkData = {
                "ApiUser": username,
                "ApiKey": apikey,
                "UserName": username,
                "Command": "namecheap.domains.check",
                "ClientIp": ip,
                "DomainList": item,
            }
            response = post(checkUrl, checkData)
            # response = get(checkUrl)
            print(response.status_code, end=", ")
            tree = ElementTree.fromstring(response.content)
            dictTree = dictify(tree)
            for item in dictTree["{http://api.namecheap.com/xml.response}ApiResponse"][
                "{http://api.namecheap.com/xml.response}CommandResponse"
            ][0]["{http://api.namecheap.com/xml.response}DomainCheckResult"]:
                # print(item)
                if purchased >= 3:
                    print("PURCHASE LIMIT REACHED, EXITING")
                    exit()
                elif item["Available"] == "true" and item["IsPremiumName"] == "false":
                    # this shows that the domain is a standard (~$10) domain
                    # this is the type of domain that should be registered
                    # POST to buy...
                    item.pop("Description", None)
                    item.pop("PremiumRenewalPrice", None)
                    item.pop("PremiumRestorePrice", None)
                    item.pop("PremiumTransferPrice", None)
                    item.pop("IcannFee", None)
                    item.pop("EapFee", None)
                    print("\nPurchase: ", item)
                    getUrl, getData = gen_create_info(item["Domain"])
                    # post to get domain
                    getResponse = post(getUrl, getData)
                    if getResponse.status_code == 200:
                        getTree = ElementTree.fromstring(getResponse.content)
                        getDictTree = dictify(getTree)
                        alert = EmailAction(item["Domain"], str(getDictTree))
                        alert.send_alert()
                        purchased += 1
                    else:
                        getTree = ElementTree.fromstring(getResponse.content)
                        getDictTree = dictify(getTree)
                        errorSubj = f"ERROR REGISTERING {item['Domain']}"
                        alert = EmailAction(item["Domain"], str(getDictTree))
                        alert.send_alert()
                    with open(outfile, "a", newline="") as csvfile:
                        writer = DictWriter(csvfile, fieldnames=cols)
                        writer.writerow(item)

            sleep(3)
        sleep(60)
