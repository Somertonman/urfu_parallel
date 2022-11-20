import streamlit as st
import requests

st.title('Определение тональности текста')
text = st.text_input('Введите текст', 'Я люблю распределенные вычисления')
result = st.button('Определить тональность')
if result:
    response = requests.post('http://backend:8000/get_suggestions',
                             json={'sentence': text})
    st.write('**Результаты распознавания:**')
    st.write(response.json()['data'][0]['sequence'])
