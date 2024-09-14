import streamlit as st
from streamlit_pdf_viewer import pdf_viewer



def main():
    
    st.set_page_config(layout="centered")

    with st.sidebar:
        st.header("About")
        st.write("""
            My Name is Nitesh Sharma and This is my Intership project under ineuron Intership.
            ***
            github :- https://github.com/nitesh29ns/
                
            linkdin :- https://www.linkedin.com/in/nitesh-sharma-0a260b183/
            """)

    with st.container():

        html_temp = """
        <div style="background-color:tomato;padding:5px">
        <h2 style="color:white;text-align:center;"> Talk to PDF </h2>
        </div>
        """

        st.markdown(html_temp,unsafe_allow_html=True)

        html_write_temp="""
        <div>
        <h1 style="font-size: 25px"> You have to upload an pdf and any thing with in the context of this pdf.</h1>
        </div>

        """

        st.write(html_write_temp, unsafe_allow_html=True)

       

        pdf_file = st.file_uploader("upload PDF file", type="pdf")

        print(pdf_file)

        with st.expander("view pdf"):
            if pdf_file:
                binary_data = pdf_file.getvalue()
                pdf_viewer(input=binary_data,
                            width=700)
            

    query = st.text_input("query")
        
    if st.button("Ask"):
        print(query)


        
    


if __name__ == "__main__":
    main()