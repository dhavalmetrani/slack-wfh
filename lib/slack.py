import os

from slack import WebClient

ENV_SLACK_TOKEN = "AMIBOT_SLACK_TOKEN"
DEFAULT_CHANNEL = "#misc-wfh"
DEFAULT_MESSAGE = "Test message."
DEFAULT_USER    = "amibot"
OK              = "ok"
ERROR           = "error"

class Slack:
  def __init__(self):
    """
    Init function
    """
    self._token = os.getenv(ENV_SLACK_TOKEN, None)
    if None is self._token:
      err_msg = "Could not get {} from env.".format(ENV_SLACK_TOKEN)
      raise Exception(err_msg)
    self._sc = WebClient(token=self._token)

  def message_channel(self, channel=DEFAULT_CHANNEL, text=DEFAULT_MESSAGE, username=DEFAULT_USER, link_names=True):
    """
    Send message to specified slack channel.
    """
    # result = self._sc.api_call("chat.postMessage", channel_id=channel_id, text=text, username=username)
    result = self._sc.chat_postMessage(channel=channel,
                                       text=text,
                                       username=DEFAULT_USER,
                                       link_names=True)
    if result[OK] == False:
      err_msg = "Error from Slack: {err}".format(err=result[ERROR])
      raise Exception(err_msg)


def main():
  """
  This is the main function
  """
  s = Slack()
  s.message_channel(text="This is a sampel test esaegve,")

  pass


if __name__ == '__main__':
  """
  Main guard.
  """
  main()
