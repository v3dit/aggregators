import streamlit as st
import numpy as np
import pandas as pd

# Function to calculate scores for each hotel
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

# Main function to run the Streamlit app
def main():
    st.title('Restraunt Review Comparison')
    st.write('#### Easily compare restraunt reviews with this intuitive tool. Just choose your main restraunts to instantly see how it fares in ambience, staff service, and food quality against others. Gain valuable insights into its performance compared to top-rated restrauntss overall, and visualize the differences through direct comparisons.')
    # Hotel scores stored in a dictionary
    hotel_scores = {
        'Hotel1': (9, 8, 10),
        'Hotel2': (8, 7, 9),
        'Hotel3': (10, 9, 8)
    }
    import os

    # Get all file URLs in the "datas" subdirectory
    file_paths = [
    ('Ananda Cafe', r'C:\\AIML\\HackNiche_DODS\\Streamlit_Interface\\src\\pages\\streamlit_data\\anandacafescoredd.json'),
    ('Chantilly', r'C:\\AIML\\HackNiche_DODS\\Streamlit_Interface\\src\\pages\\streamlit_data\\ChantillyReviewsscoredd.json'),
    ('Earth Cafe', r'C:\\AIML\\HackNiche_DODS\\Streamlit_Interface\\src\\pages\\streamlit_data\\earth-cafe-@-juhu-1-juhuscoredd.json'),
    ('Love and Latte', r'C:\\AIML\\HackNiche_DODS\\Streamlit_Interface\\src\\pages\\streamlit_data\\love-latte-juhuscoredd.json'),
    ('Ettara', r'C:\\AIML\\HackNiche_DODS\\Streamlit_Interface\\src\\pages\\streamlit_data\\EttaraScored.json')
]

