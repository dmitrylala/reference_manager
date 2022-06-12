import requests
import streamlit as st


HEADER = "Котики"
MORE_KITTENS = "Хочу котика!"
MORE_KITTENS_GIF = "Хочу гифку с котиком!"
CAT_API = "https://api.thecatapi.com/v1/images/search"
TOKEN = st.secrets["cat_api_token"]


def get_random_cat():
    response = requests.get(CAT_API, params={"x-api-key": TOKEN})
    return response.json()[0]["url"]


def get_random_cat_gif():
    while True:
        response = requests.get(CAT_API, params={"x-api-key": TOKEN})
        url = response.json()[0]["url"]
        if url.endswith(".gif"):
            return url


def main():
    st.markdown(f"# {HEADER} 😺")
    st.sidebar.markdown(f"# {HEADER} 😺️")

    more_kittens = st.button(MORE_KITTENS)
    more_kittens_gif = st.button(MORE_KITTENS_GIF)

    if more_kittens:
        st.markdown(f"![Alt Text]({get_random_cat()})")

    if more_kittens_gif:
        st.markdown(f"![Alt Text]({get_random_cat_gif()})")


if __name__ == "__main__":
    main()
