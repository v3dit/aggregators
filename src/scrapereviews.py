from bs4 import BeautifulSoup
import requests
import re
import json
import pandas as pd
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from langchain_community.llms import Ollama
import google.generativeai as genai
import os
import streamlit as st
# links=['https://www.zomato.com/mumbai/third-wave-coffee-juhu/reviews','https://www.zomato.com/mumbai/ananda-cafe-juhu/reviews','https://www.zomato.com/mumbai/javaphile-pali-hill-bandra-west/reviews']




# Lists to store data
competitors_list=[]
genai.configure(api_key='AIzaSyAldz5w2KztdyVBwC3PCXzUcv5VMqw6trA')
model=genai.GenerativeModel('gemini-pro')
headers = {
    'authority': 'scrapeme.live',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}
from langchain_community.llms import Ollama

llm = Ollama(model="llama2")
llm2=Ollama(model='mistral')
prompt="Generate a score for parameters :Ambiance, Staff, Food. Be strict in terms of grading. If no valuable information is given for a parameter default to NaN return only a json formatted string like  \{\"Ambiance\"\: 10.0, \"Staff\"\: 9.5, \"Food\"\: 10.0\} for "
def getScript2Json(url):
    soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")
    script_tag = soup.find('script', text=re.compile(r'window\.__PRELOADED_STATE__'))
    script_text = script_tag.text if script_tag else ''
    json_string_pattern = r'window\.__PRELOADED_STATE__ = JSON\.parse\("(.*?)"\);'
    match = re.search(json_string_pattern, script_text)
    if match:
        json_string = match.group(1)

    else:
        print("JSON string not found")
    json_string = json_string.replace('\\\\\\"','').replace('\\"','\"').replace('&apos','').replace("\'", "").replace('\\','')
    return json.loads(json_string)
def ScrapeAllReviews(url):
    url=url+"/reviews"
    
    data = getScript2Json(url)

    if data is not None:
        numberOfPages = data.get('pages', {}).get('restaurant', {}).get(str(data.get('pages', {}).get('current', {}).get('resId', '')), {}).get('sections', {}).get('SECTION_REVIEWS', {}).get('numberOfPages', None)
        print(f"Number of Pages: {numberOfPages}")
        print("Restaurant ID"+str(data.get('pages', {}).get('current', {}).get('resId', {})))
        review_data_list = []

        for i in range(1, 7+1): #numberOfPages+1): #Change back when actually using it

            for _ in range(random.randint(0,2)):
#                 print("",end="")
                sleep(1)
            try:
                
                data1 = getScript2Json(url + "?page=" + str(i) + "&sort=rd&filter=reviews-dd")

                # Extract the reviews
                reviews = data1.get('entities', {}).get('REVIEWS', {})

                # Iterate over each review
                for review_id, review_data in reviews.items():
                    # Extract relevant information from each review
                    review_text = review_data.get('reviewText', '')
                    user_name = review_data.get('userName', '')
                    rating = review_data.get('ratingV2', '')
                    timestamp = review_data.get('timestamp', '')

                    # Append the extracted information to the list
                    review_data_list.append({
                        "Review ID": review_id,
                        "User Name": user_name,
                        "Rating": rating,
                        "Timestamp": timestamp,
                        "Review Text": review_text
                    })
                    pd.DataFrame(review_data_list).to_json("ScrapingDataZomato"+url.split('/')[4]+"_st1_temp.json")
            
            except:
                print(f"Error in page number {i}")
            print(f"Extracting page number:{i}/{numberOfPages}. {int(100*i/numberOfPages)}% completed ")
        df = pd.DataFrame(review_data_list)
        
        return df,df.to_json(),
    else:
        print("Data is None")
def jsontoscores(json_string):
    json_data = json.loads(re.search(r'{(.*?)}', json_string.replace('\n', '').replace('\t', '').strip()).group() )
    print(json_data)
    ambiance_score = float(json_data.get('Ambiance'))
    staff_score = float(json_data.get('Staff'))
    food_score = float(json_data.get('Food'))
    return ambiance_score, staff_score, food_score
def score_returner(df):
    ambiance=df['AmbianceScore'].mean()
    staff=df['StaffScore'].mean()
    food=df['FoodScore'].mean()
    return ambiance,staff,food
def addSentimentScoreOS(df,name):
    df['AmbianceScore']=np.nan
    df['FoodScore']=np.nan
    df['StaffScore']=np.nan
    for i,text in enumerate(df['Review Text']):
        try:
            if(i<7): # replace with True when running for functionality
            
                prompt="Generate a score for the parameters: Ambiance, Staff, Food. Evaluate these aspects very strictly, ensuring that very few scores achieve a perfect 10. Ensure proper text formatting by adding backslashes before apostrophes and double apostrophes. In cases where no valuable information is provided for a specific parameter, score it NaN. The output should be a JSON formatted string, precisely maintaining the structure and escape characters as shown: {\\\"Ambiance\\\": 10.0, \\\"Staff\\\": 9.5, \\\"Food\\\": 10.0}. The goal is to create a standardized, rigorous assessment method for these critical components, reflecting high standards and attention to detail in the evaluation process. The dataset provided is for: "
                resp=llm2.invoke(prompt+str(df['Review Text'][i]))
