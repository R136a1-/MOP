#!/bin/bash
cd payload
tar cLf ../payload.tar ./*
cd ..

if [ -e "payload.tar" ]; then
    gzip payload.tar

    if [ -e "payload.tar.gz" ]; then
        cat decompress.sh payload.tar.gz > selfextract.bsx
    else
        echo "payload.tar.gz does not exist"
        exit 1
    fi
else
    echo "payload.tar does not exist"
    exit 1
fi

echo "selfextract.bsx created"
exit 0
