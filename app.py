# Import python packages
import streamlit as st

# ======= BEGIN VANNA SETUP =======

from vanna.remote import VannaDefault

vanna_model_name=st.secrets.vanna.vanna_model_name
vanna_api_key = st.secrets.vanna.vanna_api_key
vn = VannaDefault(model=vanna_model_name, api_key=vanna_api_key)

# vn.connect_to...(YOUR_DATABASE_CREDENTIALS)
# example using suprabase
supra_host=st.secrets.supra.supra_host
supra_user=st.secrets.supra.supra_user
supra_password=st.secrets.supra.supra_password

vn.connect_to_postgres(host=supra_host, dbname='postgres', user=supra_user, password=supra_password, port=5432)

# ======= END VANNA SETUP =======

my_question = st.session_state.get("my_question", default=None)

if my_question is None:
    my_question = st.text_input(
        "Ask me a question about your data",
        key="my_question",
    )
else:
    st.text(my_question)
    
    sql = vn.generate_sql(my_question)

    st.text(sql)

    df = vn.run_sql(sql)    
        
    st.dataframe(df, use_container_width=True)

    code = vn.generate_plotly_code(question=my_question, sql=sql, df=df)

    fig = vn.get_plotly_figure(plotly_code=code, df=df)

    st.plotly_chart(fig, use_container_width=True)
