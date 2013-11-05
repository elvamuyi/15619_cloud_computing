import MySQLdb

db = MySQLdb.connect(user='user', passwd="password", db="twitter_test")

c=db.cursor()
c.execute("""SELECT tid, text FROM tweets WHERE create_at = %s""", ('2013-10-10 10:10:10'))

r = c.fetchall() # r is a tuple containing all the results

r # ((111111L, 'Hello world!'), (222222L, 'Bye world!'))

