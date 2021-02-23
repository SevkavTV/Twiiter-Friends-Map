
'''
Lab 2, Task 3. Archakov Vsevolod.
'''
from flask import Flask, render_template, request
from twitter import *

app = Flask('Twitter Friends Map')


@app.route('/')
def input_data():
    return render_template('input.html')


@app.route('/friends_map', methods=["POST"])
def create_map():
    try:
        nickname = request.form.get('nickname')
        token = request.form.get('token')

        if not nickname or not token:
            return render_template('failure.html')

        twitter_friends_json = twitter_get_friends_json(
            nickname=nickname, token=token)
        print('successfull request')
        friends_data = generate_friends_data(twitter_friends_json)
        print('got locations')
        generate_map(friends_data)
        print('generated map')

        return render_template('twitter_map.html')

    except:
        return render_template('failure.html')


if __name__ == '__main__':
    app.run(debug=False)
