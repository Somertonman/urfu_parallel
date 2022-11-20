import streamlit as st
import requests
import pandas as pd

st.title('Masked language modeling')
st.write(
    'Pretrained model on English language using a masked language modeling (MLM) objective. It was introduced in this paper and first released in this repository. This model is uncased: it does not make a difference between english and English.')
text = st.text_input('Enter text', 'All students * URFU')
min_score_val = st.slider('Minimal score of returned tokens:', min_value=0.1, max_value=1.0, step=0.1,
                          label_visibility="visible")
n_of_results_val = st.slider('Minimal score of returned tokens:', min_value=1, max_value=5, label_visibility="visible")
if_words_only = st.checkbox('Words only', value=False)

result = st.button('Suggest predictions')
if result:
    response = requests.post('http://backend:8000/get_suggestions',
                             json={'sentence': text,
                                   'min_score': min_score_val,
                                   'n_of_results': n_of_results_val,
                                   'words_only': if_words_only})
    st.write('**Results:**')
    resp = response.json()
    if resp['status'] == 'ok':
        st.info('Successful request', icon="ℹ️")
        df = pd.DataFrame.from_dict(response.json()['data'])
        st.table(data=df)
    else:
        err_mg = resp['details']
        st.error(f'Error. {err_mg}', icon="🚨")
    # st.write(response.json()['data'][0]['sequence'])
