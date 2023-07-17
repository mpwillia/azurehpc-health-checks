#!/bin/bash
VERSION="$1"
WORKING_DIR="$2"

mkdir -p $WORKING_DIR
pushd $WORKING_DIR

OUTPUT="az-nhc-$VERSION"
if [[ -d $OUTPUT ]]; then
    exit 0
fi

if [[ -f $OUTPUT.tar.gz ]]; then
    rm $OUTPUT.tar.gz
elif [[ -f $OUTPUT.zip ]]; then
    rm $OUTPUT.zip
fi

if [[ ${VERSION,,} -eq "main" ]]; then
    wget -O $OUTPUT.zip https://github.com/Azure/azurehpc-health-checks/archive/refs/heads/main.zip
    unzip $OUTPUT.zip
else
    wget -O "$OUTPUT.tar.gz" https://github.com/Azure/azurehpc-health-checks/archive/refs/tags/v$VERSION.tar.gz 
    tar -xzf $OUTPUT.tar.gz
fi