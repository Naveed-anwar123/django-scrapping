from django.shortcuts import render
from django.http import  HttpResponse
from . import forms
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponseRedirect
import pandas as pd

data = []
all_data = []
def index(request):
    my_dic = {
        'insert_me': 'Inserted'
    }
    return render(request, 'index.html', context=my_dic)

def search(request):
    form = forms.FormName()
    if request.method == 'POST':
        form = forms.FormName(request.POST)
        q= form['search'].value()
        search_item = q
        url = "https://www.google.co.in/search?q=" + search_item

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        search_item_m = q + ' manta'
        url_m = "https://www.google.co.in/search?q=" + search_item_m

        response_m = requests.get(url_m)
        soup_m = BeautifulSoup(response_m.text, "lxml")

        try:
            facebook = "true"
            linkedin = "true"

            data = []
   #         print([qout.text for qout in soup.select("span.A1t5ne")][0])
            data.append([qout.text for qout in soup.select("span.A1t5ne")][0])
  #          print([qout.text for qout in soup.select("span.A1t5ne")][3])
            data.append([qout.text for qout in soup.select("span.A1t5ne")][3])
 #           print(soup.select("div.g")[0].select('.r a')[0]['href'].split("/&")[0].split("=")[1])
            data.append(soup.select("div.g")[0].select('.r a')[0]['href'].split("/&")[0].split("=")[1])
#            print(soup_m.select("div.g")[0].select('.r a')[0]['href'].split("/&")[0].split("=")[1])
            data.append(soup_m.select("div.g")[0].select('.r a')[0]['href'].split("/&")[0].split("=")[1])

            for qout in soup.select(".r a"):
                if qout['href'].find("facebook") != -1 and facebook == "true":
                    #print(qout['href'].split("/&")[0].split("=")[1])
                    data.append(qout['href'].split("/&")[0].split("=")[1])
                    facebook = "false"

                if qout['href'].find("linkedin") != -1 and linkedin == "true":
                    #print(qout['href'].split("/&")[0].split("=")[1])
                    data.append(qout['href'].split("/&")[0].split("=")[1])
                    linkedin = "false"

                if qout['href'].find("instagram") != -1:
                    data.append(qout['href'].split("/&")[0].split("=")[1])


            all_data.append(data)
            df = pd.concat([pd.Series(x) for x in all_data], axis=1)
            df = df.transpose()
            df.columns = ['Address', 'Phone', 'Website', 'Manta.com	', 'Facebook', 'Linked-in']

            print("-----")
            df.to_excel('Results.xlsx', encoding='utf8')
            print("-----")
            return render(request, 'search.html', {'d': all_data,'form': form})
        except:
            print("Unhandled Error")
            print("Enter correct company or person name")


    return render(request, 'search.html', {'form': form})

