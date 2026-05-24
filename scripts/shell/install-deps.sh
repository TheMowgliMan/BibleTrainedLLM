rm -f .deps-obtained
mkdir -p $HOME/.venvs

python3 -m venv $HOME/.venvs/$1
$HOME/.venvs/$1/bin/python3 --version

export PYTHONPATH=$HOME/.venvs/$1/bin
echo $PYTHONPATH

. $HOME/.venvs/$1/bin/activate

which pip3

pip3 install transformers
pip3 install torch
pip3 install sentencepiece

deactivate

touch .deps-obtained
