FROM continuumio/miniconda3

WORKDIR /app

RUN git clone https://github.com/GuilhermeMBP/alpha-beta-CROWN.git
RUN git clone https://github.com/GuilhermeMBP/VFRN4UAVs.git
RUN git clone https://github.com/GuilhermeMBP/gym-pybullet-drones.git

WORKDIR /app/alpha-beta-CROWN

#clone auto_LiRPA
RUN git clone https://github.com/Verified-Intelligence/auto_LiRPA.git 
WORKDIR /app/alpha-beta-CROWN/auto_LiRPA 
RUN git checkout 2553832b5a5bbfe643b694458867ebd1dbdece65

WORKDIR /app/alpha-beta-CROWN

SHELL ["/bin/bash", "--login", "-c"]

# Remove the old environment, if necessary.
RUN conda deactivate; conda env remove --name alpha-beta-crown
# install all dependents into the alpha-beta-crown environment
RUN conda env create -f complete_verifier/environment.yaml --name alpha-beta-crown

WORKDIR /app/gym-pybullet-drones

RUN conda create -n drones python=3.10

RUN /bin/bash -c "conda init"

RUN /bin/bash -c "source ~/.bashrc && conda activate drones && pip3 install --upgrade pip && pip3 install -e ."

RUN conda create -n pynever python=3.11

RUN /bin/bash -c "source ~/.bashrc && conda activate drones && pip3 install pynever==0.1.1a4"

RUN conda init bash

CMD /bin/bash