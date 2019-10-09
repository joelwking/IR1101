#
#     Copyright (c) 2019 World Wide Technology, LLC
#     All rights reserved.
#
#     author: joel.king@wwt.com (@joelwking)
#     written:  1 October 2019
#
#     usage:
#
FROM arm64v8/alpine:3.7

MAINTAINER @joelwking

COPY qemu-aarch64-static /usr/bin
RUN apk add --no-cache python
#
RUN mkdir -p /app
WORKDIR /app
COPY *.py /app
#
# Execution
#
CMD ["python2.7", "hello.py"]
