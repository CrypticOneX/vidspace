import os
from VidSpace import app, mysql
from flask import url_for, redirect


@app.route('/delete/<video_id>')
def delete_video(video_id):
    cur = mysql.connection.cursor()
    data = cur.execute('''SELECT * FROM videos WHERE _video_id = %s''', [video_id])
    if data < 0:
        return redirect('studio')
    else:
        data = cur.fetchone()
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], data['video_uri']))
        except FileNotFoundError:
            print("File not found!")
        except TypeError:
            print("Forgive Me!")

        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], data['thumb_uri']))
        except FileNotFoundError:
            print("File not found!")
        except TypeError:
            print("Forgive Me!")

        cur.execute('''DELETE FROM videos WHERE _video_id = %s''', [video_id])
        mysql.connection.commit()
    return redirect(url_for('studio'))