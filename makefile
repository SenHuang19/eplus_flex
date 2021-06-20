IMG_NAME=eplus_flex

COMMAND_RUN=docker run \
	  --name ${IMG_NAME} \
	  --detach=false \
	  --rm \
	  -i \
	  -t \
	  --network host \
	  -v `pwd`:/home/developer/fmu/eplus/run \
	  ${IMG_NAME} /bin/bash -c "cd eplus/run && energyplus -w ../weather/${wea}.epw -r ../model/ASHRAE901_OfficeLarge_STD2019_${city}.idf"

COMMAND_RUN_python=docker run \
	  --name python2 \
	  --detach=false \
	  --rm \
	  -i \
	  -t \
	  --network host \
	  -v `pwd`:/home/developer/ \
	  python2 /bin/bash -c "cd /home/developer && python server.py config/${city}.config ${start} ${dev}"



build_eplus:
	docker build -f Dockerfile_eplus --network host --no-cache --rm -t ${IMG_NAME} .

run_eplus:
	$(COMMAND_RUN)
			
build_python:
	docker build -f Dockerfile_python2 --network host --no-cache --rm -t python2 .
	
run_python:
	$(COMMAND_RUN_python)	

