from curses.ascii import isdigit
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.db import connections
import re
import requests
import time

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
# from ..db.urls import INTERGER


import datetime
from datetime import date

from .models import *

postrecomm_list = []
postrecomm_list = []
postrecomm_pie = [0, 0, 0]
postrecomm_sum = []

deployment_date_table = {
    "6092021": ["2021-06-09 00:00:00", "2021-11-13 11:59:59"],
    "7132021": ["2021-07-13 00:00:00", "2021-12-03 11:59:59"],
    "8022021": ["2021-08-02 00:00:00", "2021-12-07 11:59:59"],
    "10282021": ["2021-10-28 00:00:00", ""],
    "1172022": ["2022-01-17 00:00:00", ""],
    "2182022": ["2022-02-18 00:00:00", ""],
    "3162022": ["2022-03-16 00:00:00", ""],
    "5062022": ["2022-05-06 00:00:00", ""],
    "5122022": ["2022-05-12 00:00:00", ""],
    "8122022": ["2022-08-12 00:00:00", ""],
    "9152022": ["2022-09-15 00:00:00", ""],
    "9212022": ["2022-09-21 00:00:00", ""],
    "11192022": ["2022-11-09 00:00:00", ""],
    "1182023": ["2023-01-18 00:00:00", ""],
    "5112023": ["2023-05-11 00:00:00", ""],
}

monitor_date_table = {
    "6092021": ["2021-06-09 00:00:00", "2021-11-13 11:59:59"],
    "7132021": ["2021-07-13 00:00:00", "2021-12-03 11:59:59"],
    "8022021": ["2021-08-02 00:00:00", "2021-12-07 11:59:59"],
    "1172022": ["2022-01-17 00:00:00", ""],
    "2182022": ["2022-02-18 00:00:00", ""],
    "3162022": ["2022-03-16 00:00:00", ""],
    "5122022": ["2022-05-12 00:00:00", ""],
    "8122022": ["2022-08-12 00:00:00", ""],
    "9152022": ["2022-09-15 00:00:00", ""],
    "9212022": ["2022-09-21 00:00:00", ""],
    "11192022": ["2022-11-09 00:00:00", ""],
    "1182023": ["2023-01-18 00:00:00", ""],
    "5112023": ["2023-05-11 00:00:00", ""],
}

action_lookup_table = [
    "Time to take a brief break.",
    "Take a quick moment for yourself.",
    "Take some time to “put on your oxygen mask.",
    "Step away for a moment.",
    "It seems like this could be a good time to take a time-out.",
    "Feel free to step away if you need to collect your thoughts.",
    "Feel free to step away if you need to settle yourself.",
    "It seems like you could use some uninterrupted personal time,<br>"
    " can you engage your family member in an activity that they <br>"
    "enjoy?",
    "Engage [insert name] in an engaging activity and give yourself <br>"
    "a few moments of personal time?]",
    "Try some breathing exercises on your mindfulness training app.",
    "Now is a good time to perform a breathing meditation using the <br>"
    "mindfulness app or one of these recordings.(provide list of guided <br>"
    "breathing audio)",
    "Now is a good time to perform a breathing exercise.Please use a <br>"
    "guided breathing from either the mindfulness app or the list provided <br>"
    "below.(provide list of guided breathing audio)",
    "Open your mindfulness training app or listen to one these recordings <br>"
    "and perform a body scan meditation.(provide list of body scan audio)",
    "Perform a body scan using your mindfulness training app or the guided <br>"
    "body scan meditation provided. (provide list of body scan audio)",
    "You know [your family member] best, what’s an activity that [he/she] has <br>"
    "always enjoyed?-included in caregiver training.",
    "Are you able to set up an activity for your family member now?",
    "Now might be a good time to start an activity with/for your family member.",
    "You and your family member may benefit from engaging in an activity that you <br>"
    "both enjoy.",
    "Now might be a good time to do something you and [your family member/insert name] <br>"
    "love doing together.",
    "Can you start an activity with/for [your family member/insert name] that would<br>"
    " make you both feel calmer?",
    "Trying engaging [your family member/insert name] in an activity or task that<br>"
    "provides them with a sense of ease.",
    "Grab your activity box",
    "Now might be a good time to [Load Dynamic Activities]"
]

def ownership(request):
    return render(request, 'google4809d73a899ef81d.html')

