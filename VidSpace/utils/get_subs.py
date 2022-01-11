from VidSpace import mysql


def get_subscribers(channel_id):
    no_subs = mysql.connection.cursor()
    no_subs.execute('''SELECT * FROM subscribers WHERE _chid = %s''', [channel_id])
    no_of_subs = no_subs.fetchall()
    no_subs = len(no_of_subs)

    return no_subs


def is_subscriber(user_id, channel_id):
    cur = mysql.connection.cursor()
    result = cur.execute('''SELECT * FROM subscribers WHERE _uid = %s AND _chid = %s''', (user_id, channel_id))

    if result > 0:
        return True
    return False
