import requests
import streamlit as st


HEADER = "Котики"
MORE_KITTENS = "Хочу котика!"
CAT_API = "https://api.thecatapi.com/v1/images/search"
TOKEN = st.secrets["cat_api_token"]


def get_random_cat():
    response = requests.get(CAT_API, params={"x-api-key": TOKEN})
    return response.json()[0]["url"]


def main():
    st.markdown(f"# {HEADER} 😺")
    st.sidebar.markdown(f"# {HEADER} 😺️")

    if st.button(MORE_KITTENS):
        url = get_random_cat()
        st.markdown(f"![Alt Text]({url})")


if __name__ == "__main__":
    main()
