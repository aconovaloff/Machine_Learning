
# coding: utf-8


# **File descriptions** 
#     [Detroit Open Data Portal](https://data.detroitmi.gov/)
#     train.csv - the training set (all tickets issued 2004-2011)
#     test.csv - the test set (all tickets issued 2012-2016)
#     addresses.csv & latlons.csv - mapping from ticket id to addresses, and from addresses to lat/lon coordinates. 
#      Note: misspelled addresses may be incorrectly geolocated.
# 
# <br>
# 
# **Data fields**
# 
# train.csv & test.csv
# 
#     ticket_id - unique identifier for tickets
#     agency_name - Agency that issued the ticket
#     inspector_name - Name of inspector that issued the ticket
#     violator_name - Name of the person/organization that the ticket was issued to
#     violation_street_number, violation_street_name, violation_zip_code - Address where the violation occurred
#     mailing_address_str_number, mailing_address_str_name, city, state, zip_code, non_us_str_code, country - Mailing address of the violator
#     ticket_issued_date - Date and time the ticket was issued
#     hearing_date - Date and time the violator's hearing was scheduled
#     violation_code, violation_description - Type of violation
#     disposition - Judgment and judgement type
#     fine_amount - Violation fine amount, excluding fees
#     admin_fee - $20 fee assigned to responsible judgments
# state_fee - $10 fee assigned to responsible judgments
#     late_fee - 10% fee assigned to responsible judgments
#     discount_amount - discount applied, if any
#     clean_up_cost - DPW clean-up or graffiti removal cost
#     judgment_amount - Sum of all fines and fees
#     grafitti_status - Flag for graffiti violations
#     
# train.csv only
# 
#     payment_amount - Amount paid, if any
#     payment_date - Date payment was made, if it was received
#     payment_status - Current payment status as of Feb 1 2017
#     balance_due - Fines and fees still owed
#     collection_status - Flag for payments in collections
#     compliance [target variable for prediction] 
#      Null = Not responsible
#      0 = Responsible, non-compliant
#      1 = Responsible, compliant
#     compliance_detail - More information on why each ticket was marked compliant or non-compliant
# 
# 
# ___
# 
# ## Evaluation
# 
# Your predictions will be given as the probability that the corresponding blight ticket will be paid on time.
# 
# The evaluation metric is the Area Under the ROC Curve (AUC). 
# 

# Example:
# 
#     ticket_id
#        284932    0.531842
#        285362    0.401958
#        285361    0.105928
#        285338    0.018572
#                  ...
#        376499    0.208567
#        376500    0.818759
#        369851    0.018528
#        Name: compliance, dtype: float32
#        


# In[27]:

import pandas as pd
import numpy as np

def blight_model():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn import preprocessing
    from sklearn.preprocessing import LabelEncoder
    from collections import defaultdict
    
   
    comp = pd.read_csv('train.csv', engine='python')
    comp_test = pd.read_csv('test.csv', engine='python')
    #test_y = comp_test['compliance']
    #del (comp_test['compliance'])
    test_X = comp_test[['fine_amount', 'city','state','grafitti_status','judgment_amount',
                        'violation_code','ticket_issued_date','disposition','clean_up_cost','violator_name']]
    comp = comp[np.isfinite(comp['compliance'])]
    train_y = comp['compliance']
    train_X = comp
    del (train_X['payment_amount'],train_X['payment_date'],train_X['payment_status'], 
         train_X['balance_due'],train_X['collection_status'],train_X['compliance'], train_X['compliance_detail'],
        train_X['violation_zip_code'], train_X['non_us_str_code'])
   #clf = RandomForestClassifier(n_estimators = 5,
                            #random_state=0).fit(train_X, train_y)
    #train_X =  train_X.dropna(axis=0, how='any')
    #train_X = train_X.fillna(0)
    test_X['city'] = test_X['city'].fillna('NaN')
    test_X['state'] = test_X['state'].fillna('NaN')
    train_X['city'] = train_X['city'].fillna('NaN')
    train_X['state'] = train_X['state'].fillna('NaN')   
    test_X['grafitti_status'] = test_X['grafitti_status'].fillna('NaN')
    train_X['grafitti_status'] = train_X['grafitti_status'].fillna('NaN')
    test_X['violator_name'] = test_X['violator_name'].fillna('NaN')
    train_X['violator_name'] = train_X['violator_name'].fillna('NaN')
    #test_X['hearing_date'] = test_X['hearing_date'].fillna('NaN')
    #train_X['hearing_date'] = train_X['hearing_date'].fillna('NaN')
    trial = train_X[['fine_amount', 'city','state','grafitti_status','judgment_amount',
                     'violation_code','ticket_issued_date','disposition','clean_up_cost','violator_name']]
    #train_X = train_X.stack()
    #train_X[pd.isnull(train_X)]  = 'NaN'
    #train_X = train_X.unstack()
    le = LabelEncoder()
 #  d = defaultdict(le)
    #trial = le.fit_transform(trial['city'])
    trial['city'] = le.fit_transform(trial['city'])
    test_X['city'] = le.fit_transform(test_X['city'])
    trial['state'] = le.fit_transform(trial['state'])
    test_X['state'] = le.fit_transform(test_X['state'])
    trial['grafitti_status'] = le.fit_transform(trial['grafitti_status'])
    test_X['grafitti_status'] = le.fit_transform(test_X['grafitti_status'])
    trial['violation_code'] = le.fit_transform(trial['violation_code'])
    test_X['violation_code'] = le.fit_transform(test_X['violation_code'])
    trial['ticket_issued_date'] = le.fit_transform(trial['ticket_issued_date'])
    test_X['ticket_issued_date'] = le.fit_transform(test_X['ticket_issued_date'])
    #trial['hearing_date'] = le.fit_transform(trial['hearing_date'])
    #test_X['hearing_date'] = le.fit_transform(test_X['hearing_date'])
    trial['disposition'] = le.fit_transform(trial['disposition'])
    test_X['disposition'] = le.fit_transform(test_X['disposition'])
    trial['violator_name'] = le.fit_transform(trial['violator_name'])
    test_X['violator_name'] = le.fit_transform(test_X['violator_name'])
    #trial['state'] = le.fit_transform(trial['state'])
    
    clf = RandomForestClassifier(n_estimators = 10,random_state=0).fit(trial, train_y)
    comp_test['compliance'] = clf.predict_proba(test_X)[:,1]
    answer = comp_test[['ticket_id', 'compliance']]
    answer.set_index('ticket_id', inplace=True)
    #train_X.apply(le.fit_transform)
    #return clf.score(trial, train_y)
    #return clf.evaluation_function(test_X)
    #with train_X.option_context('display.max_rows', None, 'display.max_columns', 3):print(train_X)
    #answer = clf.predict_proba(test_X).shape
    return answer.squeeze() 
    #return train_X['clean_up_cost']
blight_model()


# In[ ]:

blight_model()