# add a new function for tracing the data of a specific dep from the data button displayed in our home page(tracking)
def tracking_dept(request, dept_id):
    # # start time tracking
    # print("start", time.perf_counter())
    # tracking_list = []
    # cursor = connections['ema'].cursor()
    # # adding a dept_list in order to display the side bar containing each avaliable date button that we can click on to load its corresponding data
    # dept_list = []

    # # time around 1s
    # if(request.session['dept_list']):
    #     dept_list = request.session['dept_list']
    # else:
    #     cursor.execute(
    #         "SELECT DISTINCT dep_id FROM `sch_data`.`ema_storing_data` WHERE dep_id NOT regexp \"^-1$|^200$|^999$|^6232021$|^10$|^11111$|^11112$\"")
    #     dep_id = cursor.fetchall()
    #     for id in dep_id:
    #         if id[0] in monitor_date_table:
    #             dept_list.append(id[0])
    # # time around 1s
    # print("p1", time.perf_counter())

    # # just get the specific dep we want rather than all of them
    # cursor.execute(
    #     "SELECT DISTINCT dep_id FROM `sch_data`.`ema_storing_data` WHERE dep_id NOT regexp \"^-1$|^200$|^999$|^6232021$|^10$|^11111$|^11112$\" AND dep_id = (%s)", dept_id)
    # dep_id = cursor.fetchall()
    # #dep_id = (('8022021',),)
    # print("p2", time.perf_counter())

    # # just one item in dep_id
    # for id in dep_id:
    #     # Only retrieve data of the dep_id we want to monitor (this can reduce some loading time)
    #     if id[0] not in monitor_date_table:
    #         continue

    #     if id[0] in deployment_date_table:
    #         date = deployment_date_table[id[0]]
    #         if date[1] != "":
    #             emo_var_SQL = "SELECT time, event_vct FROM `sch_data`.`ema_storing_data` WHERE time between\"" + date[0] + "\" AND \""+ date[1]+"\" AND dep_id = (%s) ORDER BY time"
    #         elif date[1] == "":
    #             emo_var_SQL = "SELECT time, event_vct FROM `sch_data`.`ema_storing_data` WHERE time >\"" + date[0] + "\" AND dep_id = (%s) ORDER BY time"
    #         else:
    #             emo_var_SQL = "SELECT time, event_vct FROM `sch_data`.`ema_storing_data` WHERE time > \"2021-06-01 00:00:00\" AND dep_id = (%s) ORDER BY time"
    #     else:
    #         emo_var_SQL = "SELECT time, event_vct FROM `sch_data`.`ema_storing_data` WHERE time > \"2021-06-01 00:00:00\" AND dep_id = (%s) ORDER BY time"
    #         date = monitor_date_table[id[0]]

    #     cursor.execute(emo_var_SQL, id)
    #     emo_var = cursor.fetchall()
    #     print("p3",time.perf_counter())

    #     # around 2s
    #     # baseline
    #     cursor.execute(
    #         "SELECT TimeReceived, Response FROM `sch_data`.reward_data where QuestionName REGEXP \"baseline:recomm:likertconfirm:1\" AND Response !=\"-1.0\" AND Response !=\"-1\" AND dep_id = (%s) ORDER BY TimeReceived",
    #         id[0])
    #     baseline_db = cursor.fetchall()
    #     baseline_list = []
    #     baseline_timestamp = []
    #     baseline_response = []
    #     for item in baseline_db:
    #         baseline_timestamp.append(item[0])
    #         baseline_response.append(int(item[1]))
    #     baseline_list.append(baseline_timestamp)
    #     baseline_list.append(baseline_response)
    #     #print(baseline_list)
    #     # around 2s
    #     print("p4",time.perf_counter())

    #     # emotion
    #     if date[1] != "":
    #         start_date = datetime.datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S")
    #     elif date[1] == "":
    #         start_date = datetime.datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S")
    #     else:
    #         start_date = emo_var[0][0].replace(minute=0, second=0, microsecond=0)

    #     intervention_period = start_date + datetime.timedelta(days=30)

    #     intervention_period_counter = [0, 0, 0, 0, 0, 0]
    #     baseline_period_counter = [0, 0, 0, 0, 0, 0]
    #     total_emotion_counter = [0, 0, 0, 0, 0, 0]
    #     counted_period = [0, 0, 0, 0, 0, 0]

    #     emotion_steps = [[],[],[],[],[],[],[]]
    #     counter = 0
    #     counting_step = datetime.timedelta(hours=1)

    #     def intervention_period_helper(index):
    #         if item[0] > intervention_period:
    #             intervention_period_counter[index] += 1
    #         else:
    #             baseline_period_counter[index] += 1
    #         total_emotion_counter[index] += 1
    #         counted_period[index] += 1

    #     def emo_counter_helper(counted,time):
    #         for index in range(len(emotion_steps)):
    #             if index == 0:
    #                 emotion_steps[0].append(time)
    #             else:
    #                 emotion_steps[index].append(counted[index-1])


    #     for item in emo_var:
    #         # period close
    #         while item[0] > start_date:
    #             emo_counter_helper(counted_period, start_date.strftime("%Y-%m-%d %H:%M:%S"))
    #             counted_period = [0, 0, 0, 0, 0, 0]
    #             start_date = start_date + counting_step

    #         temp = json.loads(item[1])
    #         element = temp.index(max(temp[0:4]))
    #         if len(temp) == 6 and temp[5] > 0.525:
    #             intervention_period_helper(5)
    #         if temp[0] == temp[1] == temp[2] == temp[3] == temp[4] == 0:
    #             continue
    #         else:
    #             intervention_period_helper(element)
    #         counter += 1

    #         # ensure the last one added
    #         if counter == len(emo_var) and counted_period != [0, 0, 0, 0, 0, 0]:
    #             emo_counter_helper(counted_period, start_date.strftime("%Y-%m-%d %H:%M:%S"))
    #     print("p5",time.perf_counter())

    #     emotion_counter = [baseline_period_counter, intervention_period_counter, total_emotion_counter]

    #     # action
    #     cursor.execute(
    #         "SELECT time, action FROM `sch_data`.`ema_storing_data` WHERE time > \"2021-03-01 00:00:00\" AND dep_id = (%s) ORDER BY time",
    #         id)
    #     act_var = cursor.fetchall()
    #     print("p6",time.perf_counter())


    #     nothing = action_helper(-2, -1, act_var, 0)
    #     timeout = action_helper(0, 8, act_var, 1)
    #     breathing = action_helper(9, 11, act_var, 2)
    #     bodyscan = action_helper(12, 13, act_var, 3)
    #     activities = action_helper(14, 21, act_var, 4)
    #     act_list = [nothing, timeout, breathing, bodyscan, activities]

    #     # post recommendation
    #     cursor.execute(
    #         "SELECT DISTINCT TimeSent, TimeReceived,Response,Question,QuestionName FROM "
    #         "`sch_data`.reward_data where QuestionName REGEXP "
    #         "\"daytime:postrecomm:helpfulno:1|daytime:postrecomm:helpfulyes:1|daytime:recomm:|daytime"
    #         ":postrecomm:implement:\" AND dep_id = (%s) ORDER BY TimeSent",
    #         id)
    #     postrecomm_db = cursor.fetchall()
    #     print("p7",time.perf_counter())

    #     postrecomm_list = []
    #     postrecomm_yes_timestamp = []
    #     postrecomm_no_timestamp = []
    #     postrecomm_yes = []
    #     postrecomm_no = []
    #     postrecomm_yes_text = []
    #     postrecomm_no_text = []
    #     postrecomm_pie = [0, 0, 0]
    #     now = datetime.datetime.now()

    #     if (len(postrecomm_db)):
    #         postrecomm_sum = [[0], [str(postrecomm_db[0][0])], [0], [str(postrecomm_db[0][0])], [0],
    #                           [str(postrecomm_db[0][0])]]
    #     else:
    #         postrecomm_sum = [[0], [now.strftime("%Y-%m-%d %H:%M:%S")], [0], [now.strftime("%Y-%m-%d %H:%M:%S")], [0],
    #                           [now.strftime("%Y-%m-%d %H:%M:%S")]]

    #     action_ID = ""

    #     print("development id: {}, number of items: {}".format(id, len(postrecomm_db)))

    #     for item in postrecomm_db:
    #         # while not action_for_response:
    #         #     cursor.execute(
    #         #         "SELECT DISTINCT time, action FROM `sch_data`.`ema_storing_data` WHERE \"" + lower_bound.strftime(
    #         #             "%Y-%m-%d %H:%M:%S") + "\"< time and time <\"" + upper_bound.strftime(
    #         #             "%Y-%m-%d %H:%M:%S") + "\" AND dep_id = (%s) ORDER BY time",
    #         #         id)
    #         #     upper_bound = upper_bound + datetime.timedelta(0, 10)
    #         #     lower_bound = lower_bound - datetime.timedelta(0, 10)
    #         #     action_for_response = cursor.fetchall()

    #         if "daytime:recomm:" in item[4]:
    #             if "timeout" in item[4]:
    #                 action_ID = -1 + int(item[4][-1])   # this action_id mapping changed from 0+int(*) to -1+int(*), since timeout starts from action 0
    #             elif "breathing" in item[4]:
    #                 action_ID = 8 + int(item[4][-1])
    #             elif "bodyscan" in item[4]:
    #                 action_ID = 11 + int(item[4][-1])
    #             elif "enjoyable" in item[4]:
    #                 action_ID = 13 + int(item[4][-1])

    #         # elif ":postrecomm:implement:" in item[4]:
    #         #     if action_ID != "":
    #         #         if last_move == "posted" and item[2] != "-1.0":
    #         #             last_move = "responded"

    #         elif item[4] == "daytime:postrecomm:helpfulyes:1" and item[2] != "-1.0":
    #             if action_ID == "":
    #                 print("---"*10+"Error"+"---"*10)
    #                 print("deployment id: {}".format(id))
    #                 print("item: ", item)
    #                 print("---"*10+"End"+"---"*10)
    #                 continue
    #             else:
    #                 postrecomm_yes.append(int(item[2]))
    #                 postrecomm_yes_timestamp.append(str(item[0]))
    #                 postrecomm_yes_text.append(
    #                     str(item[0]) + "<br>Action:" + str(action_ID) +
    #                     "<br>" + action_lookup_table[int(action_ID)])

    #         elif item[4] == "daytime:postrecomm:helpfulno:1" and item[2] != "-1.0":
    #             bar_data = ""
    #             if "1" in list(item[2]):
    #                 bar_data += " I didn’t have enough time <br>" + str(item[0]) + "<br>Action:" + str(
    #                     action_ID) + "<br>" + action_lookup_table[action_ID]
    #                 postrecomm_pie[0] += 1
    #                 postrecomm_sum[0].append(postrecomm_pie[0])
    #                 postrecomm_sum[1].append(str(item[0]))

    #             if "2" in list(item[2]):
    #                 bar_data += " I didn’t think it would help <br>" + str(item[0]) + "<br>Action:" + str(
    #                     action_ID) + "<br>" + action_lookup_table[action_ID]
    #                 postrecomm_pie[1] += 1
    #                 postrecomm_sum[2].append(postrecomm_pie[1])
    #                 postrecomm_sum[3].append(str(item[0]))

    #             if "3" in list(item[2]):
    #                 bar_data += " I didn’t see the message <br>" + str(item[0]) + "<br>Action:" + str(
    #                     action_ID) + "<br>" + action_lookup_table[action_ID]
    #                 postrecomm_pie[2] += 1
    #                 postrecomm_sum[4].append(postrecomm_pie[2])
    #                 postrecomm_sum[5].append(str(item[0]))

    #             postrecomm_no_text.append(bar_data)
    #             postrecomm_no.append(-1)
    #             postrecomm_no_timestamp.append(str(item[0]))

    #         elif (item[4] == "daytime:postrecomm:helpfulno:1" or item[4] == "daytime:postrecomm:helpfulno:1") and item[2] == "-1.0":
    #             if action_ID:
    #                 postrecomm_yes.append(0)
    #                 postrecomm_yes_timestamp.append(str(item[0]))
    #                 postrecomm_yes_text.append(
    #                     str(item[0]) + "<br>Action:" + str(action_ID) +
    #                     "<br>" + action_lookup_table[int(action_ID)] + "(No user feed back on post recommendation)")

    #     print("p8",time.perf_counter())

    #     postrecomm_list.append(postrecomm_yes_timestamp)
    #     postrecomm_list.append(postrecomm_no_timestamp)
    #     postrecomm_list.append(postrecomm_yes)
    #     postrecomm_list.append(postrecomm_no)
    #     postrecomm_list.append(postrecomm_yes_text)
    #     postrecomm_list.append(postrecomm_no_text)

    #     postrecomm_sum[0].append(postrecomm_sum[0][-1])
    #     postrecomm_sum[1].append(now.strftime("%Y-%m-%d %H:%M:%S"))
    #     postrecomm_sum[2].append(postrecomm_sum[2][-1])
    #     postrecomm_sum[3].append(now.strftime("%Y-%m-%d %H:%M:%S"))
    #     postrecomm_sum[4].append(postrecomm_sum[4][-1])
    #     postrecomm_sum[5].append(now.strftime("%Y-%m-%d %H:%M:%S"))

    #     tracking_list.append(
    #         [id[0], emotion_steps[0], emotion_steps[1], emotion_steps[2], emotion_steps[3], emotion_steps[4], emotion_steps[5], emotion_steps[6], act_list, baseline_list,
    #          postrecomm_list, postrecomm_pie, postrecomm_sum, emotion_counter]
    #     )
        
    #     print("p9",time.perf_counter())
    

    # # e_0=emotion_steps[0]
    # # e_1=emotion_steps[1]
    # # e_2=emotion_steps[2]
    # # e_3=emotion_steps[3]
    # # e_4=emotion_steps[4]
    # # e_5=emotion_steps[5]
    # # e_6=emotion_steps[6]
    # e_0=[]
    # e_1=[]
    # e_2=[]
    # e_3=[]
    # e_4=[]
    # e_5=[]
    # e_6=[]
    # return render(request, 'tracking.html', {'tracking': tracking_list, 'dept_list': dept_list, 'e_0':e_0, 'e_1':e_1, 'e_2':e_2, 'e_3':e_3, 'e_4':e_4, 'e_5':e_5, 'e_6':e_6})

    # this line of code is used to control the default tab displayed
    return redirect("/dataviewer/tracking/" + str(dept_id) + "/stress_level/")