# Creating a list of tuples with cafe names and DataFrames
    file_urls = [(name, pd.read_json(path)) for name, path in file_paths]

    # for x in file_urls:
    #     st.write(x)


    # Print the file URLs
    hotel_scores = {}
    for name,file in file_urls:
        hotel_scores[name]=score_returner(file)

    # st.write(file_urls)
    
    # Calculate scores for each hotel
    hotel_scores_dict = calculate_hotel_scores(hotel_scores)

    # Display hotel names for the main hotel selection
    hotel_names = list(hotel_scores_dict.keys())
    # main_hotel = 'Ananda Cafe'
    main_hotel = st.selectbox('Select the main hotel:', hotel_names, index=4)

    # Multiselect for comparing with specific hotels
    # Calculate and display comparisons
    average_scores = calculate_average_scores(hotel_scores_dict)
    best_hotels = find_best_hotels(hotel_scores_dict)
    col1,col2=st.columns(2)
    with col1:
        st.header('General Comparison Insights')
        colors=['#F76B69','#93C6E7','#AEE2FF','#90EE90']
        # Main hotel vs Best of all hotels in domains
        for domain, best_hotel in best_hotels.items():
            if best_hotel != main_hotel:
                # st.markdown(f"In {domain}, '{best_hotel}' performs better than '{main_hotel}' with a score of {hotel_scores_dict[best_hotel][f'{domain}Score']} vs {hotel_scores_dict[main_hotel][f'{domain}Score']}.")
                st.markdown(f"<div style='width:300px;font-size: 18px;margin:5px; padding: 20px; border-radius: 8px; display: grid; background-color: {colors[0]}; text-align:center; font-size:22px;'>In {domain}, '{best_hotel}' performs better than '{main_hotel}' with a score of {hotel_scores_dict[best_hotel][f'{domain}Score']:.2f} vs {hotel_scores_dict[main_hotel][f'{domain}Score']:.2f}.</div>",unsafe_allow_html=True)
       
            else:
                st.markdown(f"<div style='width:300px;font-size: 18px;margin:5px; padding: 20px; border-radius: 8px; display: grid; background-color: {colors[3]}; text-align:center; font-size:22px;'>In {domain}, '{best_hotel}' is the best with a score of {hotel_scores_dict[best_hotel][f'{domain}Score']:.2f}.</div>",unsafe_allow_html=True)
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
            st.markdown(f"<div style='width:300px;font-size: 15px;margin:5px; padding: 20px; border-radius: 8px; display: grid; background-color: {colors[3]}; text-align:center; font-size:22px;'>{score_type.replace('Score', '')}: '{main_hotel}' has a score of {main_score} vs the average of {average_score:.2f}.</div>",unsafe_allow_html=True)
        main_score_avg/=3
        average_score_avg/=3
        st.markdown(f"<div style='width:300px;font-size: 18px; margin:5px;padding: 20px; border-radius: 8px; display: grid; background-color: {colors[0]}; text-align:center; font-size:22px;'>Overall, '{main_hotel}' has an average score of {main_score_avg:.2f} vs the average of {average_score_avg:.2f}.</div>",unsafe_allow_html=True)
    # CSS styled insights presentation
    # st.markdown(
    #     f"<div style='padding: 20px; border-radius: 8px; display: grid; grid-template-columns: 1fr 1fr; grid-gap: 20px;'>"
    #     f"<div style='font-size: 18px; padding: 20px; border-radius: 8px; display: grid; background-color: #B9F3FC; text-align:center; font-size:22px;'>{main_hotel}' has a score of {main_score} vs the average of {average_score:.2f}.</div>"
    #     f"<div style='font-size: 18px; padding: 20px; border-radius: 8px; display: grid; background-color: #93C6E7; text-align:center; font-size:22px;'></div>"
    #     f"<div style='font-size: 18px; padding: 20px; border-radius: 8px; display: grid; background-color: #AEE2FF; text-align:center; font-size:22px;'><b>Average Price per Item:</b><br>₹{average_scores['FoodScore']:.2f}</div>"
    #     f"<div style='font-size: 18px; padding: 20px; border-radius: 8px; display: grid; background-color: #FEDEFF; text-align:center; font-size:22px;'>Overall, '{main_hotel}' has an average score of {main_score_avg:.2f} vs the average of {average_score_avg:.2f}.</div>",unsafe_allow_html=True)
    # # Direct comparison with selected hotels
    compare_hotels = st.multiselect('Select hotels to compare with the main hotel:', [hotel for hotel in hotel_names if hotel != main_hotel])
    
    
    # if compare_hotels:
    #     st.header('Direct Comparison with Selected Hotels')
    #     for hotel in compare_hotels:
    #         st.subheader(f"{main_hotel} vs {hotel}")
    #         comparisons = []
    #         for score_type in ['AmbianceScore', 'StaffScore', 'FoodScore']:
    #             main_score = hotel_scores_dict[main_hotel][score_type]
    #             compare_score = hotel_scores_dict[hotel][score_type]
    #             comparisons.append(f"{score_type.replace('Score', '')}: '{main_hotel}' = {main_score}, '{hotel}' = {compare_score}")
            
    #         # Display each comparison using the CSS style
    #         for comparison in comparisons:
    #             st.markdown(
    #                 f"<div style='margin-bottom: 10px; padding: 10px; border-radius: 8px; background-color:{colors[0]};'>"
    #                 f"{comparison}"
    #                 "</div>", unsafe_allow_html=True
    #             )
    if compare_hotels:
        st.header('Direct Comparison with Selected Hotels')
        for hotel in compare_hotels:
            st.subheader(f"{main_hotel} vs {hotel}")
            comparisons = []
            for score_type in ['AmbianceScore', 'StaffScore', 'FoodScore']:
                main_score = hotel_scores_dict[main_hotel][score_type]
                compare_score = hotel_scores_dict[hotel][score_type]
                score_comparison = main_score - compare_score
                background_color = "#90EE90" if score_comparison > 0 else "#F76B69"  # Green if main_score is higher, red if lower
                comparison_text = f"{score_type.replace('Score', '')}: '{main_hotel}' = {main_score:.2f}, '{hotel}' = {compare_score:.2f}"
                comparisons.append((comparison_text, background_color))
            
            # Display each comparison with the determined background color
            for comparison, color in comparisons:
                st.markdown(
                    f"<div style='margin-bottom: 10px; padding: 10px; border-radius: 8px; background-color: {color};'>"
                    f"{comparison}"
                    "</div>", unsafe_allow_html=True
                )

main()