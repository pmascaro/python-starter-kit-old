# London Bulls App

### Folder Structure


### Getting Started

### Creating the project (for developers only)

#### 1. Creating venv

This sections is based on the following youtube tutorial: https://www.youtube.com/watch?v=brJR5Qjp4SM

and https://bobbyhadz.com/blog/source-is-not-recognized-as-internal-or-external-command

To create virtual environment, in the project terminal, use `python -m venv venv`, where 'venv' is the name of the virtual environment. A `venv` folder will appear in the project directory.

#### 2. Using venv

This creates the virtual environment. We now need to activate it. To do so, use:

- if you use windows use the following: `venv\Scripts\activate.bat`

_Aside note:_ remember that 'chdir' command prints the path in the terminal

To deactivate it, type: `deactivate`

_Aside note:_ To deactivate the `(base)` environment, type `conda deactivate`

_Note:_ To check for interpreter, use `python`

Now it's time to install all your required libraries, which you can do as you require them. Also, you can check (here)[https://towardsdatascience.com/how-to-use-bash-to-automate-the-boring-stuff-for-data-science-d447cd23fffe] if you want to install them in one go

At the end of the process, use this in the terminal:

`pip freeze --local > requirements.txt`

You can always create another virtual environment, you can always copy all the requirements from the requirements.txt file:

`pip install -r requirements.txt`

#### Installing independencies for virtual environment

`python -m pip install --upgrade pip`

If you have created a new project from zero, install libraries adding the line of code below:

`pip install 'all libraries here`

- Example: `pip install pandas streamlit`


### Running Streamlit app

#### Development mode

`streamlit run app.py`

### Sharing Flask app with non-technical stakeholders

