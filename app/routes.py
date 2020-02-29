from app import app
from flask import request
import sys
import requests
import lib.util as util
import lib.slack as slack

# PRIVATE_CHANNEL="GGNP03DN3"
PRIVATE_CHANNEL="GU0HV4N01"
# PRIVATE_CHANNEL="GU0HV4N01"
s = slack.Slack()

def disaplay_wfh(current_date, pre_msg, slack=False):
  """
  Display all wfh.
  """

  users_wfh = []
  arr = current_date.split("-")
  dd = None
  mm = None
  yy = None
  if len(arr) > 2:
    dd = arr[2]
  if len(arr) > 1:
    if len(arr[1]) == 1:
      arr[1] = "0" + arr[1]
    mm = arr[1]
  if len(arr) > 0:
    yy = arr[0]

  today = util.get_today()
  date_range = []
  if len(arr) == 3:
    date_range = [current_date]
  elif len(arr) == 2:
    for day in range(1, 32):
      date_range.append("{}-{}-{}".format(str(yy), str(mm), str(day)))
  elif len(arr) == 1:
    for month in range(1, 13):
      for day in range(1, 32):
        _mm = str(month)
        if len(str(month)) == 1:
          _mm = "0" + str(month)
        date_range.append("{}-{}-{}".format(str(yy), str(_mm), str(day)))

  # print(date_range)
  dict_wfh = {}
  for specific_date in date_range:
    # if len(util.get_wfh(str(specific_date))) == 0:
    # print(str(specific_date))
    for _ in util.get_wfh(str(specific_date)):
      if _ not in dict_wfh:
        dict_wfh[_] = 1
      else:
        dict_wfh[_] += 1
  # users_wfh.append("- {}".format(_))

  msg = pre_msg + "The following members have reported wfh on `{}` so far: ".format(current_date)
  msg_datewise = ""
  msg += "```"

  if not dict_wfh:
    msg += "None"
  else:
    for k, v in sorted(dict_wfh.items(), key=lambda x: x[1], reverse=True):
      msg += "\n- {} [ {} ]".format(k, v)


    wfh_config = util.get_wfh_config()
    for specific_date in date_range:
      # print(specific_date)
      # util.pprint(util.get_wfh_config())
      if specific_date in wfh_config:
        msg_datewise += "\n- [ {} ]: {}".format(specific_date, wfh_config[specific_date])

  msg += "```\n"
  if len(msg_datewise) > 0:
    msg_datewise = "Datewise WFH: \n```" + msg_datewise + "```"
  if slack:
    s.message_channel(channel="#testchannel", text=msg+msg_datewise, link_names=True)
  return msg

@app.route('/index', methods=['GET', 'POST'])
def index():
    return ("This is the index page.")

@app.route('/', methods=['GET', 'POST'])
def get_details():
    current_date = str(util.get_today())
    data = None
    # pre_msg = "[ Add ] WFH invoked by {}. \nWFH reported for {}."
    pre_msg = "*[ {} ]* WFH Invoked by @{}.\n Reported for: {}. Successful!\n"
    msg = "Error"
    user_name = "None"
    channel_id = "None"
    user_to_operate = ""
    try:
        data = request.form.get("text").split(" ")
        user_name = request.form.get("user_name")
        channel_id = request.form.get("channel_id")
    except Exception as ex:
        return msg
    if data:
        command = "add"
        # pre_msg = "Invoked by @{}.\n".format(user_name)
        if len(data) > 0:
          command = data[0].lower()
          if command == "list":
            pre_msg = "*[ List ]* WFH Invoked by @{}.\n".format(user_name)
            # return(channel_id)
            if channel_id == PRIVATE_CHANNEL:
              if len(data) > 1:
                current_date = data[1].lower()
              disaplay_wfh(current_date, pre_msg, True)
            else:
              return("Sorry. You are not authorized to run this command.")
          elif command == "add":
            if len(data) <= 1:
              return("Please specify a user to add. e.g. wfh add @amithkumar")
            else:
              user_to_operate = data[1].lower()
              util.add_wfh(user_to_operate, str(current_date))
              cmd = "Add"
              pre_msg = pre_msg.format(cmd, user_name, user_to_operate)
              disaplay_wfh(current_date, pre_msg, True)
              return(pre_msg)

          elif command == "remove":
            if len(data) <= 1:
              return("Please specify a user to remove. e.g. wfh add @amithkumar")
            else:
              user_to_operate = data[1].lower()
              util.remove_wfh(user_to_operate, str(current_date))
              cmd = "Remove"
              pre_msg = pre_msg.format(cmd, user_name, user_to_operate)
              disaplay_wfh(current_date, pre_msg, True)
              return(pre_msg)
          else:
            user_to_operate = data[0].lower()
            # print("###################")
            # print(user_to_operate)
            # print("###################")
            if user_to_operate[0] == "@":
                util.add_wfh(user_to_operate, str(current_date))
                # pre_msg = "Invoked by @{}.\n".format(user_name)
                cmd = "Add"
                pre_msg = pre_msg.format(cmd, user_name, user_to_operate)
                disaplay_wfh(current_date, pre_msg, True)
                return(pre_msg)
            else:
                return("Invalid command: {}. Please specify proper parameters. [ wfh <user_to_add> | add | remove ]".format(command))
        else:
          return("Invalid command: {}. Please specify proper parameters. [ wfh <user_to_add> | add | remove ]".format(command))
    return ""
    # return disaplay_wfh(current_date, pre_msg)
