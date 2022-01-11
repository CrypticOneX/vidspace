from VidSpace import app, mysql
from VidSpace.utils.generate import generate_string
from VidSpace.utils.auth import authentication_required
from VidSpace.utils.get_subs import get_subscribers
from VidSpace.utils.get_reaction import get_dislikes, get_likes
from flask import session, request, jsonify, render_template


@app.route('/subscribe', methods=['GET', 'POST'])
@authentication_required
def subscribe():
    user_id = session['user_id']
    channel_id = request.form['subscribe']
    if channel_id == '':
        error = "Channel not found"
    ch_cur = mysql.connection.cursor()
    ch_cur.execute('''SELECT  * FROM channels WHERE owner = %s''', [user_id])
    ch_data = ch_cur.fetchone()

    # if ch_data['owner'] == user_id:
    #     return 'You cannot subscribe this channel'

    # check already subscribed or not

    sub = mysql.connection.cursor()
    res = sub.execute('''SELECT * FROM subscribers WHERE _uid = %s AND _chid = %s''', [user_id, channel_id])

    if res > 0:
        remove_sub = mysql.connection.cursor()
        remove_sub.execute('''DELETE FROM subscribers WHERE _uid = %s AND _chid = %s''', [user_id, channel_id])
        mysql.connection.commit()
        remove_sub.close()
        no_of_subs = get_subscribers(channel_id)
        return jsonify({"status": 0, "subscriber": no_of_subs})
    else:
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO subscribers (_uid, _chid) VALUES (%s, %s)''', (user_id, channel_id))
        mysql.connection.commit()
        cur.close()
        no_of_subs = get_subscribers(channel_id)
    return jsonify({"status": 1, "subscriber": no_of_subs})


@app.route('/like', methods=['GET', 'POST'])
@authentication_required
def like():
    user_id = session['user_id']
    video_id = request.form['video_id']

    cur_check = mysql.connection.cursor()
    result = cur_check.execute('''SELECT * FROM reaction WHERE _uid = %s AND _video_id = %s''', (user_id, video_id))

    if result > 0:
        cur = mysql.connection.cursor()
        cur.execute('''DELETE FROM reaction WHERE _uid = %s and _video_id = %s''', (user_id, video_id))
        mysql.connection.commit()
        cur.close()
        no_of_likes = get_likes(video_id)
        no_of_dislikes = get_dislikes(video_id)
        return jsonify({'status': 0, 'likes': no_of_likes, 'dislikes': no_of_dislikes})
    else:
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO reaction (_video_id, _uid, likes, dislikes) VALUES (%s, %s, %s, %s)''',
                    (video_id, user_id, 1, 0))
        mysql.connection.commit()
        cur.close()
        no_of_likes = get_likes(video_id)
        no_of_dislikes = get_dislikes(video_id)
        return jsonify({'status': 1, 'likes': no_of_likes, 'dislikes': no_of_dislikes})


@app.route('/dislike', methods=['GET', 'POST'])
@authentication_required
def dislike():
    user_id = session['user_id']
    video_id = request.form['video_id']

    cur_check = mysql.connection.cursor()
    result = cur_check.execute('''SELECT * FROM reaction WHERE _uid = %s AND _video_id = %s''', (user_id, video_id))

    if result > 0:
        cur = mysql.connection.cursor()
        cur.execute('''DELETE FROM reaction WHERE _uid = %s and _video_id = %s''', (user_id, video_id))
        mysql.connection.commit()
        cur.close()
        no_of_likes = get_likes(video_id)
        no_of_dislikes = get_dislikes(video_id)
        return jsonify({'status': 1, 'dislikes': no_of_dislikes, 'likes': no_of_likes})
    else:
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO reaction (_video_id, _uid, likes, dislikes) VALUES (%s, %s, %s, %s)''',
                    (video_id, user_id, 0, 1))
        mysql.connection.commit()
        cur.close()
        no_of_likes = get_likes(video_id)
        no_of_dislikes = get_dislikes(video_id)
        return jsonify({'status': 1, 'dislikes': no_of_dislikes, 'likes': no_of_likes})


@app.route('/library')
@authentication_required
def library():
    videos = []
    cur = mysql.connection.cursor()
    data = cur.execute('''SELECT * FROM watch_history WHERE _uid = %s''', [session['user_id']])
    if data > 0:
        history = cur.fetchall()
        for his in history:
            videos_cur = mysql.connection.cursor()
            videos_cur.execute('''SELECT * FROM videos WHERE _video_id = %s''', [his['_video_id']])
            videos += videos_cur.fetchall()
        return render_template('library.html', videos=videos)
    return render_template('library.html', error="No History")


# playlists


@app.route('/playlist/create-playlist', methods=['GET', 'POST'])
@authentication_required
def create_playlist():
    playlist_id = generate_string(40)
    _uid = session['user_id']
    name = request.form['pname']
    privacy = request.form['privacy']
    video_id = request.form['video_id']
    cur = mysql.connection.cursor()
    cur.execute('''INSERT INTO playlists (playlist_id, name, _uid, _video_id, privacy) VALUES (%s, %s, %s, %s)''',
                (playlist_id, name, _uid, video_id, privacy))
    mysql.connection.commit()
    cur.close()
    return '1'


@app.route('/playlist/delete-playlist/<id>')
@authentication_required
def delete_playlist(id):
    cur = mysql.connection.cursor()
    cur.execute('''DELETE FROM playlists WHERE playlist_id = %s''', [id])
    mysql.connection.commit()
    cur.close()
    return '1'


@app.route('/playlists')
def playlists():
    _uid = request.form['_uid']
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM playlists WHERE _uid = %s AND privacy = 0''', [_uid])
    mysql.connection.commit()
    cur.close()
    return '1'


# @app.route('/comments', methods=['GET', 'POST'])
# @authentication_required
# def comment():
#     comment = request.form['comment-text']
#     video_id = request.form['video-id']
#     uid = session['user_id']
#     cur = mysql.connection.cursor()
#     cur.execute('''INSERT INTO comments (_uid, _video_id, comment) VALUES (%s, %s, %s)''', (uid, video_id, comment))
#     mysql.connection.commit()
#     cur.close()
#     comment = mysql.connection.cursor()
#     comment.execute('''SELECT * FROM comments WHERE _video_id = %s''', [video_id])
#     comments = comment.fetchall()
#     return jsonify({'comments': comments})
