import streamlit as st
from PIL import Image
import base64

import pandas as pd
import datetime as dt


####
# setting page's format
####
st.set_page_config(layout="wide",page_title="London Bulls Official Website")

# remove "made with streamlit" text - this makes app prettier
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

####
# App
####

# App's title image
image = Image.open('./images/logo_LB_no_icon.png')

st.image(image) # , caption='Sunrise by the mountains'

# App's icon image

# LOGO_IMAGE = "logo.png"

# st.markdown(
#     """
#     <style>
#     .container {
#         display: flex;
#     }
#     .logo-text {
#         font-weight:700 !important;
#         font-size:50px !important;
#         color: #f9a01b !important;
#         padding-top: 75px !important;
#     }
#     .logo-img {
#         float:right;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True


# st.markdown(
#     f"""
#     <div class="container">
#         <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
#         <p class="logo-text">Logo Much ?</p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )


# App's title
st.title('London Bulls Official Website')


# Load the Excel file into the session state object
if "df" not in st.session_state:

    # Load the Excel file into a DataFrame
    # st.session_state.df = pd.read_excel(".\Files\London Bulls Excel 21-22.xlsx", sheet_name ="Rolling")
    st.session_state.df = pd.read_csv("./Files/london_bulls_excel.csv")



# Load the Excel file into a DataFrame
# df = pd.read_excel(".\Files\London Bulls Excel 21-22.xlsx", sheet_name ="Rolling")

##
# Data cleaning
## 

# cols to lowercase, and blank spaces to underscore
st.session_state.df.columns = st.session_state.df.columns.str.lower()
st.session_state.df.columns = st.session_state.df.columns.str.replace(' ','_')

# Convert the 'date' column to datetime dtype
st.session_state.df['date'] = pd.to_datetime(st.session_state.df['date'])

##
# Data gathering
##

# # Create a list of unique player names from the CSV file
unique_players = st.session_state.df['full_name'].unique().tolist()

# # Create a list of unique tournament names from the CSV file
unique_tournaments = st.session_state.df['tournament'].unique().tolist()

# # Data gathering - Create a list of unique opponent names from the CSV file
unique_opponents = st.session_state.df['opponent'].unique().tolist()

# # Display first two rows of the dataframe

st.subheader('A sneaky peak into some previous player statistics:')

st.write( st.session_state.df.sample(6) )

# Define a function to add a new row to the DataFrame
def add_row(df, players, starting, minutes, goals, goals_conceded, yellow_card, red_card, tournament, date, opponent):

    new_rows = []

    for player in players:

        new_row = {"full_name": player, 
                        "starting": starting,
                        "minutes": minutes,
                        "goals": goals,
                        "goals_conceded": goals_conceded,
                        "yellow_card": yellow_card,
                        "red_card": red_card,
                        "tournament": tournament,
                        "date": date,
                        "opponent": opponent
                        }

        new_rows.append(new_row)

    new_rows_df = pd.DataFrame(new_rows)
    df = pd.concat([df, new_rows_df], ignore_index=True)

    return df

st.write('\n')

# # Add title for the subsection
st.subheader('Update player statistics after the latest match:')

# Split screen in two cols
col1, col2 = st.columns(2)

with col1:
    # Create a form for adding a new row
    players = st.multiselect("Select players", unique_players) # Use multiselect for selecting multiple players

    # Allow users to add new players to the list
    new_player = st.text_input("Enter a new player (if not in the list)")
    if new_player:
        unique_players.append(new_player)
        players.append(new_player)  # Automatically select the new player

    starting = st.selectbox("starting? :smoking:", ("yes", "no"))
    minutes = st.number_input("Enter minutes", format="%d", step=1)
    goals = st.number_input(":soccer: Enter goals", format="%d", step=1)
    goals_conceded = st.number_input(":lock: Enter goals conceded", format="%d", step=1)

# setting another col
with col2:
    
    # Create a form for adding a new row
    yellow_card = st.text_input("Enter 1 if player received a red card or leave empty")
    red_card = st.text_input("Enter 1 if player received a yellow card or leave empty")

    # Allow users to select a tournament from the existing list, or select an empty option
    tournament = st.selectbox("Select tournament (leave empty if it's a new tournament)", [""] + unique_tournaments)
    
    # Allow users to add a new tournament
    new_tournament = st.text_input("Enter a new tournament (if not in the list)")
    if new_tournament:
        unique_tournaments.append(new_tournament)
        tournament = new_tournament  # Automatically use the new tournament
    
    date = st.date_input("Enter date")

    # Allow users to select an opponent from the existing list, or select an empty option
    opponent = st.selectbox("Select opponent (leave empty if it's a new opponent)", [""] + unique_opponents)
    
    # Allow users to add a new opponent if the selected option is empty
    if not opponent:
        new_opponent = st.text_input("Enter the new opponent name")
        if new_opponent:
            unique_opponents.append(new_opponent)
            opponent = new_opponent  # Automatically use the new opponent


# convert dates to int
# st.session_state.df['date'] = st.session_state.df['date'].apply( lambda item: item.strftime("%Y-%m-%d") )

##
# Buttons
##

add_button = st.button("Press here to add statistics")

st.write('\n')


# # If the "Press here to add statistics" button is clicked, add the new rows to the DataFrame
if add_button:
    
    st.session_state.df = add_row(st.session_state.df,players, starting, minutes, goals, goals_conceded, yellow_card, red_card, tournament, date, opponent)

    st.success("New data added successfully!")

    # checkpiont
    print(st.session_state.df.tail(4))

    # horizzontal line
    st.divider()

##
# Display data
#

st.subheader("Player statistics after the latest match:")

# Convert the 'date' column to datetime dtype
st.session_state.df['date'] = pd.to_datetime(st.session_state.df['date'])

# Find the most recent date in the DataFrame
most_recent_date = st.session_state.df['date'].max()

# Filter the DataFrame to display only rows with the most recent date
df_most_recent = st.session_state.df[st.session_state.df['date'] == most_recent_date].copy()

# Change the date format to 'dd-mmm-yyyy'
df_most_recent['date'] = pd.to_datetime(df_most_recent['date']).dt.strftime('%d-%b-%Y')

# Display the filtered DataFrame
st.write(df_most_recent)

st.write('\n')

st.divider()

##
# Add a button to save the updated DataFrame to the Excel file
save_button = st.button(":white_check_mark: :checkered_flag: Save statistics for the most recent match")

# If the "Save" button is clicked, append the new data to the Excel file
# if save_button:
#     with pd.ExcelWriter(".\Files\london_bulls_excel.csv", mode='a', engine="openpyxl") as writer:
#         df_most_recent.to_csv(writer, index=False, header=False, startrow=len(df) - len(df_most_recent))
#         st.success("Statistics for the most recent match have been saved!")


# If the "Save" button is clicked, append the new data to the Excel file
if save_button:
    st.session_state.df.to_csv("./Files/london_bulls_excel.csv", index=False)
    st.success("Statistics have been saved!")
