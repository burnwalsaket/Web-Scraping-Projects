
from bs4 import BeautifulSoup
import requests
import smtplib
from dotenv import load_dotenv

load_dotenv()

url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
header={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"}
response = requests.get(url,headers=header)
soup = BeautifulSoup(response.content, 'html.parser')
# print(soup.prettify())
price=soup.find(class_="a-offscreen").getText()
print(price)
price_without_currency=price.split("INR")[1]
print(price_without_currency)
price_cleaned = price_without_currency.replace(",", "")
price_as_float = float(price_cleaned)
print(price_as_float)
#Send an Email
title=soup.find(id="productTitle").getText()
print(title)
Buy_price=15000
if price_as_float<Buy_price:
    message=f"{title}is on sale for {price}"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        result = connection.login("ksaket23458@gmail.com", "my password")
        connection.sendmail(
            from_addr="ksaket23458@gmail.com",
            to_addrs="ksaket23458@gmail.com",
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
        )
