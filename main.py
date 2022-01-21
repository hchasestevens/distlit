import time
from functools import reduce, partial
from threading import Thread

import streamlit as st
import seaborn as sns
import tensorflow_probability as tfp
from matplotlib import pyplot as pl

'''streamlit'''

if 'pipeline' not in st.session_state:
    pipeline = st.session_state.pipeline = []
else:
    pipeline = st.session_state.pipeline
print(pipeline)

if 'add_new_state' not in st.session_state:
    add_new_state = st.session_state.add_new_state = False
else:
    add_new_state = st.session_state.add_new_state


FIGSIZE = (5, 2)


def display(pipeline_item, elem):
    fig = pl.figure(figsize=FIGSIZE)
    sample = disp_sample(*pipeline_item)
    sns.distplot(sample)
    elem.pyplot(fig)


def calc(pipeline):
    if not pipeline:
        st.text("click +!")
        return

    # method 1 - joint dist
    sample = dist_joint(pipeline)
    fig = pl.figure(figsize=FIGSIZE)
    #st.metric("Result:", str(pipeline))
    sns.distplot(sample)
    st.text('joint')
    st.pyplot(fig)

    # method 2 - multiplying
    fig = pl.figure(figsize=FIGSIZE)
    sample = dist_mult(pipeline)
    sns.distplot(sample)
    st.text('mult')
    st.pyplot(fig)


@st.cache
def dist_mult(pipeline):
    starts, ends = zip(*pipeline)
    dist = tfp.distributions.Uniform(low=starts, high=ends)
    sample = dist.sample(10000)
    return sample.numpy().prod(axis=1)


@st.cache
def dist_joint(pipeline):
    (first_start, first_end), *rest = pipeline
    dist = tfp.distributions.JointDistributionSequential(
        [tfp.distributions.Uniform(low=first_start, high=first_end)] + [
            lambda x: tfp.distributions.Uniform(low=low * x, high=high * x)
            for low, high in rest
        ]
    )
    *_, sample = dist.sample(25000)
    return sample


@st.cache
def disp_sample(start, end):
    dist = tfp.distributions.Uniform(low=start, high=end)
    sample = dist.sample(20000)
    return sample


for i, item in enumerate(pipeline, start=1):
    container = st.container()
    col1, col2, *_ = container.columns([1, 1, 4])
    col1.text(item)
    col2.button('-', on_click=partial(st.session_state.pipeline.pop, i - 1), key=f'remove-{i}')
    col1, col2 = container.columns(2)
    display(item, col1)

    fig = pl.figure(figsize=FIGSIZE)
    sample = dist_joint(pipeline[:i])
    sns.distplot(sample, label='joint')  # this looks wrong! 0.1-1 * 0.1-1 * 10-100 e.g. # actually, always happens at 3rd instance? maybe lambda isn't working the same way I want, doesn't take n-1 but instead binds by arg name?
    sample = dist_mult(pipeline[:i])
    sns.distplot(sample, label='mult')
    col2.pyplot(fig)


def stop_add_new_state_and_commit(pipeline_item):
    st.session_state.pipeline.append(pipeline_item)
    st.session_state.add_new_state = False


def enable_add_new_state():
    st.session_state.add_new_state = True


if not add_new_state:
    new = st.empty()
    add_new = new.button('+', on_click=enable_add_new_state)
else:
    added = st.container()
    added.text("Uniform distribution:")
    plot = added.empty()
    start = added.number_input("Start:", key='start')
    end = added.number_input("End:", key='end')

    display((start, end), plot)

    added.button(
        "Done",
        on_click=lambda: stop_add_new_state_and_commit((st.session_state.start, st.session_state.end))
    )



'''-----------------------------'''

st.text(pipeline)
calc(pipeline)
