import happybase
import datetime

DEBUG = True
HBASE_SERVER = 'ec2-107-20-14-178.compute-1.amazonaws.com'
TABLE_TWEET = 'tweet'
TABLE_USER = 'user'
# TWEET_FAMILY = ["time", "text", "user", "re"]
# TWEET_QUALIFIER = ["time", "text", "uid", "is_re", "o_tid"]
# USER_FAMILY = ["count", "re"]
# USER_QUALIFIER = ["count", "re_uids"]

# changing the time format from "2013-10-02+00:00:00" in URL
# to "Wed Oct 02 00:00:00 +0000 2013" in JSON
def time_format(time):
  t = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
  return t.strftime("%a %b %d %H:%M:%S +d{4} %Y")

# get q2 from hbase
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

# get q3 from hbase
def q3_hbase(userid_min, userid_max):
  conn = happybase.Connection(HBASE_SERVER)

  if DEBUG == True:
    print "Established connection. HBase tables: "
    print conn.tables()

  table = conn.table(TABLE_USER)
  results = []
  filter_string = "(RowFilter (>=, 'binary:" + userid_min + "') AND RowFilter (<=, 'binary:" + userid_max + "'))"

  for key, value in table.scan(columns=["count:count"],filter=filter_string):
    result = value['count:count']   # TODO: check the type of result, add them later
    results.append(result)

  #results = list(set(results))
  #results.sort()
  result_string = ""

  for i in range(0, len(results)):
    result_string += results[i]+'\n'  # TODO: need modification

  return result_string

# get q4 from hbase
def q4_hbase(userid):
  conn = happybase.Connection(HBASE_SERVER)

  if DEBUG == True:
    print "Established connection. HBase tables: "
    print conn.tables()

  table = conn.table(TABLE_USER)
  result = row(userid, columns=["re":"re_uids"]) # TODO: check the type of result, extract the list
  result_list = result[userid]["re":"re_uids"]

  #results = list(set(results))
  result_list.sort()
  result_string = ""

  for i in range(0, len(result_list)):
    result_string += result_list[i]+'\n'

  return result_string
