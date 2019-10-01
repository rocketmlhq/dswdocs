## Data Science Workbench

RocketML Data Science Workbench (DSW) is a machine learning (ML) platform to enable Data scientists and ML engineers across your organization to easily build and deploy ML solutions at scale. 


## Projects
Data Scientist's work is done in a project, which is a collection of workspaces and project files.

### Project Files
For every user, workbench creates a folder in your corporate S3 bucket. For every project created by a user, DSW creates a project folder in the user folder. Project folder name can be accessed from Projects Details page. All workspaces created in this project will have read-write access to project files folder. Any data, code, results can be stored in project files folder for future use.


## Workspaces
Workspaces are single-node and multi-node CPU/GPU clusters with **read-only** access to data sources and **read-write** access to project files.

### Single Node

### Multi-node HPC cluster

### Compute Options

#### CPU
- c5.large
- c5.xlarge
- c5.2xlarge
- c5.4xlarge
- c5.9xlarge
- c5.12xlarge
- c5.18xlarge
- c5.24xlarge


#### GPU (Coming Soon)
- p3.2xlarge
- p3.8xlarge
- p3.16xlarge
- g4dn.xlarge
- g4dn.2xlarge
- g4dn.4xlarge
- g4dn.8xlarge
- g4dn.16xlarge

## Data Sources

### Corporate Data Sources

### RocketML Seed Data

### Data on Internet

## JupyterLab Documentation
[![Jupyter Lab Documentation](http://img.youtube.com/vi/y30fs6kg6fc/0.jpg)](https://www.youtube.com/playlist?list=PLUrHeD2K9CmlEvyGGgZXDf_u31MvLB_Lg "Jupyter Lab Documentation")

## Installing pip, conda, and apt packages

### Open a terminal
![terminal](https://tljh.jupyter.org/en/latest/_images/new-terminal-button2.png)

### Installing pip packages
Open a terminal and install the package at the terminal
`pip install --user <package name>`

### Installing conda packages
Open a terminal and install the package at the terminal
`sudo /opt/conda/bin/conda install -c <channel> <package name>`

## Support or Contact

Having trouble with Data Science Workbench? or [Contact us](email:info@rocketml.net) and we’ll help you sort it out.
