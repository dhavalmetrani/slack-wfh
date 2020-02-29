"""
Utility functions.
"""
import json
import sys
import os
import subprocess
import traceback
import csv
import requests
import redis

from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse

import logging

import lib.constants as constants


def init_logging(mode=logging.INFO):
  """
  Sets the logging mode.
  :mode: Logging mode
  :returns: Log handler
  """
  global log
  log = None
  log = logging.getLogger(constants.LOGGER_NAME)
  # log.setLevel(os.getenv(constants.LOG_LEVEL, mode))
  # log.addHandler(logging.StreamHandler(sys.stdout))
  # log.info("Module: {} Function: {}".format(__name__, sys._getframe().f_code.co_name))

def pprint(json_data):
  """
  Pretty print json data.
  :json_data: Json data to print.
  """
  # log.info("Module: {} Function: {}".format(__name__, sys._getframe().f_code.co_name))
  print(json.dumps(json_data, indent=4, sort_keys=True))

def load_json(file_path):
  """
  Read the contents of file and load as json.
  :file_path: Path of file.
  :returns: json format of specified file
  """
  # log.info("Module: {} Function: {}".format(__name__, sys._getframe().f_code.co_name))
  data = "{}"
  try:
    if os.path.isfile(file_path):
      with open(file_path, "r") as f:
        data = f.read()
  except Exception as ex:
    # log.error("Cannot load json data.")
    data = "{}"

  return json.loads(data)

def run_process(command="ls"):
  """
  Run command.
  :command: Command to run.
  :returns: Boolean value specifying successful execution of command.
  """
  # log.info("Module: {} Function: {}".format(__name__, sys._getframe().f_code.co_name))
  # log.info("Running command: "+ command)
  process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  output = ""
  error = ""
  for line in process.stdout:
    output += line
    process.wait()
  for line in process.stderr:
    error += line
    process.wait()
  if len(output) >= 1:
    # log.info(output)
    print(output)
  if len(error) >= 1:
    print(error)
    # log.critical(error)
    # log.info("Return code from kinit: " + str(process.returncode))
  if process.returncode != 0:
    err_msg = "Error during kinit. Make sure you have speficied the correct password."
    raise ValueError(err_msg)


def get_arg_type(arg):
  """
  Get the type of argument passed.
  :arg: Argument passed.
  :returns: Type of argument.
  """
  # log.info("Module: {} Function: {}".format(__name__, sys._getframe().f_code.co_name))
  try:
    type = int(arg)
    return "int"
  except:
    return "str"

def write_csv(output_csv, csv_cols, list_data):
  """
  Write csv file.
  :output_csv: csv file to write.
  :csv_cols: Columns to write.
  :list_data: List of rows data to write.
  """
  # log.info("Module: {} Function: {}".format(__name__, sys._getframe().f_code.co_name))
  try:
    # log.info(os.getcwd())
    # log.info(output_csv)
    with open(output_csv, 'w') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=csv_cols)
      writer.writeheader()
      for data in list_data:
        writer.writerow(data)
  except IOError:
    # log.error("I/O error while writing CSV file.")
    print("I/O error while writing CSV file.")

def setup_redis_connection(host="localhost"):
  """
  Sets up redis connection
  :host: Redis hostname
  :returns: Redis connection.
  """
  # log.info("Module: {} Function: {}".format(__name__, sys._getframe().f_code.co_name))
  return redis.Redis(host=host)

def get_csv_rows(file_path):
  """
  Returns a list of csv rows
  :file_path: Source csv file.
  :returns: a list of csv rows
  """
  # log.info("Module: {} Function: {}".format(__name__, sys._getframe().f_code.co_name))
  list = []
  # log.info(file_path)
  if not os.path.isfile(file_path):
    err_msg = "File does not exist: {}".format(file_path)
    raise Exception(err_msg)
  with open(file_path, mode='r') as infile:
    reader = csv.reader(infile)
    for row in reader:
      list.append(row)
      # input()
  return list


def get_today():
  """
  Returns todays date in yyyy-mm-dd format.
  """
  return date.today()

def get_wfh(current_date):
  """
  Get the wfh for current_date.
  """
  ret_users = []
  file_path = os.path.abspath(__file__)
  file_path = file_path[:file_path.rfind("/")]
  # print(file_path)
  json_details = load_json(file_path + "/config.json")
  # print(file_path + "/config.json")
  if current_date in json_details:
    ret_users = json_details[current_date]

  return ret_users

def add_wfh(user_name, current_date):
  """
  Add new wfh for current_date.
  """
  ret_users = []
  file_path = os.path.abspath(__file__)
  file_path = file_path[:file_path.rfind("/")]
  # print(file_path)
  json_details = load_json(file_path + "/config.json")
  if current_date in json_details:
    if user_name not in json_details[current_date]:
      json_details[current_date].append(user_name)
  else:
    json_details[current_date] = [user_name]
  # pprint(json_details)
  write_json_to_file(json_details, file_path + "/config.json")


def get_wfh_config():
  """
  Get wfh config.
  """
  ret = {}
  file_path = os.path.abspath(__file__)
  file_path = file_path[:file_path.rfind("/")]
  ret = load_json(file_path + "/config.json")
  return ret


def remove_wfh(user_name, current_date):
  """
  Remove wfh for current_date.
  """
  ret_users = []
  file_path = os.path.abspath(__file__)
  file_path = file_path[:file_path.rfind("/")]
  json_details = load_json(file_path + "/config.json")
  if current_date in json_details:
    if user_name in json_details[current_date]:
      json_details[current_date].remove(user_name)
    # else:
    #   print("User not added for `{}`.".format(current_date))
  # else:
  #   print("User not added for `{}`.".format(current_date))
  write_json_to_file(json_details, file_path + "/config.json")

def write_json_to_file(dict_temp, out_file="/tmp/tmp.json"):
  """
  Write the json to a file.
  :param dict_temp: Dictionary to write
  :param out_file: output file
  """
  # print("Writing json to file: [ %s ]" % out_file)
  with open(out_file,"w") as f:
    f.write(json.dumps(dict_temp))

def main():
  """
  Main function
  """
  print("This is a module. Do not call this directly.")


if __name__ == '__main__':
  """
  Main guard.
  """
  main()
