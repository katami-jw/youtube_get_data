import streamlit as st
import pandas as pd
from googleapiclient.discovery import build

st.title("Youtubeチャンネル調査")
st.write("気になるYouTubeチャンネルのチャンネルIDを入力してチャンネルの情報を見てみましょう")

with st.form("チャンネル情報を検索"):
    api_key=st.text_input('APIキー',type='password')
    channel_id=st.text_input('チャンネルID')
    submitted=st.form_submit_button('Submit')

if submitted:
    api_service_name = 'youtube'
    api_version = 'v3'
    #api_key = api_key

    youtube = build(api_service_name, api_version, developerKey=api_key)

    #チャンネル情報を取得
    channel_data = youtube.channels().list(
        part=['snippet','statistics'],
        id=channel_id,
        maxResults=1,
        ).execute()
    
    channel_data_df = pd.json_normalize(channel_data['items'])
    channel_data_dic = channel_data_df.to_dict(orient='records')

    #チャンネル情報を表示
    st.image(channel_data_dic[0]['snippet.thumbnails.medium.url'])
    st.write("チャンネル名▶",channel_data_dic[0]['snippet.title'])
    st.markdown(channel_data_dic[0]['snippet.description'])

    col1, col2, col3 = st.columns(3)
    col1.metric(label="総再生数", value=channel_data_dic[0]['statistics.viewCount'])
    col2.metric(label="動画数", value=channel_data_dic[0]['statistics.videoCount'])
    col3.metric(label="登録者数", value=channel_data_dic[0]['statistics.subscriberCount'])