import happybase
import datetime

DEBUG = True
HBASE_SERVER = 'ec2-23-23-39-31.compute-1.amazonaws.com'
TABLE_TWEET = 'tweet'
TABLE_USER = 'user'
#FAMILY = ["time", "text", "user", "re"]
#QUALIFIER = ["time", "text", "uid", "is_re", "o_tid"]

# changing the time format from "2013-10-02+00:00:00" in URL
# to "Wed Oct 02 00:00:00 +0000 2013" in JSON
def time_format(time):
  t = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
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

def time_format(time):
  t = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
  return t.strftime("%a %b %d %H:%M:%S +d{4} %Y")

def q3_hbase(userid_min, userid_max):
  conn = happybase.Connection(HBASE_SERVER)

  if DEBUG == True:
    print "Established connection. HBase tables: "
    print conn.tables()

  table = conn.table(TABLE_USER)
  results = []
  filter_string = "(RowFilter (>=, 'binary:" + str(userid_min) + "') AND RowFilter (<=, 'binary:" + str(userid_max) + "'))"

  for key, value in table.scan(columns=["count:count"],filter=filter_string):
    result = value['count:count']
    results.append(result)

  sum = 0
  for i in range(0, len(results)):
    sum += int(results[i].encode('hex'), 16)

  return str(sum)

def q4_hbase(userid):
  conn = happybase.Connection(HBASE_SERVER)

  if DEBUG == True:
    print "Established connection. HBase tables: "
    print conn.tables()

  table = conn.table(TABLE_USER)
  result = table.row(str(userid), columns=["re:re_uids"])

  result_string = ""
  if result:
    result_string = result["re:re_uids"]
  
  # TODO: sort by uid

  return result_string

