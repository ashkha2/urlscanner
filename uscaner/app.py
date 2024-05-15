from flask import Flask, render_template, request, redirect, url_for
import requests
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_redirects', methods=['POST'])
def check_redirects():
    url = request.form['url']

    # Vulnerability introduced: Command Injection
    try:
        # Instead of using requests to fetch the URL, execute it as a shell command
        result = subprocess.check_output(["curl", url], shell=False, text=True)

        # Display the output
        result += f"<br>The output of the command is: {result}"
    except subprocess.CalledProcessError as e:
        result = f"An error occurred: {e}"

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
