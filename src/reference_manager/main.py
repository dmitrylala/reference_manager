import streamlit as st

from font_styler import FontStyler, Font
from model.references import ReferenceCreator

HEADER = "Reference Manager"
REFERENCE_TYPE_INVITE = "Выберите тип ссылки"
REFERENCE_INVITE = "Выберите вид ссылки"


def main():
    header_styler = FontStyler(Font(
        style="italic",
        family="Georgia",
        size=50,
        color="#5C3317")
    )
    reference_styler = FontStyler(Font(size=20, color="black"))

    st.markdown(
        header_styler.apply(HEADER),
        unsafe_allow_html=True
    )

    ref_type = st.selectbox(
        REFERENCE_TYPE_INVITE,
        ReferenceCreator.reference_types,
        format_func=str.strip
    )

    creator = ReferenceCreator(
        ref_type=ref_type,
        text_handler=st.text_input,
        number_handler=st.number_input,
        date_handler=st.date_input,
        ref_styler=reference_styler
    )

    option = st.selectbox(REFERENCE_INVITE, creator.ref_names)

    st.markdown("""---""")

    try:
        st.markdown(creator.process(option), unsafe_allow_html=True)
    except TypeError as e:
        st.error(e)
    except ValueError as e:
        st.error(e)


if __name__ == '__main__':
    main()