# check if the user email is authorized to view the data
def email_check(user):
    print("checked!")
    allowed_emails = settings.ALLOWED_EMAILS
    if user.is_anonymous:
        return False
    elif user.email in allowed_emails:
        return True
    else:
        return False

# used to track each tab. Parameter: dep_id and tab name. Return: the corresponding dep_id and tab page
def tracking_dept_tab(request, dept_id, tab):

    # check if user login before accessing the page
    if(not request.user.is_authenticated):
        print("please login!")
        return redirect("/accounts/google/login/")
    print("google account logged in!")
    # if google account is not authorized, back to login page and logout from google account
    if (not email_check(request.user)):
        messages.error(request, 'Sorry. You do not have access to the data.')
        print("account does not access!")
        return redirect("/dataviewer/tracking")

    cursor = connections['ema'].cursor()
    # adding a dept_list in order to display the side bar containing each avaliable date button that we can click on to load its corresponding data
    dept_list = []

    # time around 1s
    if('dept_list' in request.session):
        dept_list = request.session['dept_list']
    else:
        cursor.execute(
            "SELECT DISTINCT dep_id FROM `sch_data`.`ema_storing_data` WHERE dep_id NOT regexp \"^-1$|^200$|^999$|^6232021$|^10$|^11111$|^11112$\"")
        dep_id = cursor.fetchall()
        for id in dep_id:
            if id[0] in monitor_date_table:
                dept_list.append(id[0])
        request.session['dept_list'] = dept_list

    # deal with emotion_steps and emotion_table at the same time
    if(tab=="emotion_table" or tab=="emotion"):
        # print("loading", tab)
        # print("start", time.perf_counter())

        # # just get the specific dep we want rather than all of them
        # cursor.execute(
        #     "SELECT DISTINCT dep_id FROM `sch_data`.`ema_storing_data` WHERE dep_id NOT regexp \"^-1$|^200$|^999$|^6232021$|^10$|^11111$|^11112$\" AND dep_id = (%s)", dept_id)
        # dep_id = cursor.fetchall()
    
        # # just one item in dep_id
        # for id in dep_id:
        #     # Only retrieve data of the dep_id we want to monitor (this can reduce some loading time)
        #     if id[0] not in monitor_date_table:
        #         continue

        #     if id[0] in deployment_date_table:
        #         date = deployment_date_table[id[0]]
        #         if date[1] != "":
        #             emo_var_SQL = "SELECT time, event_vct FROM `sch_data`.`ema_storing_data` WHERE time between\"" + date[0] + "\" AND \""+ date[1]+"\" AND dep_id = (%s) ORDER BY time"
        #         elif date[1] == "":
        #             emo_var_SQL = "SELECT time, event_vct FROM `sch_data`.`ema_storing_data` WHERE time >\"" + date[0] + "\" AND dep_id = (%s) ORDER BY time"
        #         else:
        #             emo_var_SQL = "SELECT time, event_vct FROM `sch_data`.`ema_storing_data` WHERE time > \"2021-06-01 00:00:00\" AND dep_id = (%s) ORDER BY time"
        #     else:
        #         emo_var_SQL = "SELECT time, event_vct FROM `sch_data`.`ema_storing_data` WHERE time > \"2021-06-01 00:00:00\" AND dep_id = (%s) ORDER BY time"
        #         date = monitor_date_table[id[0]]

        #     cursor.execute(emo_var_SQL, id)
        #     emo_var = cursor.fetchall()

        #     #emotion
        #     if date[1] != "":
        #         start_date = datetime.datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S")
        #     elif date[1] == "":
        #         start_date = datetime.datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S")
        #     else:
        #         start_date = emo_var[0][0].replace(minute=0, second=0, microsecond=0)

        #     intervention_period = start_date + datetime.timedelta(days=30)
        #     # print("startdate",start_date)
        #     # print("intev",intervention_period)

        #     intervention_period_counter = [0, 0, 0, 0, 0, 0]
        #     baseline_period_counter = [0, 0, 0, 0, 0, 0]
        #     total_emotion_counter = [0, 0, 0, 0, 0, 0]
        #     counted_period = [0, 0, 0, 0, 0, 0]

        #     emotion_steps = [[],[],[],[],[],[],[]]
        #     counter = 0
        #     counting_step = datetime.timedelta(hours=1)

        #     def intervention_period_helper(index):
        #         if item[0] > intervention_period:
        #             intervention_period_counter[index] += 1
        #         else:
        #             baseline_period_counter[index] += 1
        #         total_emotion_counter[index] += 1
        #         counted_period[index] += 1

        #     def emo_counter_helper(counted,time):
        #         # as long as there is one emotion that is not counted as 0, we record this day
        #         record=False
        #         for i in range(6):
        #             if(counted[i])!=0:
        #                 record=True
        #         if (record):
        #             for index in range(len(emotion_steps)):
        #                 if index == 0:
        #                     emotion_steps[0].append(time)
        #                 else:
        #                     emotion_steps[index].append(counted[index-1])
                                
        #     for item in emo_var:
                
        #         # period close
        #         while item[0] > start_date:
        #             emo_counter_helper(counted_period, start_date.strftime("%Y-%m-%d %H:%M:%S"))
        #             counted_period = [0, 0, 0, 0, 0, 0]
        #             start_date = start_date + counting_step

        #         temp = json.loads(item[1])
        #         element = temp.index(max(temp[0:4]))
        #         if len(temp) == 6 and temp[5] > 0.525:
        #             intervention_period_helper(5)
        #         if temp[0] == temp[1] == temp[2] == temp[3] == temp[4] == 0:
        #             continue
        #         else:
        #             intervention_period_helper(element)
        #         counter += 1

        #         # ensure the last one added
        #         if counter == len(emo_var) and counted_period != [0, 0, 0, 0, 0, 0]:
        #             emo_counter_helper(counted_period, start_date.strftime("%Y-%m-%d %H:%M:%S"))

        #     # print(emotion_steps[1])
        #     # print(emotion_steps[2])
        #     # print(emotion_steps[3])
        #     # print(emotion_steps[4])
        #     # print(emotion_steps[5])
        #     # print(emotion_steps[6])

        # emotion_counter = [baseline_period_counter, intervention_period_counter, total_emotion_counter]

        emotion_steps=request.session['emotion_steps']
        emotion_counter=request.session['emotion_counter']

        print("end", time.perf_counter())
        if(tab == "emotion"):
            # the latest time stamp in our dataset
            latest_time_str = emotion_steps[0][len(emotion_steps[0])-1]
            latest_time_datetime = datetime.datetime.strptime(latest_time_str, "%Y-%m-%d %H:%M:%S")+datetime.timedelta(days=1)
            # change the time format to year-month-day so that it can be used in javascript
            latest_time_str = latest_time_datetime.strftime("%Y-%m-%d %H:%M:%S")[:10]
        
            # we just want to display the recent 7days or 1 day in default
            date_default_datetime = latest_time_datetime - datetime.timedelta(days=7)
            date_default_str = date_default_datetime.strftime("%Y-%m-%d %H:%M:%S")
            date_default_str = date_default_str[:10]
            
            # print(date_default_str)
            # print(latest_time_str)
            return render(request, 'tracking.html', {'emotion_steps':emotion_steps, 'dept_list': dept_list, 'dept_id':str(dept_id), 'date_default_str':date_default_str, 'latest_time_str':latest_time_str})
        return render(request, 'tracking.html', {'emotion_counter':emotion_counter, 'dept_list': dept_list, 'dept_id':str(dept_id)})

    # deal with action tab
    elif(tab=="action"):
        print("loading", tab)
        print("start", time.perf_counter())

        cursor.execute(
            "SELECT time, action FROM `sch_data`.`ema_storing_data` WHERE time > \"2021-03-01 00:00:00\" AND dep_id = (%s) ORDER BY time",
            dept_id)
        act_var = cursor.fetchall()

        nothing = action_helper(-2, -1, act_var, 0)
        timeout = action_helper(0, 8, act_var, 1)
        breathing = action_helper(9, 11, act_var, 2)
        bodyscan = action_helper(12, 13, act_var, 3)
        activities = action_helper(14, 21, act_var, 4)
        act_list = [nothing, timeout, breathing, bodyscan, activities]
        # print(act_list)

        print("end", time.perf_counter())
        return render(request, 'tracking.html', {'dept_list': dept_list, 'dept_id':str(dept_id), 'act_list':act_list})

    # deal with stress_level
    elif(tab=="stress_level"):
        print("loading", tab)
        print("start", time.perf_counter())

        cursor.execute(
            "SELECT TimeReceived, Response FROM `sch_data`.reward_data where QuestionName REGEXP \"baseline:recomm:likertconfirm:1\" AND Response !=\"-1.0\" AND Response !=\"-1\" AND dep_id = (%s) ORDER BY TimeReceived",
            dept_id)
        baseline_db = cursor.fetchall()
        baseline_list = []
        baseline_timestamp = []
        baseline_response = []
        for item in baseline_db:
            baseline_timestamp.append(item[0])
            baseline_response.append(int(item[1]))
        baseline_list.append(baseline_timestamp)
        baseline_list.append(baseline_response)

        print("end", time.perf_counter())




        # load emotion/table data in stress_level tab and save them to the session
        print("loading", tab)
        print("start", time.perf_counter())

        # just get the specific dep we want rather than all of them
        cursor.execute(
            "SELECT DISTINCT dep_id FROM `sch_data`.`ema_storing_data` WHERE dep_id NOT regexp \"^-1$|^200$|^999$|^6232021$|^10$|^11111$|^11112$\" AND dep_id = (%s)", dept_id)
        dep_id = cursor.fetchall()
    
        # just one item in dep_id
        for id in dep_id:
            # Only retrieve data of the dep_id we want to monitor (this can reduce some loading time)
            if id[0] not in monitor_date_table:
                continue

            if id[0] in deployment_date_table:
                date = deployment_date_table[id[0]]
                if date[1] != "":
                    emo_var_SQL = "SELECT time, event_vct FROM `sch_data`.`ema_storing_data` WHERE time between\"" + date[0] + "\" AND \""+ date[1]+"\" AND dep_id = (%s) ORDER BY time"
                elif date[1] == "":
                    emo_var_SQL = "SELECT time, event_vct FROM `sch_data`.`ema_storing_data` WHERE time >\"" + date[0] + "\" AND dep_id = (%s) ORDER BY time"
                else:
                    emo_var_SQL = "SELECT time, event_vct FROM `sch_data`.`ema_storing_data` WHERE time > \"2021-06-01 00:00:00\" AND dep_id = (%s) ORDER BY time"
            else:
                emo_var_SQL = "SELECT time, event_vct FROM `sch_data`.`ema_storing_data` WHERE time > \"2021-06-01 00:00:00\" AND dep_id = (%s) ORDER BY time"
                date = monitor_date_table[id[0]]

            cursor.execute(emo_var_SQL, id)
            emo_var = cursor.fetchall()

            #emotion
            if date[1] != "":
                start_date = datetime.datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S")
            elif date[1] == "":
                start_date = datetime.datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S")
            else:
                start_date = emo_var[0][0].replace(minute=0, second=0, microsecond=0)

            intervention_period = start_date + datetime.timedelta(days=30)
            # print("startdate",start_date)
            # print("intev",intervention_period)

            intervention_period_counter = [0, 0, 0, 0, 0, 0]
            baseline_period_counter = [0, 0, 0, 0, 0, 0]
            total_emotion_counter = [0, 0, 0, 0, 0, 0]
            counted_period = [0, 0, 0, 0, 0, 0]

            emotion_steps = [[],[],[],[],[],[],[]]
            counter = 0
            counting_step = datetime.timedelta(hours=1)

            def intervention_period_helper(index):
                if item[0] > intervention_period:
                    intervention_period_counter[index] += 1
                else:
                    baseline_period_counter[index] += 1
                total_emotion_counter[index] += 1
                counted_period[index] += 1

            def emo_counter_helper(counted,time):
                # as long as there is one emotion that is not counted as 0, we record this day
                record=False
                for i in range(6):
                    if(counted[i])!=0:
                        record=True
                if (record):
                    for index in range(len(emotion_steps)):
                        if index == 0:
                            emotion_steps[0].append(time)
                        else:
                            emotion_steps[index].append(counted[index-1])
                                
            for item in emo_var:
                
                # period close
                while item[0] > start_date:
                    emo_counter_helper(counted_period, start_date.strftime("%Y-%m-%d %H:%M:%S"))
                    counted_period = [0, 0, 0, 0, 0, 0]
                    start_date = start_date + counting_step

                temp = json.loads(item[1])
                element = temp.index(max(temp[0:4]))
                if len(temp) == 6 and temp[5] > 0.525:
                    intervention_period_helper(5)
                if temp[0] == temp[1] == temp[2] == temp[3] == temp[4] == 0:
                    continue
                else:
                    intervention_period_helper(element)
                counter += 1

                # ensure the last one added
                if counter == len(emo_var) and counted_period != [0, 0, 0, 0, 0, 0]:
                    emo_counter_helper(counted_period, start_date.strftime("%Y-%m-%d %H:%M:%S"))

        emotion_counter = [baseline_period_counter, intervention_period_counter, total_emotion_counter]
        request.session['emotion_steps']=emotion_steps
        request.session['emotion_counter']=emotion_counter
        # load emotion/table data in stress_level tab and save them to the session



        return render(request, 'tracking.html', {'dept_list': dept_list, 'dept_id':str(dept_id), 'baseline_list':baseline_list})

    # deal with post recommendation
    elif(tab=="post_rec" or tab=="post_rec_pie" or tab=="post_rec_cum"):
        print("loading", tab)
        print("start", time.perf_counter())

        cursor.execute(
            "SELECT DISTINCT TimeSent, TimeReceived,Response,Question,QuestionName FROM "
            "`sch_data`.reward_data where QuestionName REGEXP "
            "\"daytime:postrecomm:helpfulno:1|daytime:postrecomm:helpfulyes:1|daytime:recomm:|daytime"
            ":postrecomm:implement:\" AND dep_id = (%s) ORDER BY TimeSent",
            dept_id)
        postrecomm_db = cursor.fetchall()

        postrecomm_list = []
        postrecomm_yes_timestamp = []
        postrecomm_no_timestamp = []
        postrecomm_yes = []
        postrecomm_no = []
        postrecomm_yes_text = []
        postrecomm_no_text = []
        postrecomm_pie = [0, 0, 0]
        now = datetime.datetime.now()

        if (len(postrecomm_db)):
            postrecomm_sum = [[0], [str(postrecomm_db[0][0])], [0], [str(postrecomm_db[0][0])], [0],
                              [str(postrecomm_db[0][0])]]
        else:
            postrecomm_sum = [[0], [now.strftime("%Y-%m-%d %H:%M:%S")], [0], [now.strftime("%Y-%m-%d %H:%M:%S")], [0],
                              [now.strftime("%Y-%m-%d %H:%M:%S")]]

        action_ID = ""

        print("development id: {}, number of items: {}".format(dept_id, len(postrecomm_db)))

        for item in postrecomm_db:
            # while not action_for_response:
            #     cursor.execute(
            #         "SELECT DISTINCT time, action FROM `sch_data`.`ema_storing_data` WHERE \"" + lower_bound.strftime(
            #             "%Y-%m-%d %H:%M:%S") + "\"< time and time <\"" + upper_bound.strftime(
            #             "%Y-%m-%d %H:%M:%S") + "\" AND dep_id = (%s) ORDER BY time",
            #         id)
            #     upper_bound = upper_bound + datetime.timedelta(0, 10)
            #     lower_bound = lower_bound - datetime.timedelta(0, 10)
            #     action_for_response = cursor.fetchall()

            if "daytime:recomm:" in item[4]:
                if "timeout" in item[4]:
                    action_ID = -1 + int(item[4][-1])   # this action_id mapping changed from 0+int(*) to -1+int(*), since timeout starts from action 0
                elif "breathing" in item[4]:
                    action_ID = 8 + int(item[4][-1])
                elif "bodyscan" in item[4]:
                    action_ID = 11 + int(item[4][-1])
                elif "enjoyable" in item[4]:
                    action_ID = 13 + int(item[4][-1])

            # elif ":postrecomm:implement:" in item[4]:
            #     if action_ID != "":
            #         if last_move == "posted" and item[2] != "-1.0":
            #             last_move = "responded"

            elif item[4] == "daytime:postrecomm:helpfulyes:1" and item[2] != "-1.0":
                if action_ID == "":
                    print("---"*10+"Error"+"---"*10)
                    print("deployment id: {}".format(id))
                    print("item: ", item)
                    print("---"*10+"End"+"---"*10)
                    continue
                else:
                    postrecomm_yes.append(int(item[2]))
                    postrecomm_yes_timestamp.append(str(item[0]))
                    postrecomm_yes_text.append(
                        str(item[0]) + "<br>Action:" + str(action_ID) +
                        "<br>" + action_lookup_table[int(action_ID)])

            elif item[4] == "daytime:postrecomm:helpfulno:1" and item[2] != "-1.0":
                bar_data = ""
                if "1" in list(item[2]):
                    bar_data += " I didn’t have enough time <br>" + str(item[0]) + "<br>Action:" + str(
                        action_ID) + "<br>" + action_lookup_table[action_ID]
                    postrecomm_pie[0] += 1
                    postrecomm_sum[0].append(postrecomm_pie[0])
                    postrecomm_sum[1].append(str(item[0]))

                if "2" in list(item[2]):
                    bar_data += " I didn’t think it would help <br>" + str(item[0]) + "<br>Action:" + str(
                        action_ID) + "<br>" + action_lookup_table[action_ID]
                    postrecomm_pie[1] += 1
                    postrecomm_sum[2].append(postrecomm_pie[1])
                    postrecomm_sum[3].append(str(item[0]))

                if "3" in list(item[2]):
                    bar_data += " I didn’t see the message <br>" + str(item[0]) + "<br>Action:" + str(
                        action_ID) + "<br>" + action_lookup_table[action_ID]
                    postrecomm_pie[2] += 1
                    postrecomm_sum[4].append(postrecomm_pie[2])
                    postrecomm_sum[5].append(str(item[0]))

                postrecomm_no_text.append(bar_data)
                postrecomm_no.append(-1)
                postrecomm_no_timestamp.append(str(item[0]))

            elif (item[4] == "daytime:postrecomm:helpfulno:1" or item[4] == "daytime:postrecomm:helpfulno:1") and item[2] == "-1.0":
                if action_ID:
                    postrecomm_yes.append(0)
                    postrecomm_yes_timestamp.append(str(item[0]))
                    postrecomm_yes_text.append(
                        str(item[0]) + "<br>Action:" + str(action_ID) +
                        "<br>" + action_lookup_table[int(action_ID)] + "(No user feed back on post recommendation)")

        postrecomm_list.append(postrecomm_yes_timestamp)
        postrecomm_list.append(postrecomm_no_timestamp)
        postrecomm_list.append(postrecomm_yes)
        postrecomm_list.append(postrecomm_no)
        postrecomm_list.append(postrecomm_yes_text)
        postrecomm_list.append(postrecomm_no_text)

        postrecomm_sum[0].append(postrecomm_sum[0][-1])
        postrecomm_sum[1].append(now.strftime("%Y-%m-%d %H:%M:%S"))
        postrecomm_sum[2].append(postrecomm_sum[2][-1])
        postrecomm_sum[3].append(now.strftime("%Y-%m-%d %H:%M:%S"))
        postrecomm_sum[4].append(postrecomm_sum[4][-1])
        postrecomm_sum[5].append(now.strftime("%Y-%m-%d %H:%M:%S"))

        print("end", time.perf_counter())
        if(tab=="post_rec"):
            return render(request, 'tracking.html', {'dept_list': dept_list, 'dept_id':str(dept_id), 'postrecomm_list':postrecomm_list})
        elif(tab=="post_rec_pie"):
            return render(request, 'tracking.html', {'dept_list': dept_list, 'dept_id':str(dept_id), 'postrecomm_pie':postrecomm_pie})
        else:
            return render(request, 'tracking.html', {'dept_list': dept_list, 'dept_id':str(dept_id), 'postrecomm_sum':postrecomm_sum})

    # deal with other conditions, if not one of our tabs, return to the instruction page
    else:
        return redirect("/dataviewer/tracking/")


