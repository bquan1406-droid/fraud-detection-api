import pandas as pd
import numpy as np

def engineer_features(tx: dict, card1_freq_dict: dict, card4_freq_dict: dict, product_freq_dict: dict, addr1_freq_dict: dict, addr2_freq_dict: dict, card2_freq_dict: dict, card3_freq_dict: dict, pemail_freq_dict: dict, remail_freq_dict: dict, card1_card2_freq_dict: dict, card1_amt_mean_dict: dict, card1_amt_std_dict: dict, card1_tx_count_dict: dict, card2_amt_mean_dict: dict, addr1_amt_mean_dict: dict, addr1_tx_count_dict: dict) -> pd.DataFrame:
    
    df = pd.DataFrame([tx])
    
    card1_freq = card1_freq_dict.get(df['card1'].iloc[0], 0)
    card4_freq = card4_freq_dict.get(df['card4'].iloc[0], 0)
    product_freq = product_freq_dict.get(df['ProductCD'].iloc[0], 0)
    addr1_freq = addr1_freq_dict.get(df['addr1'].iloc[0], 0)
    addr2_freq = addr2_freq_dict.get(df['addr2'].iloc[0], 0)
    card2_freq = card2_freq_dict.get(df['card2'].iloc[0], 0)
    card3_freq = card3_freq_dict.get(df['card3'].iloc[0], 0)
    pemail_freq = pemail_freq_dict.get(df['P_emaildomain'].iloc[0], 0)
    remail_freq = remail_freq_dict.get(df['R_emaildomain'].iloc[0], 0)
    card1_card2_key = str(df['card1'].iloc[0]) + '_' + str(df['card2'].iloc[0])
    card1_card2_freq = card1_card2_freq_dict.get(card1_card2_key, 0)
    
    amt_dollars = int(df['TransactionAmt'].iloc[0])
    amt_cents = int((df['TransactionAmt'].iloc[0] - amt_dollars) * 100)
    
    card1_amt_mean = card1_amt_mean_dict.get(df['card1'].iloc[0], 0)
    card1_amt_std = card1_amt_std_dict.get(df['card1'].iloc[0], 0)
    card1_tx_count = card1_tx_count_dict.get(df['card1'].iloc[0], 0)
    
    card2_amt_mean = card2_amt_mean_dict.get(df['card2'].iloc[0], 0)
    addr1_amt_mean = addr1_amt_mean_dict.get(df['addr1'].iloc[0], 0)
    addr1_tx_count = addr1_tx_count_dict.get(df['addr1'].iloc[0], 0)
    
    d_columns = ['D1','D2','D3','D4','D5','D6','D7','D8','D9','D10','D11','D12','D13','D14','D15']
    d_count = 0
    for col in d_columns:
        if col in df and pd.notna(df[col].iloc[0]):
            d_count += 1
    
    p_email_missing = 1 if pd.isna(df['P_emaildomain'].iloc[0]) else 0
    r_email_missing = 1 if pd.isna(df['R_emaildomain'].iloc[0]) else 0
    same_email_domain = 1 if df['P_emaildomain'].iloc[0] == df['R_emaildomain'].iloc[0] else 0
    
    card1_last_tx_diff = 0
    
    features = {
        'card1_freq': card1_freq,
        'card4_freq': card4_freq,
        'product_freq': product_freq,
        'amt_dollars': amt_dollars,
        'amt_cents': amt_cents,
        'card1_amt_mean': card1_amt_mean,
        'card1_amt_std': card1_amt_std,
        'card1_tx_count': card1_tx_count,
        'd_count': d_count,
        'addr1_freq': addr1_freq,
        'addr2_freq': addr2_freq,
        'card2_freq': card2_freq,
        'card3_freq': card3_freq,
        'card1_card2_freq': card1_card2_freq,
        'P_email_missing': p_email_missing,
        'R_email_missing': r_email_missing,
        'same_email_domain': same_email_domain,
        'pemail_freq': pemail_freq,
        'remail_freq': remail_freq,
        'card2_amt_mean': card2_amt_mean,
        'addr1_amt_mean': addr1_amt_mean,
        'card1_last_tx_diff': card1_last_tx_diff,
        'addr1_tx_count': addr1_tx_count
    }
    
    for v_col in [f'V{i}' for i in range(1, 340)]:
        features[v_col] = df.get(v_col, np.nan).iloc[0] if v_col in df else np.nan
    
    features['ProductCD_encoded'] = None
    features['card4_encoded'] = None
    
    return pd.DataFrame([features])
