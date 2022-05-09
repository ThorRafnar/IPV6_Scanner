#!/usr/bin/env python3
from distutils.filelist import findall
from itertools import count
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


class Scraper:
    def __init__(self):
        pass

    def scrape(self, country_code):

        #csv_collums = ["IPV6", "Prefix"]
        URL = f"http://www-public.tem-tsp.eu/~maigron/RIR_Stats/RIR_Delegations/Delegations/IPv6/{country_code.upper()}.html"
        page = requests.get(URL)
        print(page.status_code, URL, type(page.status_code))
        if page.status_code != 200:
            return False , " "

        soup = BeautifulSoup(page.content, "html.parser")

        ip_list = []
        #collecting all the ip's
        for a in soup.find_all('a', href=True):

            if "::" in a.text:
                ip_list.append(a.text[0:-1])

        #We will be looking for a td element wiht a number
        pattern = re.compile(r"(\d+)")

        prefix_list = []
        #Searching for all number in a td element
        for elm in soup.find_all("td", text=pattern):
            #Checking if it is a double digit numbers
            if len(pattern.search(elm.text).groups()[0]) == 2:
                prefix_list.append(pattern.search(elm.text).groups()[0])

        d = {}
        #adding our findings to a dict
        for ip, pre in zip(ip_list, prefix_list):
            d[ip] = pre

        csv_file = f"ipv6{country_code}.csv"
        #writing the ip's and prefixes to csv file
        pd.DataFrame.from_dict(data=d, orient='index').to_csv(csv_file, header=False)

        return True, csv_file


s = Scraper()

codes  = ["AF", "AX", "AL", "DZ", "AS", "AD", "AO", "AI", "AQ", "AG", "AR",
"AM", "AW", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE",
"BZ", "BJ", "BM", "BT", "BO", "BQ", "BA", "BW", "BV", "BR", "IO",
"BN", "BG", "BF", "BI", "CV", "KH", "CM", "CA", "KY", "CF", "TD",
"CL", "CN", "CX", "CC", "CO", "KM", "CG", "CD", "CK", "CR", "CI",
"HR", "CU", "CW", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG",
"SV", "GQ", "ER", "EE", "ET", "FK", "FO", "FJ", "FI", "FR", "GF",
"PF", "TF", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GD",
"GP", "GU", "GT", "GG", "GN", "GW", "GY", "HT", "HM", "VA", "HN",
"HK", "HU", "IS", "IN", "ID", "IR", "IQ", "IE", "IM", "IL", "IT",
"JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KP", "KR", "KW", "KG",
"LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK",
"MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT",
"MX", "FM", "MD", "MC", "MN", "ME", "MS", "MA", "MZ", "MM", "NA",
"NR", "NP", "NL", "NC", "NZ", "NI", "NE", "NG", "NU", "NF", "MP",
"NO", "OM", "PK", "PW", "PS", "PA", "PG", "PY", "PE", "PH", "PN",
"PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "SH", "KN",
"LC", "MF", "PM", "VC", "WS", "SM", "ST", "SA", "SN", "RS", "SC",
"SL", "SG", "SX", "SK", "SI", "SB", "SO", "ZA", "GS", "SS", "ES",
"LK", "SD", "SR", "SJ", "SZ", "SE", "CH", "SY", "TW", "TJ", "TZ",
"TH", "TL", "TG", "TK", "TO", "TT", "TN", "TR", "TM", "TC", "TV",
"UG", "UA", "AE", "GB", "US", "UM", "UY", "UZ", "VU", "VE", "VN",
"VG", "VI", "WF", "EH", "YE", "ZM", "ZW"]


