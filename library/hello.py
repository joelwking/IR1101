#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     Copyright (c) 2019 World Wide Technology, LLC
#     All rights reserved.
#
#     author: joel.king@wwt.com (@joelwking)

import time
import random

i = 0
while True:
    print('The current time is {}'.format(time.asctime()))
    i += 1
    time.sleep(random.randint(0,60))
    if i > 100:
        print('Exiting!')
        exit(0)