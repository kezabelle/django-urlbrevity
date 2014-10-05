rm -rf .coverage
python  -B -tt -W once setup.py test -a "--cov ."
