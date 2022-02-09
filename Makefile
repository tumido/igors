all: fonts

debug:
	kstart5 --ontop okular test.png

run:
	pipenv run python display.py
	okular test.png

.PHONY: fonts
fonts:
	mkdir -p fonts
	wget -O fonts/MaterialIconsOutlined-Regular.otf https://raw.githubusercontent.com/google/material-design-icons/master/font/MaterialIconsOutlined-Regular.otf

	wget -O noto.zip https://fonts.google.com/download\?family\=Noto%20Sans
	unzip -d fonts noto.zip "NotoSans*.ttf"
	rm noto.zip

	wget -O bitter.zip https://www.huertatipografica.com/free_download/144
	unzip -d fonts bitter.zip "Bitter*.ttf"
	rm bitter.zip

.node:
	wget https://unofficial-builds.nodejs.org/download/release/v16.9.1/node-v16.9.1-linux-armv6l.tar.gz
	tar -xzf node-v16.9.1-linux-armv6l.tar.gz
	rm node-v16.9.1-linux-armv6l.tar.gz
	cd node-v6.2.1-linux-armv6l/
	sudo cp -R * /usr/local/
