# ProctorU XBlock
ProctorU XBlock Installation Guide:


1. Clone xblock repo from https://github.com/ProctorU/xBlock.git to x block directory.
2. Change directory to where you have cloned ProctorU XBlock.
3. To install requirements for ProctorU XBlock.
			
		pip install -r requirements.txt

4. Open “ lms/envs/common.py “ and put “proctoru” in installed apps.
5. Run migrations for proctorU XBlock:
		
    	python manage.py lms migrate proctoru --settings=aws


6. To add authentication token for ProctorU.
		
		a. Login to admin panel of django.
		b. Click Open ProctorUAuthToken.
		c. Click on Add new ProctorUAuthToken.
		d. Copy-Paste Your AuthToken to and Save.
