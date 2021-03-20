PIP=pip
PYTHON=python

init:
	$(PIP) install -r requirements.txt

download:
	mkdir -p ./dataset/drkg
	curl -f https://dgl-data.s3-us-west-2.amazonaws.com/dataset/DRKG/drkg.tar.gz -o ./dataset/drkg.tar.gz
	tar xvzf ./dataset/drkg.tar.gz -C ./dataset/drkg

test:
	nosetests tests