#                 print(resp)
                df['AmbianceScore'][i],df['StaffScore'][i],df['FoodScore'][i]=jsontoscores(resp)
                
                print(f"Completed {i}/{len(df['Review Text'])}.\t{resp}")
                df.to_json(name+"_scored_temp.json")
        except:
              
            print(f"Error at {i} and {text}")
    return df
def addSentimentScore(df,name):
    df['AmbianceScore']=np.nan
    df['FoodScore']=np.nan
    df['StaffScore']=np.nan
    for i,text in enumerate(df['Review Text']):
        try:
            if True: #(i<7): #replace with True when running for functionality
                while True:
                    try:
                        prompt="You are a sentimental analyser and scorer. If the topic is related at all, give a numerical by properly analysing the text.Generate a score for parameters :Ambiance, Staff, Food. If no valuable information is given for a parameter default to NaN return only a json formatted string like {\"Ambiance\": 10.0, \"Staff\": 9.5, \"Food\": 10.0} for "
                        resp=model.generate_content(prompt+str(df['Review Text'][i]))
        #                 print(resp.text)
                        df['AmbianceScore'][i],df['StaffScore'][i],df['FoodScore'][i]=jsontoscores(resp.text)
                        sleep(2)
                        print(f"Completed {i}/{len(df['Review Text'])}.\t{resp.text}")
                        df.to_json(name+"_scored_temp.json")
                        break
                    except:
                        sleep(1)
                        
                        print(f"Error at {i} and {text} and response {resp.text}")
        except:
              
            print(f"Error at {i} and {text}")
    return df
def calculate_hotel_scores(hotel_scores):
    scores_dict = {}
    for hotel, scores in hotel_scores.items():
        ambiance_score, staff_score, food_score = scores
        scores_dict[hotel] = {
            'AmbianceScore': ambiance_score,
            'StaffScore': staff_score,
            'FoodScore': food_score
        }
    return scores_dict

def score_returner(df):
    ambiance=df['AmbianceScore'].mean()
    staff=df['StaffScore'].mean()
    food=df['FoodScore'].mean()
    return ambiance,staff,food
# Calculate average scores across all hotels
def calculate_average_scores(hotel_scores_dict):
    total_ambiance, total_staff, total_food, count = 0, 0, 0, len(hotel_scores_dict)
    for scores in hotel_scores_dict.values():
        total_ambiance += scores['AmbianceScore']
        total_staff += scores['StaffScore']
        total_food += scores['FoodScore']
    return {
        'AmbianceScore': total_ambiance / count,
        'StaffScore': total_staff / count,
        'FoodScore': total_food / count
    }

# Find the best hotel in each domain
def find_best_hotels(hotel_scores_dict):
    best_ambiance = max(hotel_scores_dict, key=lambda x: hotel_scores_dict[x]['AmbianceScore'])
    best_staff = max(hotel_scores_dict, key=lambda x: hotel_scores_dict[x]['StaffScore'])
    best_food = max(hotel_scores_dict, key=lambda x: hotel_scores_dict[x]['FoodScore'])
    return {
        'Ambiance': best_ambiance,
        'Staff': best_staff,
        'Food': best_food
    }
hotel_scores={}
#Loop to get urls of competitors of the target restaurant 
url=str(st.text_input("Enter the URL of the restaurant"))

