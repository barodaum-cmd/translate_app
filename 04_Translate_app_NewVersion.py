##### 기본 정보 불러오기 ####
# Streamlit 패키지 추가
import streamlit as st
# OpenAI 패키지 추가
import openai
# 구글 번역 패키지 추가
import asyncio 
from googletrans import Translator
# Deepl 번역 패키지 추가
import deepl
# 파파고 API요청을 위한 Requests 패키지 추가 
import requests

##### 기능 구현 함수 #####
# ChatGPT 번역
def gpt_translate(messages, apikey):
    client = openai.OpenAI(api_key = apikey)
    messages_prompt = [
        {"role": "system", "content": f"You are a helpful language translation assistant. Your task is to accurately and naturally translate the user's message into Korean. Provide only the translated text in your response, without any additional comments or explanations."},
        {"role": "user", "content": f"Translate this text: '{messages}'"}
    ]    
    response = client.chat.completions.create(
    model="gpt-5",
    messages=messages_prompt
    )

    return response.choices[0].message.content.strip()

# 구글 번역
async def google_trans(messages):
    async with Translator() as translator:
        result = await translator.translate(messages, dest="ko")

    return result.text

# 디플 번역
def deepl_translate(text, deeplAPI):
    translator = deepl.Translator(deeplAPI)
    result = translator.translate_text(text, target_lang="KO")
    return result.text

##### 메인 함수 #####
def main():
    # 기본 설정
    st.set_page_config(
        page_title="번역 플랫폼 모음",
        layout="wide")

    # session state 초기화
    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENAI_API"] = ""

    if "DeeplAPI" not in st.session_state:
        st.session_state["DeeplAPI"] = ""


    # 사이드바 바 생성
    with st.sidebar:

        # Open AI API 키 입력받기
        st.session_state["OPENAI_API"] = st.text_input(label='OPENAI API 키', placeholder='Enter Your OpenAI API Key', value='',type='password')

        st.markdown('---')

        # Deepl API ID/PW 입력받기
        st.session_state["DeeplAPI"] = st.text_input(label='Deepl API 키', placeholder='Enter Your Deepl API API Key', value='',type='password')
    
        st.markdown('---')

    # 제목 
    st.header('번역 플랫폼 비교하기 프로그램')
    # 구분선
    st.markdown('---')
    st.subheader("번역을 하고자 하는 텍스트를 입력하세요")
    txt = st.text_area(label="",placeholder="input English..", height=500)
    st.markdown('---')

    st.subheader("ChatGPT 번역 결과")
    st.text("https://openai.com/blog/chatgpt")
    if st.session_state["OPENAI_API"] and txt:
        result = gpt_translate(txt,st.session_state["OPENAI_API"])
        st.info(result)
    else:
        st.info('API 키를 넣으세요')
    st.markdown('---')

    st.subheader("구글 번역 결과")
    st.text("https://translate.google.co.kr/")
    if txt:
        result = asyncio.run(google_trans(txt))

        st.info(result)
    else:
        st.info("API키가 필요 없습니다")
    st.markdown('---')

    st.subheader("Deepl 번역 결과")
    st.text("https://www.deepl.com/translator")
    if st.session_state["DeeplAPI"] and txt:
        result = deepl_translate(txt,st.session_state["DeeplAPI"])
        st.info(result)
    else:
        st.info('API 키를 넣으세요')
    st.markdown('---')

if __name__=="__main__":
    main()
