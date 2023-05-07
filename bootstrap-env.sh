echo
echo "Creating virtual environment .venv"
echo "---------------------------------------------------------------------------"
py -m venv .venv
echo
echo "Activating the new created virtual environment"
echo "---------------------------------------------------------------------------"
source .venv/Scripts/activate
echo
echo "Upgrading pip in .venv"
echo "---------------------------------------------------------------------------"
.venv/Scripts/py -m pip install --upgrade pip
echo
echo "Installing this project in editable mode [with test, doc, dev extra]"
echo "---------------------------------------------------------------------------"
pip install -e ".[test, doc, dev]"
echo
echo "ALL DONE; Good luck with your work!"
