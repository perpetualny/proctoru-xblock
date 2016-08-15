ProctorU xBlock
===============

1. [About](https://github.com/perpetualny/proctoru-xblock#open-edx)
	1. [Open edX](https://github.com/perpetualny/proctoru-xblock#open-edx)
	2. [ProctorU](https://github.com/perpetualny/proctoru-xblock#proctoru)
	3. [ProctorU xBlock](https://github.com/perpetualny/proctoru-xblock#proctoru)
2. [Architecture](https://github.com/perpetualny/proctoru-xblock#architecture)
3. [Todo](https://github.com/perpetualny/proctoru-xblock#to-do)
4. [Pre-Installation Requirements](https://github.com/perpetualny/proctoru-xblock#pre-installation-requirements)
5. [Installation](https://github.com/perpetualny/proctoru-xblock#installation)
6. [License](https://github.com/perpetualny/proctoru-xblock#license)


Open edX
--------
[Open edX](http://open.edx.org) is an open-source learning management system  that powers hundereds of MOOC platforms including [edX.org](https://edx.org) and  [FunMOOC](https://www.fun-mooc.fr/), catering to tens of millions of online learners globally Learn more about Open edX and its components on the [Open edX website](https://open.edx.org/about-open-edx)

ProctorU
--------

[ProctorU](http://www.proctoru.com/) is a leading online proctoring service that allows students to take proctored exams online from anywhere using a webcam and a high speed internet connection, and allows institutions to maintain academic integrity in their online education programs.

Learn more about how ProctorU how ProctorU [ works ](http://www.proctoru.com/howitworks.php)

This software is an xBlock (extension to Open edX courseware) that enables proctoring on any Open edX instance using [ProctorU](http://www.proctoru.com/).

It can be used to schedule a proctoring session for exams within an Open edX course.  Follow the below instructions to install the xBlock on an Open edX instance.You will need to register your institution with ProctorU to get an authentication token.

![](http://i.imgur.com/rCTCfju.png)

![](http://i.imgur.com/Tr5Nlq4.jpg)

To test out a clickable prototype, click _[here](https://projects.invisionapp.com/share/V76EZPRNU#/screens)_


Architecture
-----------------


To Do
-------
	[ ] English language support
	[ ] Minor bug-fixes

Pre-Installation Requirements
--------------------------------------
	1. Open edX Dogwood release
	2. ProctorU Authentication Token
	3. Django ( > v1.8 )




Installation
-------------

1. Clone xblock repo from https://github.com/perpetualny/proctoru-xblock.git to xBlock directory.
2. Change directory to where you have cloned ProctorU XBlock.
3. To install requirements for ProctorU XBlock. **Do not upgrade dependencies** this will break the Open edX installation

        pip install -r --no-deps requirements.txt

4. Open “ lms/envs/common.py “, " cms/env/common.py " and put “proctoru” in installed apps.
5. Run migrations for proctorU XBlock:

        python manage.py lms migrate proctoru --settings=aws

6. Add "PROCTORU_TOKEN" and "PROCTORU_API" in both lms and cms `envs/common.py` file and restart edxapp

        PROCTORU_TOKEN = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        PROCTORU_API = "x.proctoru.com"

7. Restart edxapp

        sudo /edx/bin/supervisorctl restart all



License
-------
This xblock is open sourced under GNU AGPL v3 license, check the [LICENSE](https://github.com/perpetualny/proctoru-xblock/blob/master/LICENSE) file for detailed information.


The xBlock was developed by [ Perpetual Learning ](http://learning.perpetualny.com/) in collaboration with [ FunMOOC](https://www.fun-mooc.fr/) and [ ProctorU ](http://www.proctoru.com/). For more information contact [info@perpetualny.com](mailto:info@perpetualny.com)
