#import gradio as gr
#from deep_translator import GoogleTranslator
import re
from bs4 import BeautifulSoup
import requests

def convert_html_text(string):
    soup = BeautifulSoup(string, 'html.parser')
    text = soup.get_text()
    text = text.replace("\\n"," ")
    return text

def get_zendesk_data(string):
    host = "wdomni.zendesk.com"
    api = "/api/v2/help_center/articles/search"
    query_string=string.replace(" ","+")
    params = {"query": query_string, "category":"360002456313,360002447234,360002447314,4409809996569,360002455753,360002447254,360002447334,360002447214,360002455733,360002487994,360002455933,900000410866,9186364645529, 360003218594"}
    url = "https://"+host+api
    article_text = " "
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        index=0
        response_list = response.json()["results"]
        
        for x in  response_list:
            if x["title"].find("FAQ") > 0:
                index=index+1
                continue
            if x["title"].find("faq") > 0:
                index=index+1
                continue
            if x["title"].find("2022") > 0:
                index=index+1
                continue
            if x["title"].find("2023") > 0:
                index=index+1
                continue
            break 
        
        article_body = response_list[index]["body"]
#        print(article_body)
        article_text = convert_html_text(article_body)
        countOfWords = len(article_text.split())
        if countOfWords >= 1400:
            article_text = ' '.join(article_text.split()[:1425])
#        return article_text
    else:
        article_text = "Error searching articles"
#    print(article_text)
    return article_text

def input_modifier(string):
    """
    This function is applied to your text inputs before
    they are fed into the model.
    """
    prefix_text="from below text, can you answer this - "
    chat_prompt=string
    zendesk_results = get_zendesk_data(chat_prompt)

    full_text=prefix_text + chat_prompt + " : \n\n " + zendesk_results
    #print(full_text)
    
    return full_text

#my_query = "Which reports I can download from operating accounts screen?"
#result=input_modifier(my_query)
#print(result)
