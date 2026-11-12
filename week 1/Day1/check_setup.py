"""Week 01 setup check — run this before Session 1.

How to run (from the folder where you saved this file):
    Mac:      python3 check_setup.py
    Windows:  python check_setup.py

Every line should show [OK]. If something shows [FIX], follow the hint
or post a screenshot of the whole output in the help channel.
"""

import shutil
import subprocess
import sys
import urllib.request

OK = "[OK] "
FIX = "[FIX]"
results = []


def report(passed, label, detail="", hint=""):
    results.append(passed)
    print(f"{OK if passed else FIX} {label}{(' — ' + detail) if detail else ''}")
    if not passed and hint:
        print(f"       -> {hint}")


def run(cmd):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return out.returncode, (out.stdout or out.stderr).strip()
    except (OSError, subprocess.TimeoutExpired):
        return 1, ""


print("\nWeek 01 setup check\n" + "-" * 40)

# 1. Python version
v = sys.version_info
report(v >= (3, 12), "Python 3.12 or newer", f"you have {v.major}.{v.minor}.{v.micro}",
       "Install the latest Python 3 from https://www.python.org/downloads/ "
       "(Windows: tick 'Add python.exe to PATH').")

# 2. venv module
try:
    import venv  # noqa: F401
    report(True, "Virtual environments (venv) available")
except ImportError:
    report(False, "Virtual environments (venv) available", "",
           "On Linux run: sudo apt install python3-venv")

# 3. pip
code, out = run([sys.executable, "-m", "pip", "--version"])
report(code == 0, "pip installed", out.split(" from ")[0] if code == 0 else "",
       f"Run: {sys.executable} -m ensurepip --upgrade")

# 4. Git installed
git = shutil.which("git")
code, out = run(["git", "--version"]) if git else (1, "")
report(code == 0, "Git installed", out,
       "Install Git from https://git-scm.com/downloads, then open a NEW terminal.")

# 5. Git identity
if git:
    _, name = run(["git", "config", "--global", "user.name"])
    _, email = run(["git", "config", "--global", "user.email"])
    report(bool(name and email), "Git name & email configured",
           f"{name} <{email}>" if name and email else "",
           'Run: git config --global user.name "Your Name"   and   '
           'git config --global user.email "you@example.com"')

# 6. VS Code command (helpful, not required)
code_cmd = shutil.which("code")
if code_cmd:
    report(True, "VS Code 'code' command available")
else:
    print("[--]  VS Code 'code' command not found (optional). In VS Code open the Command Palette "
          "and run: Shell Command: Install 'code' command in PATH (Mac).")

# 7. Can reach GitHub
try:
    urllib.request.urlopen("https://github.com", timeout=10)
    report(True, "Internet access to github.com")
except Exception as error:  # noqa: BLE001 — any network failure means the same thing here
    report(False, "Internet access to github.com", str(error)[:60],
           "Check your internet connection, VPN or firewall.")

print("-" * 40)
if all(results):
    print("All set! You're ready for Session 1.\n")
else:
    print(f"{results.count(False)} item(s) need fixing — see the hints above.\n")
