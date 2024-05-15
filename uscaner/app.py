from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_redirects', methods=['POST'])
def check_redirects():
    url = request.form['url']
    try:
        response = requests.head(url, allow_redirects=True)
        final_url = response.url
        response_history = [f"{res.status_code}: {res.url}" for res in response.history]
        response_history.append(f"{response.status_code}: {final_url}")

        if final_url != url:
            result = f"The URL redirects to: {final_url}"
        else:
            result = "No redirects detected."

        result += "<br><br>Response History:<br>" + "<br>".join(response_history)
    except requests.exceptions.RequestException as e:
        result = f"An error occurred: {e}"

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
