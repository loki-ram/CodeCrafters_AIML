import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

def train_and_save_model(csv_path='jobs_data.csv', model_path='job_matching_model.pkl'):
    # Load job data
    jobs_df = pd.read_csv(csv_path)
    
    # Replace NaN values in the 'description', 'skills_desc', and 'title' with an empty string
    jobs_df['description'] = jobs_df['description'].fillna('')
    jobs_df['skills_desc'] = jobs_df['skills_desc'].fillna('')
    jobs_df['title'] = jobs_df['title'].fillna('')
    
    # Combine the title, description, and skills_desc for job text
    jobs_df['job_text'] = jobs_df['title'] + " " + jobs_df['description'] + " " + jobs_df['skills_desc']
    
    # Initialize the TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')

    # Fit and transform the job text data
    job_vectors = vectorizer.fit_transform(jobs_df['job_text'])
    
    # Save the model and vectorizer using joblib
    joblib.dump({'vectorizer': vectorizer, 'job_data': jobs_df}, model_path)
    
    print(f"Model saved successfully to {model_path}")
    
# Call this function to train and save the model
if __name__ == '__main__':
    train_and_save_model()
