import happybase
import datetime

DEBUG = True
HBASE_SERVER = 'ec2-107-20-14-178.compute-1.amazonaws.com'
TABLE_TWEET = 'tweet'
TABLE_USER = 'user'
FAMILY = ["time", "text", "user", "re"]
QUALIFIER = ["time", "text", "uid", "is_re", "o_tid"]

# changing the time format from "2013-10-02+00:00:00" in URL
# to "Wed Oct 02 00:00:00 +0000 2013" in JSON
def time_format(time):
  t = datetime.datetime.strptime(time, "%Y-%m-%d+%H:%M:%S")
  return t.strftime("%a %b %d %H:%M:%S +d{4} %Y")

def q2_hbase(time):
  conn = happybase.Connection(HBASE_SERVER)

  if DEBUG == True:
    print "Established connection. HBase tables: "
    print conn.tables()

  table = conn.table(TABLE_TWEET)
  results = []
  filter_string = "SingleColumnValueFilter ('time', 'time', =, 'regexstring:" + time_format(time) + "')"

  for key, value in table.scan(columns=["text:text"],filter=filter_string):
    result = key + ":" + value['text:text']
    results.append(result)

  results = list(set(results))
  results.sort()
  result_string = ""

  for i in range(0, len(results)):
    result_string += results[i]+'\n'

  return result_string
