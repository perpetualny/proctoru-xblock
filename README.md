# ProctorU XBlock
ProctorU XBlock Installation Guide:


1. Clone xblock repo from https://github.com/ProctorU/xBlock.git to x block directory.
2. Change directory to where you have cloned ProctorU XBlock.
3. Change directory to ProctorU.
4. To install requirements for ProctorU XBlock.
			
		pip install -r requirements.txt

5. Open “ lms/envs/common.py “ and put “proctoru” in installed apps.
6. Run migrations for proctorU XBlock:
		
    	python manage.py lms migrate proctoru --settings=aws


7. To add authentication token for ProctorU.
		
		Login to admin panel of django.
		Click Open ProctorUAuthToken.
		Click on Add new ProctorUAuthToken.
		Copy-Paste Your AuthToken to and Save.
