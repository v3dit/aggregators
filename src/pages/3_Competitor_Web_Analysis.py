import pandas as pd
import streamlit as st
import openai
import re

# Set your OpenAI API key
openai.api_key = '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'

# Function to generate insights with GPT-3.5-turbo
# def generate_insights_with_gpt(ettara_data, competitor_data):
#     try:
#         # Construct the prompt
#         prompt = f"Summarize a comparison and provide insights on how Ettara Coffee, with ratings of {ettara_data['Ratings']}, cuisines offered ({ettara_data['Cuisines']}), and an average cost of ${ettara_data['Average Cost']} for two, compares to {competitor_data['Name']} which has ratings of {competitor_data['Ratings']}, offers cuisines ({competitor_data['Cuisines']}), and has an average cost of ${competitor_data['Average Cost']} for two. Consider aspects like service quality, menu diversity, ambiance, and price affordability. Give output in bullet points"
        
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a highly knowledgeable assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             prompt=prompt,
#             temperature=0.5,
#             max_tokens=250
#         )
        
#         return response.choices[0].message['content']
#     except Exception as e:
#         return f"An error occurred: {str(e)}"

# Load competitors data including Ettara Coffee's details

def load_data():
    # Replace this path with the actual path to your cleaned competitors CSV file
    file_path = 'v3dit/aggregators/src/pages/cleaned_competitors_final.csv'
    return pd.read_csv(file_path)

data = load_data()

# Extracting Ettara Coffee's data
ettara_coffee_data = data[data['Name'].str.contains('Ettara|Ettarra', case=False, regex=True)].iloc[0]

# Preparing competitors data by excluding Ettara Coffee
competitors_data = data[~data['Name'].str.contains('Ettara|Ettarra', case=False, regex=True)]

# Streamlit UI setup
st.title('Ettara Coffee vs. Competitors')
st.write('#### This feature facilitates comparing Ettara Coffee with competitors. After selecting a competitor, it displays key attributes like ratings, cuisines, and average cost. Click "Generate Insights" to leverage GPT-3.5-turbo for insightful comparisons covering service quality, menu diversity, ambiance, and price affordability.')
# st.markdown("""
# <style>
# .styled-table {
#     font-size: 20px;
#     background-color: #001f3f;
#     color: white;
# }
# .styled-table th {
#     color: white;
# }
# .styled-table td, .styled-table tr, .styled-table th {
#     color: white;
# }
# </style>
# """, unsafe_allow_html=True)

# Dropdown to select a competitor
selected_competitor = st.selectbox('Select a Competitor', competitors_data['Name'].unique())

# Display the selected competitor's data
competitor_data = competitors_data[competitors_data['Name'] == selected_competitor].iloc[0]

# Function to compare Ettara Coffee with the selected competitor
def compare_shops(ettara_data, competitor_data):
    comparison_data = {
        'Attribute': ['Ratings', 'Cuisines', 'Average Cost', 'Known For', 'Frequent Searches'],
        'Ettara Coffee': [
            ettara_data['Ratings'],
            ettara_data['Cuisines'],
            f"${ettara_data['Average Cost']} for 2",
            ettara_data['Known For'],
            ettara_data['Frequent Searches']
        ],
        selected_competitor: [
            competitor_data['Ratings'],
            competitor_data['Cuisines'],
            f"${competitor_data['Average Cost']} for 2",
            competitor_data['Known For'],
            competitor_data['Frequent Searches']
        ]
    }
    df = pd.DataFrame(comparison_data)
    return df.style.apply(lambda x: ["background: #001f3f; color: white"] * len(x), axis=1)


# Displaying the comparison table
comparison_df = compare_shops(ettara_coffee_data, competitor_data)
st.table(comparison_df)

# Button to generate and display insights
if st.button('Generate Insights'):
    # insights = generate_insights_with_gpt(ettara_coffee_data, competitor_data)
    # st.write(insights)
    final_prompt= f"Summarize a comparison and provide insights on how Ettara Coffee, {compare_shops(ettara_coffee_data, competitor_data).to_string()}. Also generate a summary using bullet points for strenghts weaknesses and overall aspects of the performance of just the company: {ettara_coffee_data.to_string()}. "
    response_final = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a highly knowledgeable assistant. Reply in only plain text without any encoding except bullet points."},
                    {"role": "user", "content": final_prompt}
                ],
                
                temperature=0.5,
                max_tokens=550
            )
    st.write(str(response_final.choices[0].message['content']))
    # st.write(str(re.sub(r'[^\w\s]','',response_final.choices[0].message['content'])))