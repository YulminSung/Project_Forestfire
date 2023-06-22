# -*- coding: utf-8 -*-
import streamlit as st
from streamlit_player import st_player, _SUPPORTED_EVENTS

def run_youtubeNews():
    c1, c2, c3 = st.columns([3, 3, 2])

    with c3:
        st.subheader("Parameters")

        options = {
            "events": st.multiselect("Events to listen", _SUPPORTED_EVENTS, ["onProgress"]),
            "progress_interval": 1000,
            "volume": st.slider("Volume", 0.0, 1.0, 1.0, .01),
            "playing": st.checkbox("Playing", False),
            "loop": st.checkbox("Loop", False),
            "controls": st.checkbox("Controls", True),
            "muted": st.checkbox("Muted", False),
        }

    with c1:
        url1 = st.text_input("First URL", "https://www.youtube.com/watch?v=ZP4s4CEGMJw")
        st_player(url1, **options, key="youtube_player1")


    with c2:
        url2 = st.text_input("Second URL", "https://www.youtube.com/watch?v=ya8MurTg4x0")
        st_player(url2, **options, key="youtube_player2")

    c4, c5, c6 = st.columns([3, 3, 2])
    with c4:
        url3 = st.text_input("Third URL", "https://www.youtube.com/watch?v=ECZBcCVNogI")
        st_player(url3, **options, key="youtube_player3")


    with c5:
        url4 = st.text_input("Fourth URL", "https://www.youtube.com/watch?v=cRIGefdVj-g")
        st_player(url4, **options, key="youtube_player4")

    with c6:
        with st.expander("SUPPORTED PLAYERS", expanded=False):
            st.write("""
               - Dailymotion
               - Facebook
               - Mixcloud
               - SoundCloud
               - Streamable
               - Twitch
               - Vimeo
               - Wistia
               - YouTube
               <br/><br/>
               """, unsafe_allow_html=True)

if __name__ == "__main__":
    run_youtubeNews()