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

build:
	docker build --network host --no-cache --rm -t ${IMG_NAME} .

remove-image:
	docker rmi ${IMG_NAME}

run:
	$(COMMAND_RUN)
			
