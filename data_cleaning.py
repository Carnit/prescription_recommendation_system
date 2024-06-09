import pandas as pd
import numpy as np
from nltk.corpus import stopwords  # Import stopwords directly
from nltk.stem import PorterStemmer  # Import PorterStemmer directly
from sklearn.feature_extraction.text import CountVectorizer

# Read data (replace 'medicine.csv' with your actual file path)
medicines = pd.read_csv("medicine.csv")

# Data cleaning
medicines.dropna(inplace=True)  
medicines.drop_duplicates(inplace=True)  

# Data pre-processing
def clean_text(text):
    """Cleans a text string by removing extra spaces, converting to lowercase,
  and applying stemming."""
    words = text.split()
    words = [word.replace(" ", "") for word in words]  
    words = [word.lower() for word in words]  
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]  
    return words


medicines["tags"] = (
    medicines[["Description", "Reason"]]
    .apply(lambda x: " ".join(clean_text(x.iloc[0])), axis=1)
    .str.lower()
)


new_df = medicines[[ 'Drug_Name', 'tags']]


stop_words = stopwords.words('english')  
cv = CountVectorizer(stop_words=stop_words, max_features=5000)  
X = cv.fit_transform(new_df['tags']).toarray()  
feature_names = cv.get_feature_names_out() 
