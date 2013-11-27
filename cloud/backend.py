import happybase
import datetime
import json

HBASE_SERVER = 'ec2-54-227-120-43.compute-1.amazonaws.com'
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
    converted_value = (json.dumps(value["text:text"]))[1:-1]
    converted_value = converted_value.replace('/','\/')
    converted_value = converted_value.replace('{','\\u007b')
    converted_value = converted_value.replace('}','\\u007d')

    result_string += key + ':' + converted_value +'\n'

  return result_string

# pass q3 queries to hbase
def q3_hbase(userid_min, userid_max):
  conn = happybase.Connection(HBASE_SERVER)
  table = conn.table(TABLE_USER)

  uid_min = "{:0>20d}".format(long(str(userid_min)))
  uid_max = "{:0>20d}".format(long(str(userid_max)) + 1L)

  sum = 0
  for key, value in table.scan(row_start=uid_min, row_stop=uid_max, columns=["count:count"]):
    result = value['count:count']
    sum += int(result.encode('hex'), 16)

  return str(sum)+'\n'

# pass q4 queries to hbase
def q4_hbase(userid):
  conn = happybase.Connection(HBASE_SERVER)
  table = conn.table(TABLE_USER)

  uid = "{:0>20d}".format(long(str(userid)))
  result = table.row(uid, columns=["re:re_uids"])

  results = []
  if result:
    results = result["re:re_uids"].split('\n')

  results = results[:-1]
  results = sorted(results, key=lambda x: int(x))

  result_string = ""
  for i in range(0, len(results)):
    result_string += results[i]+'\n'

  return result_string
