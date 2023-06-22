# -*- coding: utf-8 -*-
import streamlit as st

def run_declaration():
    buff, col, buff2 = st.columns([1, 3, 1])
    with col :
        input_user_name=st.text_input("이름", key="name",max_chars=5)
        input_phone_number=st.text_input("전화번호",key="phonenumber",max_chars=13)
        input_text=st.text_area("신고 및 문의 내용",key="declaration",height=30)
    buff3, col1, buff4 = st.columns([2, 1, 1.5])
    with col1:
        checkbox = st.checkbox('개인 정보 이용 동의')
        btn_clicked = st.button('전송',disabled=(checkbox is False))
        if btn_clicked:
            con = st.container()
            con.caption("Result")
            if not str(input_user_name):
                con.error("이름을 확인해 주세요")
            elif not str(input_phone_number):
                con.error("전화 번호를 확인해 주세요")
            elif not str(input_text):
                con.error("접수 내용을 확인해 주세요")
            else:
                con.warning('접수가 완료 되었습니다. 순차적으로 처리하여 연락드리겠습니다.')
        else:
            st.write('전송을 누르면 접수가 완료됩니다.')

if __name__ == "__main__":
    run_declaration()