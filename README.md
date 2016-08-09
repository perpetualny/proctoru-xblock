# ProctorU XBlock
ProctorU XBlock Installation Guide:


1. Clone xblock repo from https://github.com/ProctorU/xBlock.git to x block directory.
2. Change directory to where you have cloned ProctorU XBlock.
3. To install requirements for ProctorU XBlock.
		
		pip install --no-deps xBlock/	
		pip install -r --no-deps xBlock/requirements.txt

4. Open “ lms/envs/common.py “, " cms/env/common.py " and put “proctoru” in installed apps.
5. Run migrations for proctorU XBlock:
		
    	python manage.py lms migrate proctoru --settings=aws


6. To add authentication token for ProctorU.
		
		a. Login to admin panel of lms.
		b. Click Open ProctorUAuthToken.
		c. Click on Add new ProctorUAuthToken.
		d. Add a token 6647b4ba-5da5-44a1-bc8e-ead386a66215
		e. save the token
