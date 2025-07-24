from flask import Flask, render_template_string, request
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# HTML + CSS Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Resume Based Job Search</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f8ff;
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #2c3e50;
        }
        .upload-box {
            background: white;
            padding: 30px;
            border-radius: 10px;
            max-width: 600px;
            margin: 20px auto;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        input[type="file"] {
            width: 100%;
            padding: 20px;
            border: 2px dashed #ccc;
            border-radius: 10px;
            margin-bottom: 20px;
            background: #fafafa;
        }
        input[type="submit"] {
            background: #1e90ff;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }
        .results {
            max-width: 700px;
            margin: 30px auto;
            background: #ffffff;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .results h2 {
            color: #2c3e50;
        }
        .job-links a {
            display: block;
            margin: 10px 0;
            font-weight: bold;
            color: #0077cc;
            text-decoration: none;
        }
        .job-links a:hover {
            color: #0055aa;
        }
    </style>
</head>
<body>
    <h1>📄 Resume Based Job Search</h1>
    <div class="upload-box">
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="resume" required><br>
            <input type="submit" value="Upload Resume">
        </form>
    </div>
    {% if job_title %}
    <div class="results">
        <h2>🎯 Detected Role: <span style="color:#1e90ff">{{ job_title }}</span></h2>
        <div class="job-links">
            <h3>🔍 Explore Jobs for "{{ job_title }}"</h3>
            {% for name, link in job_links.items() %}
                <a href="{{ link }}" target="_blank">{{ name }}</a>
            {% endfor %}
        </div>
    </div>
    {% endif %}
</body>
</html>
"""

# Helper to generate search links
def generate_job_links(role):
    role_query = role.replace(" ", "+")
    return {
        "LinkedIn": f"https://www.linkedin.com/jobs/search/?keywords={role_query}",
        "Google Jobs": f"https://www.google.com/search?q={role_query}+jobs+in+India",
        "Naukri": f"https://www.naukri.com/{role_query}-jobs",
        "Indeed": f"https://in.indeed.com/jobs?q={role_query}",
        "MonsterIndia": f"https://www.monsterindia.com/search/{role_query}-jobs"
    }

@app.route('/', methods=['GET', 'POST'])
def home():
    job_title = None
    job_links = {}
    if request.method == 'POST':
        file = request.files['resume']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Simulated extraction: You can replace this with actual parser
            job_title = "Python Developer"  # ← Replace with actual logic later
            job_links = generate_job_links(job_title)

    return render_template_string(HTML_TEMPLATE, job_title=job_title, job_links=job_links)

if __name__ == '__main__':
    app.run(debug=True)

