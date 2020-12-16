#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color
printf "${GREEN}Fetching latest pcgs_scraper version..."

URL=$(curl -s "https://api.github.com/repos/ryanamannion/pcgs_scraper/releases/latest" | \
	python3 -c "import sys, json; print(json.load(sys.stdin)['tarball_url'])")

VERSION=$(echo $URL | awk -F'/' '{print $NF}')
SAVE_DIR="pcgs_scraper-releases"
FILE="pcgs_scraper-${VERSION}.tar.gz"
FULL="${SAVE_DIR}/${FILE}"

printf " Latest: ${VERSION}${NC}\n"

if [ ! -d "./${SAVE_DIR}" ]; then
	printf "${GREEN}First time, creating ${SAVE_DIR}... "
	mkdir "$SAVE_DIR"
	printf "Done${NC}\n"
fi

if [ ! -f "$FULL" ]; then
	printf "${GREEN}Saving ${VERSION} to ${FULL}... "
	cd $SAVE_DIR
	wget --quiet --output-document=$FILE $URL
	printf "Done${NC}\n"
	cd ..
	exit
else
	printf "${RED}${FULL} already exists, exiting${NC}\n"
	exit
fi
