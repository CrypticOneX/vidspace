from VidSpace import mysql


def get_likes(video_id):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM reaction WHERE _video_id = %s AND likes = 1''', [video_id])
    result = cur.fetchall()
    return len(result)


def get_dislikes(video_id):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM reaction WHERE _video_id = %s AND dislikes = 1''', [video_id])
    result = cur.fetchall()
    return len(result)
