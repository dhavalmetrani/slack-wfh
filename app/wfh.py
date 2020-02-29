"""
Wfh details.
e.g. wfh list
e.g. wfh list 2020-02-29
e.g. wfh list 2020-02
e.g. wfh list 2020
e.g. wfh add @dhaval
e.g. wfh remove @dhaval

"""
import sys
import requests
import lib.util as util
import lib.slack as slack

s = slack.Slack()

def disaplay_wfh(current_date):
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

  msg = "The following members have reported wfh on `{}` so far: ".format(current_date)
  msg += "```"
  if not dict_wfh:
    msg += None
  else:
    for k, v in sorted(dict_wfh.items(), key=lambda x: x[1], reverse=True):
      msg += "\n- {} [ {} ]".format(k, v)
  msg += "```"
  print(msg)
  s.message_channel(channel="#testchannel", text=msg, link_names=True)

def main():
  """
  Main function.
  """
  # print(len(sys.argv))
  # print(sys.argv[0])
  current_date = str(util.get_today())
  if len(sys.argv) <= 1:
    print("Please specify proper parameters. [ wfh list | add | remove ]")
    exit(1)
  else:
    command = sys.argv[1].lower()
    if command == "list":
      if len(sys.argv) > 2:
        current_date = sys.argv[2].lower()
      disaplay_wfh(current_date)
    elif command == "add":
      if len(sys.argv) <= 2:
        print("Please specify a user to add. e.g. wfh add @amithkumar")
        exit(1)
      else:
        user_to_add = sys.argv[2].lower()
        util.add_wfh(user_to_add, str(current_date))
        disaplay_wfh(current_date)

    elif command == "remove":
      if len(sys.argv) <= 2:
        print("Please specify a user to remove. e.g. wfh add @amithkumar")
        exit(1)
      else:
        user_to_remove = sys.argv[2].lower()
        util.remove_wfh(user_to_remove, str(current_date))
        disaplay_wfh(current_date)
    else:
      print("Invalid command: {}. Please specify proper parameters. [ wfh list | add | remove ]".format(command))

    # user_to_add = sys.argv[1].lower()
    # # print(user_to_add)
    # util.add_wfh(user_to_add, str(current_date))


if __name__ == '__main__':
  """
  Main guard.
  """
  main()
