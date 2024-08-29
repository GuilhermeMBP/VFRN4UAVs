FROM continuumio/miniconda3

RUN git clone https://github.com/Verified-Intelligence/alpha-beta-CROWN.git

WORKDIR /alpha-beta-CROWN

#clone auto_LiRPA
RUN git clone https://github.com/Verified-Intelligence/auto_LiRPA.git

SHELL ["/bin/bash", "--login", "-c"]

# Remove the old environment, if necessary.
RUN conda deactivate; conda env remove --name alpha-beta-crown
# install all dependents into the alpha-beta-crown environment
RUN conda env create -f complete_verifier/environment.yaml --name alpha-beta-crown

RUN conda init bash