# build with

# docker build -t idom_reaction_chamber .

FROM mcr.microsoft.com/vscode/devcontainers/miniconda:0-3


RUN conda install -c conda-forge mamba

RUN mamba install -c conda-forge -y "openmc=0.13.0=*nompi*"

RUN pip install openmc_data

RUN download_nndc 

ENV OPENMC_CROSS_SECTIONS=/nndc-b7.1-hdf5/endfb71_hdf5/cross_sections.xml