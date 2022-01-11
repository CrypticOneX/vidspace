from VidSpace import app, mysql
from flask import session, jsonify, request, redirect, url_for


@app.route('/comment/<video_id>', methods=['GET', 'POST'])
def comment(video_id):
    cur = mysql.connection.cursor()
    cur.execute('''select first_name, _video_id, comment, date from comments, users where users._uid = comments._uid and _video_id =  %s''', [video_id])
    comments = cur.fetchall()
    if request.method == 'POST':
        if 'logged_in' in session:
            user_id = session['user_id']
            comment_text = request.json['comment']
            add_comment_cursor = mysql.connection.cursor()
            add_comment_cursor.execute('''INSERT INTO comments (_uid, _video_id, comment) VALUES (%s, %s, %s)''', (user_id, video_id, comment_text))
            mysql.connection.commit()
            add_comment_cursor.execute('''select first_name, _video_id, comment, date from comments, users where users._uid = comments._uid and _video_id =  %s''', [video_id])
            new_comments = add_comment_cursor.fetchall()
            return jsonify({'comments': new_comments})
        else:
            return redirect(url_for('signin'))

    return jsonify({'comments': comments})
