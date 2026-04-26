import subprocess

# تشغيل البوت
subprocess.Popen(["python", "main.py"])

# تشغيل الواجهة
subprocess.run([
    "streamlit", "run", "dashboard.py",
    "--server.port", "8080",
    "--server.address", "0.0.0.0"
])
