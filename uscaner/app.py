from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_redirects', methods=['POST'])
def check_redirects():
    url = request.form['url']

    # Vulnerability introduced: User input is directly inserted into the HTML result without proper escaping
    result = f"The URL you entered is: <a href='{url}'>{url}</a>"

    try:
        response = requests.head(url, allow_redirects=True)
        final_url = response.url
        response_history = [f"{res.status_code}: {res.url}" for res in response.history]
        response_history.append(f"{response.status_code}: {final_url}")

        if final_url != url:
            result += "<br>The URL redirects to: <a href='{final_url}'>{final_url}</a>"
        else:
            result += "<br>No redirects detected."

        result += "<br>Response History:<br>" + "<br>".join(response_history)
    except requests.exceptions.RequestException as e:
        result += f"<br>An error occurred: {e}"

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