# homepage, does not calculate data for each deps but just display the homepage
def tracking(request):

    print("instruction")
    print("start", time.perf_counter())
    cursor = connections['ema'].cursor()
    dept_list = []
    if('dept_list' in request.session):
        dept_list = request.session['dept_list']
    else:
        cursor.execute(
            "SELECT DISTINCT dep_id FROM `sch_data`.`ema_storing_data` WHERE dep_id NOT regexp \"^-1$|^200$|^999$|^6232021$|^10$|^11111$|^11112$\"")
        dep_id = cursor.fetchall()
        # adding a dept_list in order to display the side bar containing each avaliable date button that we can click on to load its corresponding data    
        for id in dep_id:
            if id[0] in monitor_date_table:
                dept_list.append(id[0])
        # record dept_list using session so that we do not need to access the aws repeatedly
        request.session['dept_list']=dept_list
    print("end", time.perf_counter())
    return render(request, 'tracking.html', {'dept_list': dept_list})


def action_helper(left, right, data, action_category):
    act_var_list = []
    action_text = []
    action_time_stump = []
    for d in data:
        acting_id = d[1]
        if left <= acting_id <= right:
            act_var_list.append(action_category)
            if acting_id != -1:
                action_text.append("Action: " + str(acting_id) + "<br>" + action_lookup_table[acting_id])
            else:
                action_text.append("Action: " + str(acting_id) + "<br>" + "N/A")
            action_time_stump.append(d[0].strftime("%Y-%m-%d %H:%M:%S"))
    return [act_var_list, action_text, action_time_stump]


