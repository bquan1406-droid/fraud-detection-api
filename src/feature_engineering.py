import pandas as pd
import numpy as np
import joblib

def load_frequency_dicts():
    base_path = 'models/frequency_dicts/'
    dicts = {
        'card1_freq': joblib.load(base_path + 'card1_freq_dict.pkl'),
        'card4_freq': joblib.load(base_path + 'card4_freq_dict.pkl'),
        'product_freq': joblib.load(base_path + 'product_freq_dict.pkl'),
        'addr1_freq': joblib.load(base_path + 'addr1_freq_dict.pkl'),
        'addr2_freq': joblib.load(base_path + 'addr2_freq_dict.pkl'),
        'card2_freq': joblib.load(base_path + 'card2_freq_dict.pkl'),
        'card3_freq': joblib.load(base_path + 'card3_freq_dict.pkl'),
        'pemail_freq': joblib.load(base_path + 'pemail_freq_dict.pkl'),
        'remail_freq': joblib.load(base_path + 'remail_freq_dict.pkl'),
        'card1_card2_freq': joblib.load(base_path + 'card1_card2_freq_dict.pkl'),
        'card1_amt_mean': joblib.load(base_path + 'card1_amt_mean_dict.pkl'),
        'card1_amt_std': joblib.load(base_path + 'card1_amt_std_dict.pkl'),
        'card1_tx_count': joblib.load(base_path + 'card1_tx_count_dict.pkl'),
        'card2_amt_mean': joblib.load(base_path + 'card2_amt_mean_dict.pkl'),
        'addr1_amt_mean': joblib.load(base_path + 'addr1_amt_mean_dict.pkl'),
        'addr1_tx_count': joblib.load(base_path + 'addr1_tx_count_dict.pkl')
    }
    return dicts

def engineer_features(tx, dicts):
    features = {}
    
    features['card1_freq'] = dicts['card1_freq'].get(tx.card1, 0)
    features['card4_freq'] = dicts['card4_freq'].get(tx.card4, 0)
    features['product_freq'] = dicts['product_freq'].get(tx.ProductCD, 0)
    features['addr1_freq'] = dicts['addr1_freq'].get(tx.addr1, 0)
    features['addr2_freq'] = dicts['addr2_freq'].get(tx.addr2, 0)
    features['card2_freq'] = dicts['card2_freq'].get(tx.card2 if tx.card2 else -1, 0)
    features['card3_freq'] = dicts['card3_freq'].get(tx.card3 if tx.card3 else -1, 0)
    
    pemail = tx.P_emaildomain if tx.P_emaildomain else 'missing'
    remail = tx.R_emaildomain if tx.R_emaildomain else 'missing'
    features['pemail_freq'] = dicts['pemail_freq'].get(pemail, 0)
    features['remail_freq'] = dicts['remail_freq'].get(remail, 0)
    
    card1_card2_key = str(tx.card1) + '_' + str(tx.card2 if tx.card2 else -1)
    features['card1_card2_freq'] = dicts['card1_card2_freq'].get(card1_card2_key, 0)
    
    features['amt_dollars'] = int(tx.TransactionAmt)
    features['amt_cents'] = int((tx.TransactionAmt - int(tx.TransactionAmt)) * 100)
    
    features['card1_amt_mean'] = dicts['card1_amt_mean'].get(tx.card1, 0)
    features['card1_amt_std'] = dicts['card1_amt_std'].get(tx.card1, 0)
    features['card1_tx_count'] = dicts['card1_tx_count'].get(tx.card1, 0)
    features['card2_amt_mean'] = dicts['card2_amt_mean'].get(tx.card2 if tx.card2 else -1, 0)
    features['addr1_amt_mean'] = dicts['addr1_amt_mean'].get(tx.addr1, 0)
    features['addr1_tx_count'] = dicts['addr1_tx_count'].get(tx.addr1, 0)
    
    d_columns = ['D1','D2','D3','D4','D5','D6','D7','D8','D9','D10','D11','D12','D13','D14','D15']
    d_count = 0
    for col in d_columns:
        value = getattr(tx, col, None)
        if value is not None and not pd.isna(value):
            d_count += 1
    features['d_count'] = d_count
    
    features['P_email_missing'] = 1 if tx.P_emaildomain is None else 0
    features['R_email_missing'] = 1 if tx.R_emaildomain is None else 0
    features['same_email_domain'] = 1 if tx.P_emaildomain == tx.R_emaildomain else 0
    
    features['card1_last_tx_diff'] = 0
    
    for i in range(1, 340):
        v_col = f'V{i}'
        features[v_col] = getattr(tx, v_col, None)
    
    return features
