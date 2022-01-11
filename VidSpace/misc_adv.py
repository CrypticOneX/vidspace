from VidSpace import app, mysql
from VidSpace.client import get_subscribers
from VidSpace.utils.get_subs import is_subscriber
from flask import redirect, url_for, render_template, session


@app.route('/channel/<id>', methods = ['GET'])
def channel(id):
    global subscription_status
    cur = mysql.connection.cursor()
    result = cur.execute('''SELECT * FROM channels WHERE _chid = %s''', [id])
    if result > 0:
        channel = cur.fetchone()
        cur_videos = mysql.connection.cursor()
        cur_videos.execute('''SELECT * FROM videos WHERE uploaded_by = %s''', [channel['_chid']])
        videos = cur_videos.fetchall()
        subscription_status = None
        if 'logged_in' in session and 'user_id' in session:
            subscription_status = is_subscriber(session['user_id'], channel['_chid'])

        return render_template('channel.html', channel=channel, videos=videos, subscription_status=subscription_status, title=channel['name'])

    return redirect(url_for('not_found'))

@app.route('/channel/about/<id>')
def channel_about(id):
    cur = mysql.connection.cursor()
    result = cur.execute('''SELECT * FROM channels WHERE _chid = %s''', [id])
    if result > 0:
        channel = cur.fetchone()
        vid_cur = mysql.connection.cursor()
        vid_cur.execute('''SELECT * FROM videos WHERE uploaded_by = %s''', [channel['_chid']])
        no_of_videos = vid_cur.rowcount
        total_subscribers = get_subscribers(id)
        print(total_subscribers)
        return render_template('about.html', channel=channel, no_of_videos = no_of_videos, total_subscribers=total_subscribers, title=channel['name'])

    return redirect(url_for('not_found'))
