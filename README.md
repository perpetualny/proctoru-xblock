# ProctorU XBlock
ProctorU XBlock Installation Guide:


1. Clone xblock repo from https://github.com/ProctorU/xBlock.git to x block directory.
2. Change directory to where you have cloned ProctorU XBlock.
3. To install requirements for ProctorU XBlock. Do not upgrade dependencies this will break the installation
		
		pip install -r --no-deps requirements.txt

4. Open “ lms/envs/common.py “, " cms/env/common.py " and put “proctoru” in installed apps.
5. Run migrations for proctorU XBlock:
		
    	python manage.py lms migrate proctoru --settings=aws

6. Add "PROCTORU_TOKEN" and "PROCTORU_API" in both lms and cms `envs/common.py` file and restart edxapp

		PROCTORU_TOKEN = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
		PROCTORU_API = "x.proctoru.com"
		
7. Restart edxapp

		sudo /edx/bin/supervisorctl restart all
