from django.db import connections
import datetime

postrecomm_list = []
postrecomm_pie = [0, 0, 0]
postrecomm_sum = []

def start_up():
    cursor = connections['ema'].cursor()
    cursor.execute(
        "SELECT DISTINCT TimeReceived, Response,QuestionName FROM `sch_data`.reward_data where QuestionName REGEXP \"daytime:postrecomm:helpfulno:1|daytime:postrecomm:helpfulyes:1\" AND Response !=\"-1.0\" AND Response !=\"-1\" AND dep_id = (%s) ORDER BY TimeReceived",
        id)
    postrecomm_db = cursor.fetchall()


    postrecomm_yes_timestamp = []
    postrecomm_no_timestamp = []
    postrecomm_yes = []
    postrecomm_no = []
    postrecomm_yes_text = []
    postrecomm_no_text = []

    now = datetime.datetime.now()

    if (len(postrecomm_db)):
        postrecomm_sum = [[0], [str(postrecomm_db[0][0])], [0], [str(postrecomm_db[0][0])], [0],
                          [str(postrecomm_db[0][0])]]
    else:
        postrecomm_sum = [[0], [now.strftime("%Y-%m-%d %H:%M:%S")], [0], [now.strftime("%Y-%m-%d %H:%M:%S")], [0],
                          [now.strftime("%Y-%m-%d %H:%M:%S")]]

    for item in postrecomm_db:

        time = datetime.datetime.strptime(str(item[0]), "%Y-%m-%d %H:%M:%S")
        upper_bound = time + datetime.timedelta(0, 10)
        lower_bound = time - datetime.timedelta(0, 10)
        action_for_response = []

        while not action_for_response:
            cursor.execute(
                "SELECT DISTINCT time, action FROM `sch_data`.`ema_storing_data` WHERE \"" + lower_bound.strftime(
                    "%Y-%m-%d %H:%M:%S") + "\"< time and time <\"" + upper_bound.strftime(
                    "%Y-%m-%d %H:%M:%S") + "\" AND dep_id = (%s) ORDER BY time",
                id)
            upper_bound = upper_bound + datetime.timedelta(0, 10)
            lower_bound = lower_bound - datetime.timedelta(0, 10)
            action_for_response = cursor.fetchall()

        if item[2] == "daytime:postrecomm:helpfulyes:1":
            postrecomm_yes.append(int(item[1]))
            postrecomm_yes_timestamp.append(str(item[0]))
            postrecomm_yes_text.append(str(action_for_response[0][0]) + "<br>Action:" + str(action_for_response[0][1]))
        else:
            bar_data = ""
            if "1" in list(item[1]):
                bar_data += " I didn’t have enough time <br>" + str(action_for_response[0][0]) + "<br>Action" + str(
                    action_for_response[0][1])
                postrecomm_pie[0] += 1
                postrecomm_sum[0].append(postrecomm_pie[0])
                postrecomm_sum[1].append(str(item[0]))

            if "2" in list(item[1]):
                bar_data += " I didn’t think it would help <br>" + str(action_for_response[0][0]) + "<br>Action" + str(
                    action_for_response[0][1])
                postrecomm_pie[1] += 1
                postrecomm_sum[2].append(postrecomm_pie[1])
                postrecomm_sum[3].append(str(item[0]))

            if "3" in list(item[1]):
                bar_data += " I didn’t see the message <br>" + str(action_for_response[0][0]) + "<br>Action" + str(
                    action_for_response[0][1])
                postrecomm_pie[2] += 1
                postrecomm_sum[4].append(postrecomm_pie[2])
                postrecomm_sum[5].append(str(item[0]))

            postrecomm_no_text.append(bar_data)
            postrecomm_no.append(-1)
            postrecomm_no_timestamp.append(str(item[0]))
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
    return 0
