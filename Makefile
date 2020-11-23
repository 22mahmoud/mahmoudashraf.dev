# config
SRC 	:= src
DIST 	:= dist
NAME 	:= 'Mahmoud Ashraf'
URL 	:= 'https://mahmoudashraf.dev'

gen:
	[ -d $(DIST) ] || mkdir $(DIST)
	./ssg5/ssg5 $(SRC) $(DIST) $(NAME) $(URL)

watch:
	find . -type f ! -path '${SRC}/.*' | entr -d $(MAKE) gen

server:
	python3 -m http.server -d $(DIST)

dev:
	$(MAKE) clean -j2 watch server

clean:
	rm -rf dist

update:
	git pull origin master
	git submodule foreach git pull origin master
	$(MAKE) clean gen

.PHONY : gen clean watch server dev update