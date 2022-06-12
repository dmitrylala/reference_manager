import streamlit as st

from model import ReferenceCreator
from utils import FontStyler, Font


HEADER = "Reference Manager"
REFERENCE_TYPE_INVITE = "Выберите тип ссылки"
REFERENCE_INVITE = "Выберите вид ссылки"

HEADER_STYLER = FontStyler(Font(
    style="italic",
    family="Georgia",
    size=50,
    color="#5C3317")
)
REFERENCE_STYLER = FontStyler(Font(size=20, color="black"))


def main():
    st.markdown(HEADER_STYLER.apply(HEADER), unsafe_allow_html=True)
    st.sidebar.markdown(f"# {HEADER} 🎈")

    ref_type = st.selectbox(
        REFERENCE_TYPE_INVITE,
        ReferenceCreator.reference_types
    )

    creator = ReferenceCreator(
        ref_type=ref_type,
        text_handler=st.text_input,
        number_handler=st.number_input,
        date_handler=st.date_input,
        ref_styler=REFERENCE_STYLER
    )

    option = st.selectbox(REFERENCE_INVITE, creator.ref_names)

    st.markdown("""---""")

    try:
        st.markdown(creator.process(option), unsafe_allow_html=True)
    except TypeError as e:
        st.error(e)
    except ValueError as e:
        st.error(e)


if __name__ == "__main__":
    main()
