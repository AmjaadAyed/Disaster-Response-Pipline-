import sys
import pandas as pd
import numpy as np
import sklearn 
from sqlalchemy import create_engine
from nltk.tokenize import word_tokenize 
from nltk.stem import WordNetLemmatizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report
import re
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, make_scorer
from sklearn.model_selection import train_test_split, GridSearchCV
import pickle
import nltk
nltk.download(['punkt', 'wordnet'])


def load_data(database_filepath):
    engine = create_engine('sqlite:///' + database_filepath)
    df = pd.read_sql("Messages", engine)
    X = df['message']
    Y = df.iloc[:,4:]
    category_names = Y.columns
    return X, Y, category_names


def tokenize(text):
    url_regex = 'http[s]?://(?:[a-z-AZ]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    detected_urls = re.findall(url_regex, text)
    for url in detected_urls:
        text = text.replace(url, "urlplaceholder")

    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def build_model():
    pipeline = Pipeline([
    ('vect', CountVectorizer(tokenizer = tokenize)),
    ('tfidf', TfidfTransformer()),
    ('clf', MultiOutputClassifier(RandomForestClassifier()))
    ])
    

    #model parameters for GridSearchCV
    parameters = {  'vect__max_df': (0.75, 1.0),
                    'clf__estimator__n_estimators': [10, 20],
                    'clf__estimator__min_samples_split': [2, 5]
              }
    model = GridSearchCV (pipeline, param_grid= parameters, n_jobs=-1, verbose =7 )
    return model


def evaluate_model(model, X_test, Y_test, category_names):
    Y_predict =model.predict(X_test)
    for n, column in enumerate(category_names):
        print(column, classification_report(Y_test.iloc[:,n],Y_predict[:,n]))
    


def save_model(model, model_filepath):
    pickle.dump(model.best_estimator_, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()