def daily(request):
    # check if user login before accessing the page
    if(not request.user.is_authenticated):
        print("please login!")
        return redirect("/accounts/google/login/")
    print("google account logged in!")
    # if google account is not authorized, back to login page and logout from google account
    if (not email_check(request.user)):
        messages.error(request, 'Sorry. You do not have access to the data.')
        print("account does not access!")
        return redirect("/dataviewer/tracking")

    cursor = connections['ema'].cursor()
    cursor.execute("SELECT DISTINCT dep_id FROM `sch_data`.`reward_data` WHERE dep_id NOT regexp "
                   "\"^-1$|^200$|^999$|^10$|^11111$|^11112$\"")
    dep_id = cursor.fetchall()
    daily_list = []

    for id in dep_id:

        stress = []
        stress_timestamp = []
        lonely = []
        lonely_timestamp = []
        health1 = []
        health1_timestamp = []
        health2 = []
        health2_timestamp = []
        interactions1 = []
        interactions1_timestamp = []
        interactions2 = []
        interactions2_timestamp = []
        evening = []

        goal = []

        start = ''

        if str(id[0]) not in monitor_date_table:
            continue

        if str(id[0]) in deployment_date_table:
            start = deployment_date_table[str(id[0])][0]
        else:
            start = "06-01-2021 00:00:00"

        cursor.execute(
            "SELECT TimeReceived, Response FROM `sch_data`.reward_data where QuestionName REGEXP \"evening:likert:stress:1|baseline:evening:likertstress:1\" AND Response !=\"-1.0\" AND Response !=\"-1\" AND TimeReceived !=\"NA\" AND dep_id = (%s) AND TimeSent > \"" + start + " \" ORDER BY TimeReceived",
            id)
        stress_db = cursor.fetchall()
        for item in stress_db:
            stress_timestamp.append(item[0])
            stress.append(int(item[1]))
        evening.append([stress_timestamp, stress])

        cursor.execute(
            "SELECT TimeReceived, Response FROM `sch_data`.reward_data where QuestionName REGEXP \"evening:likert:lonely:1|baseline:evening:likertlonely:1\" AND Response !=\"-1.0\" AND Response !=\"-1\" AND TimeReceived !=\"NA\" AND dep_id = (%s) AND TimeSent > \"" + start + " \" ORDER BY TimeReceived",
            id)
        lonely_db = cursor.fetchall()
        for item in lonely_db:
            lonely_timestamp.append(item[0])
            lonely.append(int(item[1]))
        evening.append([lonely_timestamp, lonely])

        cursor.execute(
            "SELECT TimeReceived, Response FROM `sch_data`.reward_data where QuestionName REGEXP \"evening:likert:health:1|baseline:evening:likerthealth:1\" AND Response !=\"-1.0\" AND Response !=\"-1\" AND TimeReceived !=\"NA\" AND dep_id = (%s) AND TimeSent > \"" + start + " \" ORDER BY TimeReceived",
            id)
        health1_db = cursor.fetchall()
        for item in health1_db:
            health1_timestamp.append(item[0])
            health1.append(int(item[1]))
        evening.append([health1_timestamp, health1])

        cursor.execute(
            "SELECT TimeReceived, Response FROM `sch_data`.reward_data where QuestionName REGEXP \"evening:likert:health:2|baseline:evening:likerthealth:2\" AND Response !=\"-1.0\" AND Response !=\"-1\" AND TimeReceived !=\"NA\" AND dep_id = (%s) AND TimeSent > \"" + start + " \" ORDER BY TimeReceived",
            id)
        health2_db = cursor.fetchall()
        for item in health2_db:
            health2_timestamp.append(item[0])
            health2.append(int(item[1]))
        evening.append([health2_timestamp, health2])

        def has_numbers(item):
            return bool(re.search(r'^\d+$', item))

        cursor.execute(
            "SELECT TimeReceived, Response FROM `sch_data`.reward_data where QuestionName REGEXP \"evening:textbox:interactions:1|baseline:evening:textboxinteractions:1\" AND Response !=\"-1.0\" AND Response !=\"-1\" AND TimeReceived !=\"NA\" AND dep_id = (%s) AND TimeSent > \"" + start + " \" ORDER BY TimeReceived",
            id)
        interactions1_db = cursor.fetchall()
        for item in interactions1_db:
            interactions1_timestamp.append(item[0])
            if has_numbers(item[1]):
                interactions1.append(int(item[1]))
            else:
                interactions1.append(0)
        evening.append([interactions1_timestamp, interactions1])

        cursor.execute(
            "SELECT TimeReceived, Response FROM `sch_data`.reward_data where QuestionName REGEXP \"evening:textbox:interactions:2|baseline:evening:textboxinteractions:2\" AND Response !=\"-1.0\" AND Response !=\"-1\" AND TimeReceived !=\"NA\" AND dep_id = (%s) AND TimeSent > \"" + start + " \" ORDER BY TimeReceived",
            id)
        interactions2_db = cursor.fetchall()
        for item in interactions2_db:
            interactions2_timestamp.append(item[0])
            interactions2.append(int(item[1]))
        evening.append([interactions2_timestamp, interactions2])

        cursor.execute(
            "SELECT TimeReceived, Response, QuestionName FROM `sch_data`.reward_data where QuestionName REGEXP \"evening:daily:goalyes:1|evening:daily:goalno:1\" AND Response !=\"-1.0\" AND Response !=\"-1\" AND TimeReceived !=\"NA\" AND dep_id = (%s) AND TimeSent > \"" + start + " \" ORDER BY TimeReceived",
            id)
        goal_db = cursor.fetchall()

        goal_yes_timestamp = []
        goal_no_timestamp = []
        goal_yes = []
        goal_no = []
        goal_yes_text = []
        goal_no_text = []
        for item in goal_db:
            if item[1] == "0":
                goal_yes_timestamp.append(str(item[0]))
                goal_yes.append(1)
                goal_yes_text.append("All good")
            else:
                bar_data = ""
                if "1" in list(item[1]):
                    bar_data += " I didn’t have enough time <br>"
                if "2" in list(item[1]):
                    bar_data += " I was too tired or stressed <br>"
                if "3" in list(item[1]):
                    bar_data += " I was distracted by other tasks or activities <br>"
                if "4" in list(item[1]):
                    bar_data += " I did not set a goal"
                goal_no_timestamp.append(str(item[0]))
                goal_no_text.append(bar_data)
                goal_no.append(-1)
        goal.append(goal_yes_timestamp)
        goal.append(goal_no_timestamp)
        goal.append(goal_yes)
        goal.append(goal_no)
        goal.append(goal_yes_text)
        goal.append(goal_no_text)

        feedback_list = []

        about = []
        helpful = []
        helpful_timestamp = []

        cursor.execute(
            "SELECT TimeReceived, Response, QuestionName FROM `sch_data`.reward_data where QuestionName REGEXP \"evening:stress:managno:1|evening:stress:managyes:1\" AND Response !=\"-1.0\" AND Response !=\"-1\" AND TimeReceived !=\"NA\" AND dep_id = (%s) AND TimeSent > \"" + start + " \" ORDER BY TimeReceived",
            id)
        about_db = cursor.fetchall()
        about_yes_timestamp = []
        about_no_timestamp = []
        about_yes = []
        about_no = []
        about_yes_text = []
        about_no_text = []
        positive = [0, 0, 0, 0]
        positive_daily = [0, 0, 0, 0]
        negative = [0, 0, 0]
        negative_daily = [0, 0, 0]
        now = datetime.datetime.now()

        if str(id[0]) in deployment_date_table:
            start_date = deployment_date_table[str(id[0])][0]
            if deployment_date_table[str(id[0])][1] == "":
                end_date = now.strftime("%Y-%m-%d %H:%M:%S")
            else:
                end_date = deployment_date_table[str(id[0])][1]

        else:
            start_date = "2021-07-01 00:00:00"
            end_date = now.strftime("%Y-%m-%d %H:%M:%S")

        about_sum = [[[[0], [start_date]], [[0], [start_date]], [[0], [start_date]], [[0], [start_date]], [[0], [start_date]], [[0], [start_date]], [[0], [start_date]], [[0], [start_date]]],
                     [[[0], [start_date]], [[0], [start_date]], [[0], [start_date]], [[0], [start_date]], [[0], [start_date]], [[0], [start_date]]]]

        for item in about_db:
            positive_daily = [0, 0, 0, 0]
            negative_daily = [0, 0, 0]
            if item[2] == "evening:stress:managyes:1":
                bar_data = ""
                if "1" in list(item[1]):
                    bar_data += " Deep breathing <br>"
                    positive[0] += 1
                    positive_daily[0] += 1
                    about_sum[0][0][0].append(positive[0])
                    about_sum[0][0][1].append(str(item[0]))
                    about_sum[0][4][0].append(positive_daily[0])
                    about_sum[0][4][1].append(str(item[0]))
                if "2" in list(item[1]):
                    bar_data += " Time out <br>"
                    positive[1] += 1
                    positive_daily[1] += 1
                    about_sum[0][1][0].append(positive[1])
                    about_sum[0][1][1].append(str(item[0]))
                    about_sum[0][5][0].append(positive_daily[1])
                    about_sum[0][5][1].append(str(item[0]))
                if "3" in list(item[1]):
                    bar_data += " Body Scan <br>"
                    positive[2] += 1
                    positive_daily[2] += 1
                    about_sum[0][2][0].append(positive[2])
                    about_sum[0][2][1].append(str(item[0]))
                    about_sum[0][6][0].append(positive_daily[2])
                    about_sum[0][6][1].append(str(item[0]))
                if "4" in list(item[1]):
                    bar_data += " Enjoyable Activity<br>"
                    positive[3] += 1
                    positive_daily[3] += 1
                    about_sum[0][3][0].append(positive[3])
                    about_sum[0][3][1].append(str(item[0]))
                    about_sum[0][7][0].append(positive_daily[3])
                    about_sum[0][7][1].append(str(item[0]))
                about_yes_timestamp.append(str(item[0]))
                about_yes.append(1)
                about_yes_text.append(bar_data)
            else:
                bar_data = ""
                if "1" in list(item[1]):
                    bar_data += " I didn’t have time <br>"
                    negative[0] += 1
                    about_sum[1][0][0].append(negative[0])
                    about_sum[1][0][1].append(str(item[0]))
                    # negative_daily[0] += 1
                    # about_sum[1][3][0].append(negative_daily[0])
                    # about_sum[1][3][1].append(str(item[0]))
                if "2" in list(item[1]):
                    bar_data += " I didn’t think it would help.<br>"
                    negative[1] += 1
                    about_sum[1][1][0].append(negative[1])
                    about_sum[1][1][1].append(str(item[0]))
                    # negative_daily[1] += 1
                    # about_sum[1][4][0].append(negative_daily[1])
                    # about_sum[1][4][1].append(str(item[0]))
                if "3" in list(item[1]):
                    bar_data += " I didn’t see the message(s)"
                    negative[2] += 1
                    about_sum[1][2][0].append(negative[2])
                    about_sum[1][2][1].append(str(item[0]))
                    # negative_daily[2] += 1
                    # about_sum[1][5][0].append(negative_daily[2])
                    # about_sum[1][5][1].append(str(item[0]))
                about_no_timestamp.append(str(item[0]))
                about_no_text.append(bar_data)
                about_no.append(-1)

        about_sum[0][0][0].append(about_sum[0][0][0][-1])
        about_sum[0][0][1].append(end_date)
        about_sum[0][1][0].append(about_sum[0][1][0][-1])
        about_sum[0][1][1].append(end_date)
        about_sum[0][2][0].append(about_sum[0][2][0][-1])
        about_sum[0][2][1].append(end_date)
        about_sum[0][3][0].append(about_sum[0][3][0][-1])
        about_sum[0][3][1].append(end_date)
        about_sum[0][4][0].append(about_sum[0][4][0][-1])
        about_sum[0][4][1].append(end_date)
        about_sum[0][5][0].append(about_sum[0][5][0][-1])
        about_sum[0][5][1].append(end_date)
        about_sum[0][6][0].append(about_sum[0][6][0][-1])
        about_sum[0][6][1].append(end_date)
        about_sum[0][7][0].append(about_sum[0][7][0][-1])
        about_sum[0][7][1].append(end_date)
        about_sum[1][0][0].append(about_sum[1][0][0][-1])
        about_sum[1][0][1].append(end_date)
        about_sum[1][1][0].append(about_sum[1][1][0][-1])
        about_sum[1][1][1].append(end_date)
        about_sum[1][2][0].append(about_sum[1][2][0][-1])
        about_sum[1][2][1].append(end_date)
        # about_sum[1][3][0].append(about_sum[1][3][0][-1])
        # about_sum[1][3][1].append(end_date)
        # about_sum[1][4][0].append(about_sum[1][4][0][-1])
        # about_sum[1][4][1].append(end_date)
        # about_sum[1][5][0].append(about_sum[1][5][0][-1])
        # about_sum[1][5][1].append(end_date)


        about.append(about_yes_timestamp)
        about.append(about_no_timestamp)
        about.append(about_yes)
        about.append(about_no)
        about.append(about_yes_text)
        about.append(about_no_text)
        about.append(positive)
        about.append(negative)
        about.append(about_sum)

        cursor.execute(
            "SELECT TimeReceived, Response, QuestionName FROM `sch_data`.reward_data where QuestionName REGEXP \"evening:stress:managyes:2|evening:system:helpful:2|evening:system:helpful:3\" AND Response !=\"-1.0\" AND Response !=\"-1\" AND dep_id = (%s) ORDER BY TimeReceived",
            id)
        helpful_db = cursor.fetchall()
        helpful_rate = 0

        if helpful_db:
            start_from = datetime.datetime.strptime(helpful_db[0][0], "%Y-%m-%d %H:%M:%S")
        else:
            start_from = datetime.datetime.strptime("2021-06-01 00:00:00", "%Y-%m-%d %H:%M:%S")

        period = datetime.timedelta(days=1)
        helpful_most = "Helped most:<br>"
        helpful_reduce = "Helped reducing stress:<br>"
        last_time = ''
        for item in helpful_db:
            if item[2] == "evening:stress:managyes:2":
                helpful_rate = item[1]
            elif item[2] == "evening:system:helpful:2":
                if "1" in list(item[1]):
                    helpful_most += " Deep breathing <br>"
                if "2" in list(item[1]):
                    helpful_most += " Time out <br>"
                if "3" in list(item[1]):
                    helpful_most += " Body Scan <br>"
                if "4" in list(item[1]):
                    helpful_most += " Enjoyable Activity<br>"
            elif item[2] == "evening:system:helpful:3":
                data = "Helped reducing stress:<br>"
                if "1" in list(item[1]):
                    helpful_reduce += " Deep breathing <br>"
                if "2" in list(item[1]):
                    helpful_reduce += " Time out <br>"
                if "3" in list(item[1]):
                    helpful_reduce += " Body Scan <br>"
                if "4" in list(item[1]):
                    helpful_reduce += " Enjoyable Activity<br>"
            last_time = item[0]

            while datetime.datetime.strptime(item[0], "%Y-%m-%d %H:%M:%S") > start_from:
                helpful_timestamp.append([last_time, int(helpful_rate), (helpful_most + helpful_reduce)])
                start_from = start_from + period
                helpful_most = "Helped most:<br>"
                helpful_reduce = "Helped reducing stress:<br>"

        helpful.append([x[0] for x in helpful_timestamp])
        helpful.append([x[1] for x in helpful_timestamp])
        helpful.append([x[2] for x in helpful_timestamp])

        cursor.execute(
            "SELECT TimeReceived, Response, QuestionName FROM `sch_data`.reward_data where QuestionName REGEXP \"daytime:check_in:reactive:1\" AND Response !=\"-1.0\" AND Response !=\"-1\" AND dep_id = (%s) ORDER BY TimeReceived",
            id)
        reactive_db = cursor.fetchall()
        reactive_timestamp = []
        reactive = []
        reactive_pie = [0, 0, 0, 0]
        for item in reactive_db:
            reactive_timestamp.append(item[0])
            reactive.append(int(item[1]))
            if item[1] == "1":
                reactive_pie[0] += 1
            elif item[1] == "2":
                reactive_pie[1] += 1
            elif item[1] == "3":
                reactive_pie[2] += 1
            elif item[1] == "4":
                reactive_pie[3] += 1
            else:
                continue
        reactive_list = [reactive_timestamp, reactive, reactive_pie]

        daily_list.append([id[0], evening, goal, about, helpful, reactive_list])

    return render(request, 'daily.html', {"daily": daily_list})


