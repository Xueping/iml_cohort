# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.shortcuts import render
from keras import backend as K
from keras.layers import Input, Dense
from keras.models import Model
from numpy.random import seed
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import train_test_split

from django.conf  import settings
import pandas as pd
import tensorflow as tf
from scipy import sparse, io
# from pandas.tests.io.parser import index_col


# Create your views here.
def topic(df, num_topics=5):
    """
    Represent the topics features of original features
    :param df: pandas DataFrame
    :param num_topics: the number of topics, default=5
    :return: the probability vectors of each topics the entry belongs to
    """
#     X, y = df[df.columns[:-1]], df[df.columns[-1]]
    lda = LatentDirichletAllocation(n_components=num_topics,
                                    max_iter=5,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    return lda.fit_transform(df)


def encoder(df, encoding_dim=2):
    """
    Represent the auto encoder features
    :param df: pandas DataFrame of original features
    :param encoding_dim: the dimension of encoded features
    :return: the output encoded features at encoding_dim
    """
    sess = tf.Session()
    K.set_session(sess)
    
    df = df.todense()

    X, y = df[:,:-1], df[:,-1]
    ncol = X.shape[1]  # the number of columns
    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.3, random_state=seed(2017))

#     X_train = X_train.as_matrix()
#     X_test = X_test.as_matrix()
#     X = X.as_matrix()

    # Auto encoder structure
    # InputLayer (None, 10)
    #      Dense (None, 5)
    #      Dense (None, 10)
    input_dim = Input(shape=(ncol,))
    # The encoder layer
    encoded = Dense(encoding_dim, activation='relu')(input_dim)
    # The decoder layer
    decoded = Dense(ncol, activation='sigmoid')(encoded)
    autoencoder = Model(inputs=input_dim, outputs=decoded)
    autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
    autoencoder.fit(X_train, X_train, epochs=50, batch_size=100, shuffle=True, validation_data=(X_test, X_test))
    # The single encoder model
    encoder = Model(inputs=input_dim, outputs=encoded)
#     encoded_input = Input(shape=(encoding_dim,))
    encoded_out = encoder.predict(X)
    return encoded_out


def features_representation(request):
    """
    Features representation of original, topics, and auto encoder features
    :param request: request from the form in feature_representation/features.html
    :return: render the representation of features in feature_representation/results.html
    """
    if request.method == 'POST':
        representation = str(request.POST.get("representation", ""))
                
#         df_data = pd.read_csv(os.path.join(settings.BASE_DIR, 'data/outcome_data.csv'), index_col=0 )
        df_data = io.mmread(os.path.join(settings.BASE_DIR, 'data/outcome_data.mtx'))
#         df_data = pd.read_csv('./data/DIAGNOSES_ICD.csv').sample(20)  # load the csv file of original features
#         df_origi = df_data[df_data.columns[1:]]  # original features
        
        
        if representation == "topicmodel":            
            num_topics = int(request.POST.get("num_topics", ""))  # get the number of topics
            mdl = topic(df_data, num_topics)
            cols = ['topic_{}'.format(i) for i in range(len(mdl[0]))]
            df_reperent = pd.DataFrame(mdl, columns=cols)
#             df_reperent.to_csv(os.path.join(settings.BASE_DIR, 'data/features_topics.csv'), index=False)
        elif representation == "autoencoder": 
            num_dim = int(request.POST.get("num_dim", ""))  # get the dimension of encoded features            
            mdl = encoder(df_data, num_dim)            
            cols = ['dim_{}'.format(i) for i in range(len(mdl[0]))]
            df_reperent = pd.DataFrame(mdl, columns=cols)
            
        else:
            df_reperent = df_data
#             df_reperent.to_csv(os.path.join(settings.BASE_DIR, 'data/features_autoencoder.csv'), index=False)
            
        df_reperent.to_csv(os.path.join(settings.BASE_DIR, 'data/features_rep.csv'), index=False)       
        # context is a dict of html code, containing three types of features representation
        context = {
#             'origi': df_data.sample(20).to_html(),
            'reprnt': df_reperent.sample(20).to_html(classes=['table', 'table-striped', 'table-bordered'], index=False),
#             'rep':representation
        }
        return render(request,'feature_representation/stp5-rep-view.html', context)
    else:
        return render(request, 'feature_representation/stp4-fea-representation.html')


if __name__ == "__main__":
    df_data = pd.read_csv('../data/DIAGNOSES_ICD.csv').sample(20)
    df_data = df_data.fillna(0)
    # print df.head()
    probs = topic(df_data)
    encoded_out = encoder(df_data)

    col_probs = ['topic_{}'.format(i) for i in range(len(probs[0]))]
    col_encoded = ['dim_{}'.format(i) for i in range(len(encoded_out[0]))]

    df_probs = pd.DataFrame(probs, columns=col_probs)
    df_encoded = pd.DataFrame(encoded_out, columns=col_encoded)