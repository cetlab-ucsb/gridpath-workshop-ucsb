# GridPath Workshop

## Pre-Setup Instructions
Before running the model, download the `state_model` folder from Google Drive and save it to your desktop. The path should be `~/Desktop/state_model`.

Google Drive link: [Download Folder](https://drive.google.com/drive/folders/1GnN0Eq1uCrRrRReP_92QB3Tz0MLzliB-)

### Setting up Conda

#### Install Anaconda
Anaconda is a package manager and environment manager for Python/R. It simplifies managing libraries and creating isolated environments. Follow the installation instructions based on your OS:

- [macOS](https://docs.anaconda.com/anaconda/install/mac-os/)
- [Windows](https://docs.anaconda.com/anaconda/install/windows/)
- [Linux](https://docs.anaconda.com/anaconda/install/linux/)

### Terminal Access
Use the terminal to interact with Conda:

- **macOS**: Open Terminal via Spotlight or under Applications > Utilities.
- **Linux**: Open Terminal from the applications menu or by pressing `Ctrl + Alt + T`.
- **Windows**: Open "Anaconda Prompt" from the Start menu.

### Creating a Conda Environment
In the terminal, create a new environment named `<myenv>` with Python version 3.9 for GridPath:

```bash
conda create -n <myenv> python=3.9
```
Conda offers various tools to manage environments, including activating, deactivating, listing, and removing them as needed. For detailed information on managing Conda environments, refer to this guide. For example, you can view all existing environments in Conda by running: 
```bash
conda env list
```
### Setting up model requirements in terminal
#### Activating the Conda environment
To activate the environment by run the following in the terminal:
```bash
conda activate <myenv>
```
Once activated, the environment name will appear at the beginning of the terminal prompt in parenthesis - any subsequent package installations will take place within this environment.
#### Installing open-source solver
GridPath needs an open-source solver software (cbc) to solve the optimization problem. To install cbc:

**For Mac users:** run the following command to set up the cbc solver: 
```bash
conda install -c conda-forge pyomo coincbc
```

**For Windows PC users:**
1. Windows PC users need to copy the cbc.exe file to the Library/bin folder of your Anaconda environment. The cbc.exe file is located under the ‘solver’ in the primary model folder (state_model).
2. In the Anaconda Prompt, run the following to get the list of conda environments in the system:
```bash
conda env list
```
3. Copy the path next to the environment where <myenv> is installed. It would look something like this: C:\ProgramData\anaconda3\envs\<myenv>
4. Open File Explorer and paste the path you copied into the address bar. Navigate to the Library folder, then to the bin folder.
5. Copy the cbc.exe file from the location state_level\solver\cbc.exe and paste it into ~\Library\bin\ (the path navigated in step 5).

#### Installing matplotlib
Matplotlib is a Python library used for creating visualizations, such as line plots, bar charts, histograms, and more, with a high degree of customization.
```baash
conda install matplotlib
```
#### Installing Jupyter notebook
Jupyter Notebook is an interactive development environment that allows users to write and run code in a web-based interface. Install Jupyter notebook invoking the following command
```baash
conda install notebook
```
### Git repositories
A Git repository (repo) is a version-controlled storage space for project files, tracking changes over time and allowing users to collaborate without overwriting each other's work. Repos can be hosted locally or on remote platforms like GitHub, facilitating efficient code management and collaboration. For more information, go to https://github.com/ 

**For Mac users:** Git is installed by default in the OS and no extra steps are required.

**For Windows users:** visit the [Git for Windows](https://git-scm.com/download/win) website and download the latest version. After downloading, run the installer and follow the prompts.

#### Clone gridpath repo
GridPath is a versatile grid-analytics platform that seamlessly integrates several power-system planning approaches – including production-cost, capacity-expansion, asset-valuation, and reliability modeling – within the same software ecosystem. More information can be found here: https://gridpath.readthedocs.io/en/latest/index.html 

**For Mac users:** 
``` bash
cd ~/Desktop/state_model 
git clone https://github.com/blue-marble/gridpath.git --branch v0.16.1
cd ~/Desktop/state_model/gridpath
pip install .
```
**For Windows users:** 
``` bash
cd *\Desktop\state_model 
git clone https://github.com/blue-marble/gridpath.git --branch v0.16.1
cd gridpath
pip install .
```

#### Clone workshop repo
Download and clone the gridpath-workshop repo to the local system. The folder includes all necessary files and folder for running the model:

**For Mac users:** 
```bash
cd ~/Desktop/state_model  
git clone https://github.com/cetlab-ucsb/gridpath-workshop-ucsb
```

**For Windows users:** Continuing from cloning the gridpath repo section, type “cd ..” to set directory to the parent directory - state_model
``` bash
cd ..
git clone https://github.com/cetlab-ucsb/gridpath-workshop-ucsb
```
#### Note: initial setup
The instructions up to this point are essential for setting up the model correctly and need to be run only once. For instructions on running the model after the initial setup, refer to the section on running the model after the initial setup.
—---------—---------—---------—---------—---------—---------—---------—---------—---------—-----

### Jupyter Notebook
#### Open Jupyter Notebook
Note: If you have previously run the model, ensure that you delete the contents of the 'db' folder for optimal performance. Similarly, either remove or rename the results of any previous runs stored in the 'scenarios' folder.

Run the following command to open the jupyter notebook interface via the terminal.
```bash
jupyter notebook
```
The jupyter notebook interface will look like this:

![gp_desktop](https://github.com/cetlab-ucsb/gridpath-workshop-ucsb/blob/main/images/gp_desktop.png)

There are two Jupyter notebooks available, each for a separate model. Please choose the one you would like to run and visually navigate to the Jupyter notebook located in the gridpath-workshop folder. The path should be: Desktop -> state_model -> gridpath-workshop-ucsb. The two notebooks are:
- gridpath-workshop-capex.ipynb: Runs the capacity expansion model
- gridpath-workshop-production.ipynb: Runs the production cost model
  
The selected Jupyter notebook will open in a new tab in your browser and should look like this:

![gp_notebook](https://github.com/cetlab-ucsb/gridpath-workshop-ucsb/blob/main/images/gp_notebook.png)

In jupyter, every code block needs to be run individually. You can run a code block by clicking the play button (blue circle above).

Any text that starts with # is a comment. Comments are ignored by the Python interpreter and are not executed as part of the code. They are used to explain or clarify the code for developers, making it easier to understand. Some code blocks include comments which include additional context and/or instructions. 

Once you have opened the Jupyter Notebook, simply follow the steps outlined in the notebook to generate the results. After the model has finished running, the results will be saved in your local folder.

### Running the model after the initial setup
After the initial setup, there is no need to reconfigure the Conda environment or clone the Git repositories again. The user simply needs to activate the existing environment and launch the Jupyter notebook.
```bash
conda activate <myenv>
Jupyter notebook
```



