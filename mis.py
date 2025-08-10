from operator import itemgetter
import streamlit as st

# db updated
def update_arrays(pending_array, completed_array):
    st.session_state.task_array = pending_array
    st.session_state.task_completed = completed_array
def completed_array():
    if "task_completed" not in st.session_state:
        st.session_state.task_completed = []
    return st.session_state.task_completed
def add_completed(index, task):
    if index < len(array_task()):
        remove_task(index)  
        completed_array().append(task)

def array_task():
    if "task_array" not in st.session_state:
        st.session_state.task_array = []
    return st.session_state.task_array
def add_task(task):
    array_task().append(task)
    
def add_task_back(index, task):
    if index < len(completed_array()):
        completed_array().pop(index)
        array_task().append(task)
def remove_task(index):
    array_task().pop(index)
def sort_array(array):
    index_data = list(enumerate(array))
    # print(index_data)
    newarrya = sorted(index_data, key=lambda x: itemgetter("datetime")(x[1]),reverse=True)
    # print("sorted array", newarrya)
    return newarrya
def filter_by_date(array, date):
    # print("date", date, array)
    return [task for task in array if task[1]['date'] == date]