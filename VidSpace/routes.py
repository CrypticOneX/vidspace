import os
from VidSpace import app, mysql
from flask import render_template, request, session, url_for, flash, redirect
from VidSpace.forms.users import Signup
from passlib.hash import bcrypt
from VidSpace.utils.generate import generate_string, generate_file_name
from VidSpace.utils.video_validator import allowed_file, allowed_thumb_file
from VidSpace.utils.auth import authentication_required
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip
from datetime import timedelta
from VidSpace.utils.get_subs import get_subscribers, is_subscriber
from VidSpace.utils.get_reaction import get_likes, get_dislikes


@app.route('/', methods=['GET'])
def home():
    if 'video_meta' in session:
        session.pop('video_meta')
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM videos ORDER BY views''')
    videos = cur.fetchall()
    return render_template('home.html', videos=videos, title="Home")


@app.route('/reg-success')
def reg_success():
    return "Hello World"


# create account
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Signup(request.form)
    if request.method == 'POST':
        _uid = generate_string(26)
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = bcrypt.encrypt(str(form.password.data))
        phone = form.phone.data
        ip_address = request.remote_addr
        ua = request.headers.get('User-Agent')

        _chid = generate_string(28)
        channel_name = first_name + last_name

        cur = mysql.connection.cursor()
        # execute for user
        cur.execute('''INSERT INTO users (_uid, first_name, last_name, email, password, phone, ip_address, user_agent) VALUES (%s, %s, %s, 
        %s, %s, %s, %s, %s)''', (_uid, first_name, last_name, email, password, phone, ip_address, ua))

        # execute for channel creation
        cur.execute('''INSERT INTO channels (_chid, name, owner) VALUES (%s, %s, %s)''', (_chid, channel_name, _uid))

        mysql.connection.commit()

        # close connection
        cur.close()

        flash("Verification link has been sent to your email!", "success")

        return redirect(url_for('reg_success'))

    return render_template('signup.html', form=form, title="Sign-up")


# login
@app.route('/sign-in', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        data = cur.execute('''SELECT * FROM users WHERE email = %s OR phone = %s''', [username, username])

        if data > 0:
            user_data = cur.fetchone()
            if bcrypt.verify(password, user_data['password']):
                chhanel_cur = mysql.connection.cursor()
                channel_data = cur.execute('''SELECT * FROM channels WHERE owner = %s''', [user_data['_uid']])
                fetched_channel_data = cur.fetchone()
                session['logged_in'] = True
                session['user_id'] = user_data['_uid']
                session['channel_id'] = fetched_channel_data['_chid']
                session['email'] = user_data['email']
                session['first_name'] = user_data['first_name']
                session['avatar'] = fetched_channel_data['logo']
                return redirect(url_for('home'))
            else:
                error = "Invalid email and password"
                return render_template('signin.html', error=error)
        else:
            error = "Invalid email and password"
            return render_template('signin.html', error=error, title="Sign-in")

    return render_template('signin.html', title="Sign-in")


# check user signed in or not


@app.route('/signout')
@authentication_required
def signout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/studio')
@authentication_required
def studio():
    if 'video_meta' in session:
        session.pop('video_meta')

    channel_id = session['channel_id']
    cur = mysql.connection.cursor()
    data = cur.execute('''SELECT * FROM videos WHERE uploaded_by = %s''', [channel_id])
    if data < 1:
        return render_template('studio.html', message='No Videos Found!', title="Creator Studio")
    else:
        videos = cur.fetchall()
    return render_template('studio.html', videos=videos, title="Creator Studio")


@app.route('/upload', methods=['GET', 'POST'])
@authentication_required
def upload():
    if 'video_meta' in session:
        session.pop('video_meta')
    video_id = generate_string(11)
    if request.method == 'POST':
        privacy = request.form['privacy']
        # check if post request has file part
        if 'video-file' not in request.files:
            flash('Not any files selected!', 'danger')
            return redirect(url_for('upload'))
        file = request.files['video-file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(url_for('upload'))
        if file and allowed_file(file.filename):
            ext = generate_file_name(file.filename)
            # fname = generate_string(11) + '.' + generate_file_name(file.filename)
            fname = video_id + '.' + ext
            filename = secure_filename(fname)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            clip = VideoFileClip(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            video_meta = {
                "filename": fname,
                "video_id": video_id,
                "privacy": privacy,
                "duration": clip.duration
            }
            session['video_meta'] = video_meta
            return redirect(url_for('publish'))
        return render_template('upload-video.html', title="Upload Video")

    return render_template('upload-video.html', title="Upload Video")


@app.route('/publish', methods=['GET', 'POST'])
@authentication_required
def publish():
    global fname
    if 'video_meta' not in session:
        return redirect(url_for('upload'))

    video_meta = session['video_meta']
    channel_id = session['channel_id']
    videofile = video_meta['filename']
    video_id = video_meta['video_id']
    privacy = video_meta['privacy']
    duration = video_meta['duration']
    video_duration = str(timedelta(seconds=int(duration)))
    pdata = 1

    if privacy == 'Private':
        pdata = 0
    elif privacy == 'Unlisted':
        pdata = 2

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        tags = request.form['tags']
        file = request.files['thumbnail']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(url_for('publish'))
        if file and allowed_thumb_file(file.filename):
            ext = generate_file_name(file.filename)
            # fname = generate_string(11) + '.' + generate_file_name(file.filename)
            fname = video_id + '.' + ext
            filename = secure_filename(fname)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO videos (_video_id, title, description, tags, video_uri, thumb_uri, privacy, 
        uploaded_by, duration) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (video_id, title, description, tags, videofile, fname, pdata, channel_id,
                     video_duration))
        mysql.connection.commit()
        cur.close()
        session.pop('video_meta')
        return redirect(url_for('upload'))
    return render_template('upload-video2.html', title="Upload Video")

@app.route('/search')
def search():
    search_query = request.args.get('search')
    search_string = "%" + search_query + "%"
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM videos WHERE title like %s OR description like %s OR tags like %s''', [search_string, search_query, search_query])
    video_results = cur.fetchall()

    channel_cur = mysql.connection.cursor()
    channel_cur.execute('''SELECT * FROM channels WHERE name like %s OR category like %s''', [search_string, search_string])
    channel_results = channel_cur.fetchall()

    return render_template('search_results.html', channel_results=channel_results, video_results=video_results, title=search_query)


