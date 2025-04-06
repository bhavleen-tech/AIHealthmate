from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

ALLOWED_USERS = {"Kiratmeet Singh", "Bhavleen Kaur", "Anushka Tripathi"}

HTML_FORM = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Healthmate Premium Login</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gradient-to-r from-pink-200 to-purple-300 min-h-screen flex items-center justify-center font-sans">
    <div class="bg-white p-10 rounded-lg shadow-lg w-full max-w-md">
        <h1 class="text-3xl font-bold text-center text-pink-700 mb-6">🌟 AI Healthmate Premium Login</h1>
        {% if error %}
            <div class="bg-red-100 text-red-700 p-3 rounded mb-4 text-sm">{{ error }}</div>
        {% endif %}
        <form method="POST">
            <label class="block mb-2 text-sm font-medium text-gray-700">Full Name</label>
            <input type="text" name="name" required class="w-full p-2 border rounded mb-4">

            <label class="block mb-2 text-sm font-medium text-gray-700">Age</label>
            <input type="number" name="age" required class="w-full p-2 border rounded mb-4">

            <label class="block mb-2 text-sm font-medium text-gray-700">Gender</label>
            <select name="gender" required class="w-full p-2 border rounded mb-4">
                <option value="">Select Gender</option>
                <option>Male</option>
                <option>Female</option>
                <option>Other</option>
            </select>

            <label class="block mb-2 text-sm font-medium text-gray-700">Password</label>
            <input type="password" name="password" required class="w-full p-2 border rounded mb-6">

            <button type="submit" class="bg-pink-600 text-white px-4 py-2 rounded hover:bg-pink-700 w-full">Login</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name in ALLOWED_USERS:
            return redirect("http://127.0.0.1:3000/premium.html")
        else:
            return render_template_string(HTML_FORM, error="❌ Access Denied. This Premium Feature is Restricted.")
    return render_template_string(HTML_FORM, error=None)

if __name__ == '__main__':
    app.run(host="127.0.0.6", port=5001, debug=True)
