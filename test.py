import streamlit as st
import pickle
import pandas as pd

## Application Backend ##

# To load medicine-dataframe from pickle in the form of dictionary
medicines_dict = pickle.load(open("medicine_dict.pkl", "rb"))
medicines = pd.DataFrame(medicines_dict)

# To load similarity-vector-data from pickle in the form of dictionary
similarity = pickle.load(open("similarity.pkl", "rb"))


def recommend(medicine):
    medicine_index = medicines[medicines["Drug_Name"] == medicine].index[0]
    distances = similarity[medicine_index]
    medicines_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_medicines = []
    for i in medicines_list:
        recommended_medicines.append(medicines.iloc[i[0]].Drug_Name)
    return recommended_medicines


## Application Frontend ##

# Title of the Application
st.title("Prescription Recommendation System")

# Custom CSS
st.markdown(
    """
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f2f6;
            color: #333;
            margin: 0;
            padding: 0;
        }
        h1 {
            color: #ff6666;
            background-color: #ffffcc;
            border: 2px solid #000;
            border-radius: 20px;
            padding: 10px;
            text-align: center;
            margin-bottom: 20px;
        }
        .stButton>button {
            font-size: 18px;
            font-weight: bold;
            background-color: #328188;
            color: #fff;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            margin-bottom: 20px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .stButton>button:hover {
            background-color: #2c6e70;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            background-color: #a1d6ea;
            padding: 15px;
            border-radius: 10px;
            font-size: 18px;
            margin-bottom: 10px;
        }
        a {
            padding: 5px 10px;
            background-color: #000;
            color: #fff;
            border: 1px solid #000;
            border-radius: 5px;
            text-decoration: none;
            transition: background-color 0.3s;
        }
        a:hover {
            background-color: #333;
        }
        img {
            display: block;
            margin-left: auto;
            margin-right: auto;
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Searchbox
selected_medicine_name = st.selectbox(
    "Type your medicine name whose alternative is to be recommended",
    medicines["Drug_Name"].values,
)

# Recommendation Program
if st.button("Recommend Medicine"):
    recommendations = recommend(selected_medicine_name)
    j = 1
    for i in recommendations:
        st.write(j, i)  
        st.write(
            "Click here -> " + " https://pharmeasy.in/search/all?name=" + i
        ) 
        j += 1

# Image
st.image(
    "images/image.png", caption="Recommended Medicines", use_column_width=True
)
