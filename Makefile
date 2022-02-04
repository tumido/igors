all: fonts

debug:
	kstart5 --ontop okular test.png

run:
	pipenv run python display.py
	okular test.png

fonts:
	mkdir -p fonts
	wget https://use.fontawesome.com/releases/v6.0.0-beta3/fontawesome-free-6.0.0-beta3-desktop.zip
	unzip -d fonts fontawesome-free-6.0.0-beta3-desktop.zip "fontawesome-free-6.0.0-beta3-desktop/otfs/*"
	rm fontawesome-free-6.0.0-beta3-desktop.zip

	wget -O noto.zip https://fonts.google.com/download\?family\=Noto%20Sans
	unzip -d fonts noto.zip "NotoSans*.ttf"
	rm noto.zip

	wget -O bitter.zip https://www.huertatipografica.com/free_download/144
	unzip -d fonts bitter.zip "Bitter*.ttf"
	rm bitter.zip
