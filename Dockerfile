FROM python:3.9

RUN pip install streamlit tensorflow tensorflow-probability seaborn

ADD . /code
WORKDIR /code
VOLUME /code
EXPOSE 8501

ENTRYPOINT streamlit run /code/main.py
