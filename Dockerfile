FROM pytorch/pytorch:1.5.1-cuda10.1-cudnn7-runtime

RUN apt-get update
RUN apt-get install -y libsm6 libxrender-dev libxext6 libglib2.0-0 freeglut3-dev gcc g++ curl wget

COPY ./scripts/download_trained_model.sh .

RUN chmod +x ./download_trained_model.sh

RUN sh ./download_trained_model.sh

RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
ENV NODE_VERSION=12.6.0
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN node --version
RUN npm --version

RUN pip install --upgrade pip

ENV FORCE_CUDA = "1"
COPY requirements.txt .

#install python package
RUN pip install -r requirements.txt

COPY ./static/package.json ./static/package.json

RUN cd ./static && npm install

COPY . .

EXPOSE 80

CMD python app.py
