# build with
# docker build -t openmc_dagmc_conda_test .

FROM mcr.microsoft.com/vscode/devcontainers/miniconda:0-3

RUN apt-get --allow-releaseinfo-change update
RUN apt-get --yes update && apt-get --yes upgrade

# check conda-forge for packages first
RUN conda config --add channels conda-forge
RUN conda config --set channel_priority strict

# using mamba to avoid tempest error in conda install dagmc
RUN conda install mamba -y

RUN mamba install gxx -y

RUN mamba install cmake -y

RUN mamba install make -y

RUN mamba install binutils -y

RUN mamba install -c conda-forge dagmc=3.2.2 -y

# RUN git clone --single-branch --branch develop --depth 1 https://github.com/openmc-dev/openmc.git
# this branch is upto date with develop, but contains material.from_library
RUN git clone --single-branch --branch adding_material_from_library --depth 1 https://github.com/shimwell/openmc.git

RUN cd openmc && \
    mkdir build && \
    cd build && \
    cmake -Doptimize=on \
          -Ddagmc=ON \
          -DHDF5_PREFER_PARALLEL=off ..  && \
    make -j && \
    make -j install && \
    cd /openmc/ && \
    pip install .