@app.route('/watch', methods=['GET', 'POST'])
def watch():
    global subscription_status, playlists
    video_id = request.args.get('v', default='*', type=str)
    if video_id == '*':
        error = "Video not found"
        return render_template('player.html', error=error)

    cur = mysql.connection.cursor()
    data = cur.execute('''SELECT * FROM videos WHERE _video_id = %s''', [video_id])

    if data < 0:
        error = "Video doesn't exists or deleted!"
        return render_template('player.html', error=error)

    # # check subscription
    # if session['user_id']:
    #     user_id = session['user_id']
    #     ch_cur = mysql.connection.cursor()
    #     ch_cur.execute('''SELECT  * FROM channels WHERE owner = %s''', [user_id])
    #     ch_data = ch_cur.fetchone()

    video = cur.fetchone()
    add_views = mysql.connection.cursor()
    add_views.execute('''UPDATE videos SET views = %s WHERE _video_id = %s''',
                      [str(video['views'] + 1), video['_video_id']])
    mysql.connection.commit()
    ch_cur = mysql.connection.cursor()
    ch_cur.execute('''SELECT * FROM channels WHERE _chid = %s''', [video['uploaded_by']])
    channel = ch_cur.fetchone()
    up_next_cursor = mysql.connection.cursor()
    up_next_q = up_next_cursor.execute('''SELECT * FROM videos WHERE _video_id <> %s''', [video['_video_id']])
    up_next = up_next_cursor.fetchall()
    no_subs = get_subscribers(channel['_chid'])
    subscription_status = False
    playlists = None
    if 'logged_in' in session and 'user_id' in session:
        subscription_status = is_subscriber(session['user_id'], channel['_chid'])
        # get playlists
        pl = mysql.connection.cursor()
        pl.execute('''SELECT * FROM playlists WHERE _uid = %s''', [session['user_id']])
        playlists = pl.fetchall()
        # add to watch history
        wh = mysql.connection.cursor()
        wh.execute('''INSERT INTO watch_history (_video_id, _uid) VALUES (%s, %s)''',
                   (video['_video_id'], session['user_id']))
        mysql.connection.commit()
        wh.close()
    # print(playlists)
    # get comments
    # comments = get_comments(video['_video_id'])

    likes = get_likes(video['_video_id'])
    dislikes = get_dislikes(video['_video_id'])
    return render_template('player.html', video=video, channel=channel, up_next=up_next, no_subs=no_subs,
                           likes=likes, dislikes=dislikes, subscription_status=subscription_status, playlists=playlists,
                           title=video['title'])


@app.route('/subscription')
@authentication_required
def subscription():
    cur = mysql.connection.cursor()
    result_len = cur.execute(
        '''SELECT * FROM channels where _chid IN (select _chid from subscribers, users where users._uid = subscribers._uid and users._uid = %s) ''',
        [session['user_id']])
    if result_len > 0:
        channels = cur.fetchall()
        return render_template('subscription-page.html', channels=channels, title="Subscription")
    else:
        error = 'No channels has been subscribed'
    return render_template('subscription-page.html', error=error, title="Subscription")


@app.route('/settings', methods=['GET', 'POST'])
@authentication_required
def settings():
    global fname
    _uid = session['user_id']
    user_cur = mysql.connection.cursor()
    user_cur.execute('''SELECT * FROM users WHERE _uid = %s''', [_uid])
    user_data = user_cur.fetchone()

    channel_cur = mysql.connection.cursor()
    channel_cur.execute('''SELECT * FROM channels WHERE owner = %s''', [_uid])
    channel_data = channel_cur.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        about = request.form['about']
        category = request.form['category']

        file = request.files['logo']
        # if user does not select file, browser also
        # submit an empty part without filename

        logo_id = generate_string(40)
        if file and allowed_thumb_file(file.filename):
            ext = generate_file_name(file.filename)
            # fname = generate_string(11) + '.' + generate_file_name(file.filename)
            fname = logo_id + '.' + ext
            filename = secure_filename(fname)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        update_cursor = mysql.connection.cursor()
        update_cursor.execute('''UPDATE channels SET name = %s, about = %s, category = %s, logo = %s WHERE _chid = %s''',
                                                (name, about, category, fname, channel_data['_chid']))
        mysql.connection.commit()
        update_cursor.close()

        return render_template('settings.html', user=user_data, channel=channel_data, msg="Account details updated successfully!", title="Settings")

    return render_template('settings.html', user = user_data, channel = channel_data, title="Settings")
