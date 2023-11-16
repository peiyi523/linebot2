import requests
from bs4 import BeautifulSoup


def get_invoice_numbers():
    try:
        url = "https://www.etax.nat.gov.tw/etw-main/ETW183W2_11207/"
        resp = requests.get(url)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "lxml")
        tds = soup.find(id="tenMillionsTable").find_all("div", class_="col-12 mb-3")
        numbers = [td.text.strip() for td in tds]

    except Exception as e:
        print(e)

    return numbers


# 進行對獎
def search_invoice_bingo(invoice_number, numbers):
    bingo = False
    for i in range(len(numbers)):
        if numbers[i][5:] == invoice_number[len(invoice_number) - 3 :]:
            bingo = True
            break
    message = ""
    if bingo:
        if i == 0:
            message = "超有機會中特別獎1000萬(八個號碼)"

        elif i == 1:
            message = "有機會中特別獎200萬(八個號碼)"

        else:
            message = "有機會中20萬(三個號碼中200)"
        message += f"\n請繼續對其他號碼==>{numbers[i]}"
    else:
        message = "@@沒有中獎~~"

    return message


if __name__ == "__main__":
    numbers = get_invoice_numbers()
    print(numbers)
    print(search_invoice_bingo("09505731", numbers))
