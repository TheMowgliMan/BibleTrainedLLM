export PYTHONPATH="$1:$1/scripts/py:$PYTHONPATH"
. $HOME/.venvs/$2/bin/activate
which python3
python3 main.py
deactivate