# def feedback(id, cursor):
#     # cursor = connections['ema'].cursor()
#     # cursor.execute("SELECT DISTINCT dep_id FROM `sch_data`.`reward_data` WHERE dep_id NOT regexp \"^-1|^200|^999\"")
#     # dep_id = cursor.fetchall()
#     feedback_list = []
#     #
#     # for id in dep_id:
#
#     about = []
#     about_timestamp = []
#
#     helpful = []
#     helpful_timestamp = []
#
#     cursor.execute(
#         "SELECT TimeReceived, Response, QuestionName FROM `sch_data`.reward_data where QuestionName REGEXP \"evening:stress:managno:1|evening:stress:managyes:1\" AND Response !=\"-1.0\" AND Response !=\"-1\" AND TimeReceived !=\"NA\" AND dep_id = (%s) ORDER BY TimeReceived",
#         id)
#     about_db = cursor.fetchall()
#     about_yes = []
#     about_no = []
#     about_yes_text = []
#     about_no_text = []
#     for item in about_db:
#         about_timestamp.append(str(item[0]))
#         if item[2] == "evening:stress:managyes:1":
#             bar_data = ""
#             if "1" in list(item[1]):
#                 bar_data += " Deep breathing <br>"
#             if "2" in list(item[1]):
#                 bar_data += " Time out <br>"
#             if "3" in list(item[1]):
#                 bar_data += " Body Scan <br>"
#             if "4" in list(item[1]):
#                 bar_data += " Enjoyable Activity"
#             about_yes.append(1)
#             about_no.append(0)
#             about_yes_text.append(bar_data)
#             about_no_text.append("")
#         else:
#             bar_data = ""
#             if "1" in list(item[1]):
#                 bar_data += " I didn’t have time <br>"
#             if "2" in list(item[1]):
#                 bar_data += " I didn’t think it would help.<br>"
#             if "3" in list(item[1]):
#                 bar_data += " I didn’t see the message(s)"
#             about_yes_text.append("")
#             about_no_text.append(bar_data)
#             about_yes.append(0)
#             about_no.append(-1)
#
#     about.append(about_timestamp)
#     about.append(about_yes)
#     about.append(about_no)
#     about.append(about_yes_text)
#     about.append(about_no_text)
#
#     cursor.execute(
#         "SELECT TimeReceived, Response, QuestionName FROM `sch_data`.reward_data where QuestionName REGEXP \"evening:stress:managyes:2|evening:system:helpful:2|evening:system:helpful:3\" AND Response !=\"-1.0\" AND Response !=\"-1\" AND dep_id = (%s) ORDER BY TimeReceived",
#         id)
#     helpful_db = cursor.fetchall()
#     helpful_rate = 0
#
#     if helpful_db:
#         start_from = datetime.datetime.strptime(helpful_db[0][0], "%Y-%m-%d %H:%M:%S")
#     else:
#         start_from = datetime.datetime.strptime("2021-06-01 00:00:00", "%Y-%m-%d %H:%M:%S")
#
#     period = datetime.timedelta(days=1)
#     helpful_most = "Helped most:<br>"
#     helpful_reduce = "Helped reducing stress:<br>"
#     last_time = ''
#     for item in helpful_db:
#         while datetime.datetime.strptime(item[0], "%Y-%m-%d %H:%M:%S") > start_from:
#             helpful_timestamp.append([last_time, int(helpful_rate), (helpful_most + helpful_reduce)])
#             start_from = start_from + period
#             helpful_most = "Helped most:<br>"
#             helpful_reduce = "Helped reducing stress:<br>"
#         if item[2] == "evening:stress:managyes:2":
#             helpful_rate = item[1]
#         elif item[2] == "evening:system:helpful:2":
#             if "1" in list(item[1]):
#                 helpful_most += " Deep breathing <br>"
#             if "2" in list(item[1]):
#                 helpful_most += " Time out <br>"
#             if "3" in list(item[1]):
#                 helpful_most += " Body Scan <br>"
#             if "4" in list(item[1]):
#                 helpful_most += " Enjoyable Activity<br>"
#         elif item[2] == "evening:system:helpful:3":
#             data = "Helped reducing stress:<br>"
#             if "1" in list(item[1]):
#                 helpful_reduce += " Deep breathing <br>"
#             if "2" in list(item[1]):
#                 helpful_reduce += " Time out <br>"
#             if "3" in list(item[1]):
#                 helpful_reduce += " Body Scan <br>"
#             if "4" in list(item[1]):
#                 helpful_reduce += " Enjoyable Activity<br>"
#         last_time = item[0]
#     helpful.append([x[0] for x in helpful_timestamp])
#     helpful.append([x[1] for x in helpful_timestamp])
#     helpful.append([x[2] for x in helpful_timestamp])
#
#     feedback_list.append([about, helpful])
#
#     return feedback_list


