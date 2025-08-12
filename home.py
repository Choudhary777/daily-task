from functools import partial
import json
import streamlit as st
from datetime import datetime, timedelta, date
import mis as mi
import db as dbu
# dbu.drop_table()
#daily-task
dbu.create_table()
def on_checkbox_change(index, task):
    newtask = (index, task)
    check = mi.add_completed(index, task)
    if check == True:
        save_db_data()
    # print("Main_array", mi.array_task(), "Completed_array", mi.completed_array())
def on_checkbox_change_re(index, task):
    # print("task", task)
    datetime_ = datetime.now()
    date_ = datetime_.strftime("%d-%m-%Y")
    if "datetime" in task:
        task["datetime"] = datetime_
    if "date" in task:
        task["date"] = date_
    # print("task", task)
    check = mi.add_task_back(index, task)
    if check == True:
        save_db_data()
    # print("Main_array", mi.array_task(), "Completed_array", mi.completed_array())
    # st.rerun()

def onchange(args):
    if args in st.session_state:
        value = st.session_state[args]
        if value !="":
            value = value.replace(" ","")
            st.session_state[args] = value
def onchangepass(args):
    if args in st.session_state:
        value = st.session_state[args]
        if value !="":
            if " " in value:
                st.session_state[args] = ""
def convert_dates(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    return obj
def save_db_data():
    json_data_ = json.dumps(mi.array_task(),default=convert_dates, indent=2)
    json_data_2 = json.dumps(mi.completed_array(),default=convert_dates, indent=2)
    dbu.insert_user_data(st.session_state.current_user, json_data_, json_data_2)
# Helper function to try parsing ISO date/datetime
def try_parse_iso(value):
    try:
        # Try full datetime first
        return datetime.fromisoformat(value)
    except Exception as e:
        # print("value", e)
        return value
# Recursive conversion function for nested JSON
def convert_iso_dates(obj):
    if isinstance(obj, dict):
        return {k: convert_iso_dates(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_iso_dates(i) for i in obj]
    elif isinstance(obj, str):
        parsed = try_parse_iso(obj)
        return parsed if isinstance(parsed, datetime) else parsed
    else:
        return obj
def get_db_data():
    data = dbu.get_user_data(st.session_state.current_user)
    # print("data", data, st.session_state.current_user)
    if data != None:
        values = json.loads(data[0])
        converted_pening = convert_iso_dates(values)
        values = json.loads(data[1])
        converted_completed = convert_iso_dates(values)
        mi.update_arrays(converted_pening, converted_completed)
def change_text(args):
        if args in st.session_state:
            value = st.session_state[args]
            print("value", value)
            if value.endswith("\n\n"):
                value = value.replace("\n\n","\n")
                st.session_state[args] = value

def home():
    if "counter" not in st.session_state:
        st.session_state.counter = 0
    if "isadded" not in st.session_state:
        st.session_state.isadded = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = ""
    if st.session_state.current_user != "":
        with st.container(horizontal=True, vertical_alignment="center"):
            st.subheader("Home")
            if st.button("Logout", key="logout", type="tertiary"):
                st.session_state.clear()
                st.rerun()
        with st.expander("**ADD TASK**", expanded=True):
            with st.container():
                col1, col2 = st.columns([2,1], vertical_alignment="center", border=False, gap="small")
                with col1:
                    if st.session_state.isadded == True:
                        # print("session state is TRUE")
                        st.session_state.task = ""
                        st.session_state.isadded = False
                    st.text_area("Enter your name", key="task", placeholder="Enter your task here", label_visibility="collapsed",height=120)
                with col2:
                    if st.button("Submit", icon="🚀",key="submit", use_container_width=True, type="primary"):
                        if "task" in st.session_state and st.session_state.task != "":
                            datetime_ = datetime.now()
                            date_ = datetime_.strftime("%d-%m-%Y")
                            # print("datetime", datetime_)
                            # mi.add_task(st.session_state.task,False, datetime_,date_)
                            task_x = st.session_state.task
                            task_x = task_x.strip()
                            mi.add_task({"task": st.session_state.task, "status": False, "datetime": datetime_, "date": date_})
                            save_db_data()
                            st.session_state.isadded = True
                            st.rerun()
                            # print("array", mi.array_task())
                            # st.rerun()
        with st.container( horizontal=True, vertical_alignment="center"):
                st.markdown("**Filter by date**")
                with st.container(width=150):
                    st.date_input("Date", key="date", label_visibility="collapsed", value=None, format="DD/MM/YYYY", max_value="today")
        with st.expander("**PENDING TASKS**",expanded=True):
            with st.container():
                sortedarray = mi.sort_array(mi.array_task())
                if "date" in st.session_state and st.session_state.date != None:
                    date_ = st.session_state.date.strftime("%d-%m-%Y")
                    sortedarray = mi.filter_by_date(sortedarray, date_)
                if len(sortedarray) == 0:
                    st.markdown("<div style='color:green; padding-bottom:10px'><i>No pending tasks</i></div>", unsafe_allow_html=True)
                for i,task in sortedarray:
                    task_ = task['task']
                    status = task['status']
                    datetime_ = task['datetime']
                    date_ = task['date']
                    taskstatus = "Pending"
                    if status:
                        taskstatus = "Completed"
                    
                    with st.container(border= True):
                        newtask = task_
                        if "\n" in newtask:
                            newtask = newtask.replace("\n","<br>")
                        st.markdown(f'<span style="color:#069C47FF;font-size:17px;">{newtask}</span>', unsafe_allow_html=True)
                        with st.container(horizontal=True, horizontal_alignment="center", vertical_alignment="center", ):
                            st.button(" ", icon="📝", key=f"Edit_{i}", type="tertiary", )
                            st.markdown(f'<span style="color:#0D8B8BFF;font-size:12px;">{date_}</span>', unsafe_allow_html=True)
                            st.markdown(f'<span style="color:orange;font-size:14px;">{taskstatus}</span>', unsafe_allow_html=True)
                            st.session_state[f"Check_{i}"] = False
                            st.checkbox("*Launched*", key=f"Check_{i}",on_change=partial(on_checkbox_change, i, task),)
        with st.expander("**COMPLETED TASKS**",):
            with st.container():
                # print("completed array", mi.completed_array())
                sortedarray = mi.sort_array(mi.completed_array())
                if "date" in st.session_state and st.session_state.date != None:
                    date_ = st.session_state.date.strftime("%d-%m-%Y")
                    sortedarray = mi.filter_by_date(sortedarray, date_)
                if len(sortedarray) > 0:
                    for i,task in sortedarray:
                        # print(i, task)
                        task_ = task['task']
                        datetime_ = task['datetime']
                        date_ = task['date']
                        with st.container( border= True):
                            newtask = task_
                            if "\n" in newtask:
                                newtask = newtask.replace("\n","<br>")
                            st.markdown(f'<span style="color:#069C47FF;font-size:17px;">{newtask}</span>', unsafe_allow_html=True)
                            with st.container(horizontal=True, horizontal_alignment="center", vertical_alignment="center", gap="small"):
                                st.button(" ", icon="🗑️", key=f"deletre_{i}", type="tertiary", )
                                st.markdown(f'<span style="color:#0D8B8BFF;font-size:12px;">{date_}</span>', unsafe_allow_html=True)
                                st.markdown(f'<span style="color:orange;font-size:14px;">Completed</span>', unsafe_allow_html=True)
                                st.session_state[f"Checkre_{i}"] = False
                                st.checkbox("*Re-launch*", key=f"Checkre_{i}",on_change=partial(on_checkbox_change_re, i, task))
                else:
                    st.markdown("<div style='color:green; padding-bottom:10px'><i>No completed tasks</i></div>", unsafe_allow_html=True)
        with st.expander("**DELETED TASKS**",):
            pass
    else:
        st.subheader("Login/Signup")
        with st.container():
            st.text_input("**User Name**", key="user_name", placeholder="Enter user name",on_change=partial(onchange, "user_name"))
            st.text_input("**Password**", key="user_pass", placeholder="Enter password",on_change=partial(onchangepass, "user_pass"), type="password")
        with st.container(horizontal=True, width=400, gap="large"):
            if st.button("Login", key="login", use_container_width=True, type="primary"):
                if "user_name" in st.session_state and "user_pass" in st.session_state:
                    if st.session_state.user_name != "" and st.session_state.user_pass != "":
                        users = dbu.check_user(st.session_state.user_name, st.session_state.user_pass)
                        if users == None:
                            st.toast("**User name or passward is incorrect**", icon="🚨")
                        else:
                            usern = st.session_state.user_name
                            st.session_state.current_user = usern.lower()
                            get_db_data()
                            st.rerun()
                    else:
                        st.toast("**Please enter user name or password**", icon="🚨")
            if st.button("Signup", key="signup", use_container_width=True, type="primary"):
                if "user_name" in st.session_state and "user_pass" in st.session_state:
                    if st.session_state.user_name != "" and st.session_state.user_pass != "" and len(st.session_state.user_pass) >= 4 and len(st.session_state.user_name) >= 4:
                        users = dbu.check_username(st.session_state.user_name)
                        if users == None:
                            dbu.insert_user(st.session_state.user_name, st.session_state.user_pass)
                            st.toast("**User created successfully**", icon="✅")
                        else:
                            st.toast("**User already exists**", icon="🚨")
                    else:
                        st.toast("**Please enter user name or password (length should minimum 4)**", icon="🚨")
home()