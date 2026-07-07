# set base image Lambda python3.8
FROM public.ecr.aws/lambda/python:3.8

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# Copy function code
COPY . ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]


# this is a backup for fuseki Dockerfile to be copped to another file in case we need to run fuseki project on the server

# FROM stain/jena-fuseki

# RUN apt-get update; \
#     apt-get install -y --no-install-recommends procps