# WRI India Decarbonization Workshop 

Create a Conda Environment

Follow the instructions to install Anaconda: 
macOS: https://docs.anaconda.com/anaconda/install/mac-os/
Windows: https://docs.anaconda.com/anaconda/install/windows/
Linux: https://docs.anaconda.com/anaconda/install/linux/

To avoid incompatibility problems between packages, create a specific Anaconda environment named <myenv> with python version 3.8 for GridPath.

`conda create -n <myenv> python=3.8`

You can find instructions on how to manage Anaconda environments on this website: 

https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

The command to list the environments available in your Anaconda installation is conda env list. You can activate an existing environment named <myenv> by typing conda activate <myenv> in the terminal.

Install Jupyter Notebook by invoking the following command: pip3 install jupyter (Jupyter Notebook is a Python interface).

matplotlib is the plotting library utilized by the visualization functionalities. The command to install matplotlib  is conda install conda-forge::matplotlib 

## Download Workshop Files

Download the folder in  containing the .csv input files corresponding to the state you want to install https://drive.google.com/drive/u/0/folders/1zTkNsWSxBnIoFxwPWBdd1wDqfUPV91bR

You now have the path to the downloaded input files as <path_to_csvs> and the folder with the .csv input files is <folder_name>.

Download the tutorial materials for the workshop from the GitHub repository typing in the terminal `git clone https://github.com/cetlab-ucsb/wri-workshop.git` from the project folder `<path_to_project>`

Install GridPath v0.14.1

The porting software is for GridPath v0.14.1. GridPath repository in GitHub https://github.com/blue-marble/gridpath

The instructions for installing GridPath are in this GitHub main repository. GridPath has multiple releases available, and each one of them has a unique tag. The link to the version tag v0.14.1 is https://github.com/blue-marble/gridpath/releases/tag/v0.14.1

Navigate (cd) to the directory where you want to install GridPath, for instance:
cd /Users/<user_name>/Desktop/<project_name>/

The command to clone the GridPath release tagged as v0.14.1 is: 

git clone https://github.com/blue-marble/gridpath.git --branch v0.14.1

Navigate to the <path_to_gridpath> directory cd gridpath and install GridPath with the command pip install .


Install Open-Source Solver

GridPath needs an open-source solver software (cbc) to solve the optimization problem. To install cbc enter this command in the terminal after activating your Anaconda environment conda install -c conda-forge pyomo coincbc


Run GriPath from Terminal

Create a database using GridPath. You need to know the path to GridPath files <path_to_gridpath> and give the path <path_to_database> where you want to create the database. Give a name to the database <database_name.db>. The database has a .db extension.

python <path_to_gridpath>/gridpath/db/create_database.py --database <path_to_database>/<database_name.db>

Import the .csv from their folder <path_to_csvs>/<folder_name> into the database <database_name.db> with the following command,

python <path_to_gridpath>/gridpath/db/utilities/port_csvs_to_db.py --database <path_to_database>/<database_name.db> --csv_location <path_to_csvs>/<folder_name>

Import the scenarios on scenarios.csv file from the folder <path_to_csvs>/<folder_name> with the following command,

python <path_to_gridpath>/gridpath/db/utilities/scenario.py --database <path_to_database>/<database_name.db> --csv_path <path_to_csvs>/<folder_name>/scenarios.csv

Use GridPath to solve a specific scenario <scenario_name> in the file scenarios.csv. The columns on that file are the scenarios and the header is the scenario name. Solve scenario <scenario_name> with the following command:

python <path_to_gridpath>/gridpath/gridpath/run_end_to_end.py --database <path_to_database>/<database_name.db> --scenario <scenario_name>

