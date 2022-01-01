from functools import reduce

import streamlit as st

'''streamlit'''

if 'pipeline' not in st.session_state:
    pipeline = st.session_state.pipeline = [1]
else:
    pipeline = st.session_state.pipeline
print(pipeline)


def display(pipeline_item):
    container = st.empty()
    container.text(pipeline_item)


def calc(pipeline):
    c = reduce(lambda x, y: x * y, pipeline)
    st.metric("Result:", c)


for item in pipeline:
    display(item)

new = st.empty()
add_new = new.button('+')
if add_new:
    with st.form(key='new'):
        added = st.container()
        x = st.slider("Prob:", 0.0, 1.0)
        st.form_submit_button("Done", on_click=pipeline.append, args=(float(x),))
            #pipeline.append(float(x))
            #display(x)


'''-----------------------------'''

calc(pipeline)