def weekly(request):
    # check if user login before accessing the page
    if(not request.user.is_authenticated):
        print("please login!")
        return redirect("/accounts/google/login/")
    print("google account logged in!")
    # if google account is not authorized, back to login page and logout from google account
    if (not email_check(request.user)):
        messages.error(request, 'Sorry. You do not have access to the data.')
        print("account does not access!")
        return redirect("/dataviewer/tracking")

    cursor = connections['ema'].cursor()
    cursor.execute(
        "SELECT DISTINCT dep_id FROM `sch_data`.`reward_data` WHERE dep_id NOT regexp \"^-1$|^200$|^999$|^10$|^11111$|^11112$\"")
    dep_id = cursor.fetchall()
    weekly = []

    for id in dep_id:
        if str(id[0]) not in monitor_date_table:
            continue
        temp = weekly_helper(id, cursor)
        weekly.append(temp)

    return render(request, 'weekly.html', {"weekly": weekly})


def weekly_helper(id, cursor):
    weekly_massage = [id[0]]
    type = ["weekly:messages:1|weekly:messages:no:1", "weekly:msgetime:1|weekly:msgetime:no:1",
            "weekly:startstop:1|weekly:startstop:no:1", "weekly:survey:1"]
    for i in range(0, 4):
        cursor.execute(
            "SELECT TimeReceived, Response, QuestionName FROM `sch_data`.reward_data where QuestionName REGEXP \"" +
            type[
                i] + "\" AND Response !=\"-1.0\" AND Response !=\"-1\" AND TimeReceived !=\"NA\" AND dep_id = (%s) ORDER BY TimeReceived",
            id)
        weekly_massage_db = cursor.fetchall()

        #
        if i == 3:
            bar = []
            bar_data_all = []
            timestamp = []
            bar_data_total = [0, 0, 0, 0, 0, 0, 0]
            for item in weekly_massage_db:
                bar_data = [0, 0, 0, 0, 0, 0, 0]
                if "1" in list(item[1]):
                    bar_data[0] = 1
                    bar_data_total[0] += 1
                if "2" in list(item[1]):
                    bar_data[1] = 1
                    bar_data_total[1] += 1
                if "3" in list(item[1]):
                    bar_data[2] = 1
                    bar_data_total[2] += 1
                if "4" in list(item[1]):
                    bar_data[3] = 1
                    bar_data_total[3] += 1
                if "5" in list(item[1]):
                    bar_data[4] = 1
                    bar_data_total[4] += 1
                if "6" in list(item[1]):
                    bar_data[5] = 1
                    bar_data_total[5] += 1
                if "7" in list(item[1]):
                    bar_data[6] = 1
                    bar_data_total[6] += 1
                bar_data_all.append(bar_data)
                timestamp.append(item[0])

            bar.append([x[0] for x in bar_data_all])
            bar.append([x[1] for x in bar_data_all])
            bar.append([x[2] for x in bar_data_all])
            bar.append([x[3] for x in bar_data_all])
            bar.append([x[4] for x in bar_data_all])
            bar.append([x[5] for x in bar_data_all])
            bar.append([x[6] for x in bar_data_all])

            weekly_massage.append([timestamp, bar, bar_data_total])

        else:
            weekly_massage_resp = []
            weekly_massage_resp_no = []
            weekly_massage_timestamp = []
            weekly_massage_timestamp_no = []
            weekly_massage_text = []
            weekly_massage_text_no = []
            no = False
            for item in weekly_massage_db:
                text = ""
                if no:
                    if i == 0:
                        if item[1] == "1":
                            text = "Prefer more massage"
                        elif item[1] == "2":
                            text = "Prefer fewer massage"
                    elif i == 1:
                        if item[1] == "1":
                            text = "More time between massage"
                        elif item[1] == "2":
                            text = "Less time between massage"
                    elif i == 2:
                        if item[1] == "1":
                            text = "Yes"
                        elif item[1] == "2":
                            text = "No"

                    weekly_massage_timestamp_no.append(item[0])
                    weekly_massage_resp_no.append(int(-1))
                    weekly_massage_text_no.append(text)
                    no = False
                elif item[1] == "0" and not no:
                    no = True
                else:
                    weekly_massage_timestamp.append(item[0])
                    weekly_massage_resp.append(int(1))
                    weekly_massage_text.append("")

            weekly_massage.append(
                [weekly_massage_timestamp, weekly_massage_resp, weekly_massage_text, weekly_massage_timestamp_no,
                 weekly_massage_resp_no,
                 weekly_massage_text_no])

    return weekly_massage
