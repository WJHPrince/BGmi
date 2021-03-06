BGmi
====
BGmi is a cli tool for subscribed bangumi.

|travis| |pypi|

====
TODO
====
+ Download bangumi by file format, file size, etc.

=======
Feature
=======
+ Subscribe/unsubscribe bangumi
+ Bangumi calendar
+ Bangumi episode informatdon
+ Download bangumi by subtitle group
+ Web page to view all subscribed bangumi
+ RSS feed for uTorrent

.. image:: https://raw.githubusercontent.com/RicterZ/BGmi/master/images/bgmi.png
    :alt: BGmi
    :align: center
.. image:: https://raw.githubusercontent.com/RicterZ/BGmi/master/images/bgmi_http.png
    :alt: BGmi HTTP Service
    :align: center

============
Installation
============
For **Mac OS X / Linux**:

.. code-block:: bash

    git clone https://github.com/RicterZ/BGmi
    cd BGmi
    python setup.py install

Or use pip:

.. code-block:: bash

    pip install bgmi

For **Windows**: BGmi does not support Windows now.  

=============
Usage of bgmi
=============

Show bangumi calendar:

.. code-block:: bash

    bgmi cal all


Subscribe bangumi:

.. code-block:: bash

    bgmi add "Re：從零開始的異世界生活" "暗殺教室Ⅱ" "線上遊戲的老婆不可能是女生？" "在下坂本，有何貴幹？" "JoJo的奇妙冒險 不滅鑽石"


Unsubscribe bangumi:

.. code-block:: bash

    bgmi delete --name "暗殺教室Ⅱ"


Update bangumi database which locates at ~/.bgmi/bangumi.db defaultly:

.. code-block:: bash

    bgmi update --download


Set up the bangumi subtitle group filter and fetch entries:

.. code-block:: bash

    bgmi filter "線上遊戲的老婆不可能是女生？" "KNA,惡魔島"
    bgmi fetch "線上遊戲的老婆不可能是女生？"


Show BGmi configure and modify it:

.. code-block:: bash

    bgmi config
    bgmi config MAX_PAGE 3

Fields of configure file:

+ `DMHY_URL`: url of dmhy mirror
+ `BGMI_SAVE_PATH`: path which save the bangumi
+ `DOWNLOAD_DELEGATE`: which ways used to download bangumi (aria2, aria2-rpc, xunlei)
+ `MAX_PAGE`: the max page of fetching bangumi info
+ `BGMI_TMP_PATH`: just a temporary path
+ `ARIA2_PATH`: path of the aria2c binary
+ `ARIA2_RPC_URL`: rpc url of aria2c deamon
+ `BGMI_LX_PATH`: path of xunlei-lixian binary

==================
Usage of bgmi_http
==================

Start BGmi HTTP Service bind on `0.0.0.0:8888`:

.. code-block:: bash

    bgmi_http --port=8888 --address=0.0.0.0

Configure tornado with nginx:

.. code-block:: bash

    server {
        listen 80;
        root /var/www/html/bangumi;
        autoindex on;
        charset utf8;
        server_name bangumi.example.com;

        location /bangumi {
            alias /var/www/html/bangumi;
        }

        location / {
            # reverse proxy to tornado listened port.
            proxy_pass http://127.0.0.1:8888;
        }
    }

Of cause you can use `yaaw <https://github.com/binux/yaaw/>`_ to manage download items if you use aria2c to download bangumi.

.. code-block:: bash

    ...
    location /bgmi_admin {
        auth_basic "BGmi admin (yaaw)";
        auth_basic_user_file /etc/nginx/htpasswd;
        alias /var/www/html/yaaw/;
    }

    location /jsonrpc {
        # aria2c listened port
        proxy_pass http://127.0.0.1:6800;
    }
    ...


=======
License
=======
The MIT License (MIT)

Copyright (c) 2016 Ricter Zheng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

.. |travis| image:: https://travis-ci.org/RicterZ/BGmi.svg?branch=master
   :target: https://travis-ci.org/RicterZ/BGmi

.. |pypi| image:: https://img.shields.io/pypi/v/bgmi.svg
   :target: https://pypi.python.org/pypi/bgmi
