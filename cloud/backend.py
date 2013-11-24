import happybase
import datetime

HBASE_SERVER = 'ec2-54-227-109-12.compute-1.amazonaws.com'
TABLE_TWEET = 'tweet'
TABLE_USER = 'user'
TABLE_TIME = 'time'

# changing the time format from "2013-10-02+00:00:00" in URL
# to "Wed Oct 02 00:00:00 +0000 2013" in JSON
def time_format(time):
  t = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
  return t.strftime("%a %b %d %H:%M:%S +0000 %Y")

# pass q2 queries to hbase
def q2_hbase(time):
  conn = happybase.Connection(HBASE_SERVER)
  table1 = conn.table(TABLE_TIME)
  result = table1.row(time_format(time), columns=["tweet:tid"])

  row_keys = []
  if result:
    row_keys = result["tweet:tid"].split('\n')

  row_keys = row_keys[:-1]
  row_keys = sorted(row_keys, key=lambda x: int(x))

  table2 = conn.table(TABLE_TWEET)
  result_string = ""
  for key, value in table2.rows(row_keys, columns=["text:text"]):
    result_string += key + ':' + value["text:text"] +'\n'

  return result_string

# pass q3 queries to hbase
def q3_hbase(userid_min, userid_max):
  conn = happybase.Connection(HBASE_SERVER)
  table = conn.table(TABLE_USER)
  results = []
  filter_string = "(RowFilter (>=, 'binary:" + str(userid_min) + "') AND RowFilter (<=, 'binary:" + str(userid_max) + "'))"

  for key, value in table.scan(columns=["count:count"],filter=filter_string):
    result = value['count:count']
    results.append(result)

  sum = 0
  for i in range(0, len(results)):
    sum += int(results[i].encode('hex'), 16)

  return str(sum)+'\n'

# pass q4 queries to hbase
def q4_hbase(userid):
  conn = happybase.Connection(HBASE_SERVER)
  table = conn.table(TABLE_USER)
  result = table.row(str(userid), columns=["re:re_uids"])

  results = []
  result_string = ""
  if result:
    results = result["re:re_uids"].split('\n')

  results = results[:-1]
  results = sorted(results, key=lambda x: int(x))

  for i in range(0, len(results)):
    result_string += results[i]+'\n'

  return result_string