run= st.button("Run")
if run:
    driver = webdriver.Chrome()
    driver.get(url)
    sleep(15)
    a_tags = driver.find_elements(By.CSS_SELECTOR, '.sc-bnOsYM')
    a_tags= [a_tag.get_attribute("href") if a_tag else "N/A" for a_tag in a_tags]
    a_tags.append(url)
    
    competitors_list.append(a_tags)
    driver.quit()
    for i,link in enumerate(list(np.unique(a_tags))):
        print('Link:',link)
        # st.write(str((i/len(np.unique(a_tags))*100)+"%%complete"))
        st.write('Link:',link)
        df__,_=ScrapeAllReviews(link)
        df__sc=addSentimentScore(df__[df__['Review Text']!=''].reset_index().head(),link.split('/')[4])
        hotel_scores[link.split('/')[4]]=(score_returner(df__sc))
    print(hotel_scores)
    # st.write(hotel_scores)
    hotel_scores_dict = calculate_hotel_scores(hotel_scores)

    # Display hotel names for the main hotel selection
    hotel_names = list(hotel_scores_dict.keys())
    # main_hotel = 'Ananda Cafe'
    main_hotel=url.split('/')[4]

    # Multiselect for comparing with specific hotels
    # Calculate and display comparisons
    average_scores = calculate_average_scores(hotel_scores_dict)
    best_hotels = find_best_hotels(hotel_scores_dict)
    col1,col2=st.columns(2)
    with col1:
        st.header('General Comparison Insights')
        colors=['#B9F3FC','#93C6E7','#AEE2FF','#FEDEFF']
        # Main hotel vs Best of all hotels in domains
        for domain, best_hotel in best_hotels.items():
            if best_hotel != main_hotel:
                # st.markdown(f"In {domain}, '{best_hotel}' performs better than '{main_hotel}' with a score of {hotel_scores_dict[best_hotel][f'{domain}Score']} vs {hotel_scores_dict[main_hotel][f'{domain}Score']}.")
                st.markdown(f" <div class='animation' style='width:300px;font-size: 18px;margin:5px; padding: 20px; border-radius: 8px; display: grid; background-color: {colors[0]}; text-align:center; font-size:22px;'>In {domain}, '{best_hotel}' performs better than '{main_hotel}' with a score of {hotel_scores_dict[best_hotel][f'{domain}Score']:.2f} vs {hotel_scores_dict[main_hotel][f'{domain}Score']:.2f}.</div>",unsafe_allow_html=True)
       
            else:
                st.markdown(f" <div class='animation' style='width:300px;font-size: 18px;margin:5px; padding: 20px; border-radius: 8px; display: grid; background-color: {colors[3]}; text-align:center; font-size:22px;'>In {domain}, '{best_hotel}' is the best with a score of {hotel_scores_dict[best_hotel][f'{domain}Score']:.2f}.</div>",unsafe_allow_html=True)
                # st.markdown(f"In {domain}, '{best_hotel}' is the best with a score of {hotel_scores_dict[best_hotel][f'{domain}Score']}.")

    # Main hotel vs Average of all hotels
    with col2:
        st.header('Average Comparison Insights')
        main_score_avg=0
        average_score_avg=0
        for score_type in ['AmbianceScore', 'StaffScore', 'FoodScore']:
            main_score = hotel_scores_dict[main_hotel][score_type]
            average_score = average_scores[score_type]
            main_score_avg+=main_score
            average_score_avg+=average_score
            # st.markdown(f"{score_type.replace('Score', '')}: '{main_hotel}' has a score of {main_score} vs the average of {average_score:.2f}.")
            st.markdown(f" <div class='animation' style='width:300px;font-size: 15px;margin:5px; padding: 20px; border-radius: 8px; display: grid; background-color: {colors[3]}; text-align:center; font-size:22px;'>{score_type.replace('Score', '')}: '{main_hotel}' has a score of {main_score} vs the average of {average_score:.2f}.</div>",unsafe_allow_html=True)
        main_score_avg/=3
        average_score_avg/=3
        st.markdown(f" <div class='animation' style='width:300px;font-size: 18px; margin:5px;padding: 20px; border-radius: 8px; display: grid; background-color: {colors[0]}; text-align:center; font-size:22px;'>Overall, '{main_hotel}' has an average score of {main_score_avg:.2f} vs the average of {average_score_avg:.2f}.</div>",unsafe_allow_html=True)

    compare_hotels = [hotel for hotel in hotel_names if hotel != main_hotel]
    
    

    if compare_hotels:
        st.header('Direct Comparison with Selected Hotels')
        for hotel in compare_hotels:
            st.subheader(f"{main_hotel} vs {hotel}")
            comparisons = []
            for score_type in ['AmbianceScore', 'StaffScore', 'FoodScore']:
                main_score = hotel_scores_dict[main_hotel][score_type]
                compare_score = hotel_scores_dict[hotel][score_type]
                score_comparison = main_score - compare_score
                background_color = "#90EE90" if score_comparison > 0 else "#FFCCCB"  # Green if main_score is higher, red if lower
                comparison_text = f"{score_type.replace('Score', '')}: '{main_hotel}' = {main_score:.2f}, '{hotel}' = {compare_score:.2f}"
                comparisons.append((comparison_text, background_color))
            
            # Display each comparison with the determined background color
            for comparison, color in comparisons:
                st.markdown(
                    f" <div class='animation' style='margin-bottom: 10px; padding: 10px; border-radius: 8px; background-color: {color};'>"
                    f"{comparison}"
                    "</div>", unsafe_allow_html=True
                )
    st.markdown("<style> .animation {background-color:black;}</style>", unsafe_allow_html=True)





# Main function to run the Streamlit app




    
    # Calculate scores for each hotel
  