# Developer Notes

We use miniconda to manage the project environment, and poetry to manage the packages.

You will need to install both system tools prior to development.

## Environment Creation

Create the conda environment:
```shell
conda env create -f environment.yml
conda activate metarstation
```
Install the project Python packages (including the local package as an editable install):
```shell
poetry install
```

## Environment Variables

We use a `.env` file to load project specific environment variables at runtime, however some variables (such as Prefect related) need to be present before the application loads.

So we set them at the time of activating the conda environment, but we need to deactivate then reactivate the environment after setting for them to take proper effect.

```shell
conda env config vars set -n metarstation DATA_DIR="$(pwd)/data"
conda env config vars set -n metarstation PREFECT__LOGGING__EXTRA_LOGGERS="[\"metar_station\"]"
conda env config vars set -n metarstation PREFECT__FLOWS__CHECKPOINTING="true"
conda env config vars set -n metarstation PIP_CONFIG_FILE="$(pwd)/pip.conf"
conda deactivate
conda activate metarstation
```

To list any variables you may have, run `conda env config vars list -n metarstation`.

To set environment variables, run `conda env config vars set -n metarstation my_var=value`.

To unset the environment variable, run `conda env config vars unset -n metarstation my_var`.

https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#setting-environment-variables

## Install Jupyter Kernel
Install kernel for access by central JupyterLab instance:

```shell
python -m ipykernel install --user --name metarstation --display-name "METAR Station"
```
