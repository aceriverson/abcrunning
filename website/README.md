## Welcome to ABC Run Log!

## Table of contents:

    Setting up the site: 22
    Getting started: 32a
    Logging in: 40a
    Logging out: 47a
    Logging a run: 52a
    Adding gear: 71a
    Join groups: 85a
    Create groups: 94a
    Leaving a group: 104a
    Viewing your groups: 114a
    Personal profile page: 128a
    Viewing detailed activity report: 141
    Weather report: 150a
    Changing password: 162
    Conclusion: 170


## Setting up the site

    A world-wide accessable version of ABC Run Log is on its way, but to try out our service now, follow the instructions to launch your own website.

    a. Ensure you are in the /website directory of ABC Run Log
    b. Through the terminal, execute "flask run"

    This package contains a pre-filled database to help you explore and connect with other users.


## Getting started

    To begin, visit the /register page by clicking the top right corner.
    Enter a username, password, and confirm your password.

    If all of the fields pass our checks, your account will be activated and you will be logged in automatically!


## Logging in

    If you sign out and need to sign back in, navigate to 'Log In'
    Use your username and password to sign in.
    While your password will be encrypted, please refrain from using any passwords that you use on other sites.


## Logging out

    While logged in, navigate to 'Log Out' in the top right to clear the session.


## Logging a run

    In the navigation bar, select 'Log Run'
    Here you can enter the details of your latest run to share with others and store in your log!

    We have given you a default run name, but feel free to change it to keep better track.
    Enter the type of run from either our preselected choices (Run, Easy Run, Workout, etc) or enter your own.
        Users who would like to log activities other than running (biking, swimming, walking, etc) may specify so here.
    Fill out the distance, time, and date.
    Feel free to fill out any of the remaining fields, however these are optional for those who do not wish to use them.
    If you are tracking mileage on any gear, select it here. See line
    ## TODO
    to add your first piece of equipment.

    Submit your run!

    You will now see it appear on your personal section of the / page.


## Adding gear

    If you don't have any gear entered yet, you will be prompted to fill out the form to add some.
    Start with the brand, model, and finally a nickname that helps you remember what it is, then click 'Add'.

    Your gear will now show up in the gear page, and you can select it when logging a run.

    Once your gear has reached the end of its usable life, you can retire it on the /gear page by selecting it, and clicking 'Retire'.
    This gear will remain visible but it will no longer be possible to log mileage on.

    If you would like to remove a retired piece of equipment entirely, select it and click 'Remove'. This action is permanent,
    however the mileage run on the shoe will still be visible elsewhere on the site.


## Join groups

    Now if you want to start connecting with other runners, navigate the 'Groups' dropdown and select 'Join a Group'

    Here you can see a list of 20 most active groups, and you can join one with the click of the 'Join' button.
    If you are looking to join a specific group, enter the group id into the 'Group ID' box on top. The groupid can be given to you by a
    friend who is already in the group when they visit the /group's page.


## Create groups

    If you'd like to host your own group for friends, navigate the 'Groups' dropdown and select 'Create a Group'

    Enter a unique group name and a short bio, and you are on your way!
    The creator of a group is automatically added to the group, so don't worry about joining.

    Users are limited to creating three groups.


## Leaving a group

    If you would no longer like to connect with a group, navigate the 'Groups' dropdown and select 'Leave a Group'.

    Select the group you would like to leave from the dropdown and click 'Leave'.

    Note: Group creators do not have the ability to leave their groups.
    Note: Groups will not reappear in the join groups page, remember their Group ID to manually rejoin.


## Viewing your groups

    To see the activites shared among your groups, navigate the 'Groups' dropdown and select 'My Groups'.

    Select from the dropdown the group you would like to view and click 'View'.

    You will be given the group name and bio, as well as a share link so you can share the group feed with others.
    The 'Group ID' field can be copied and pasted into /joingroups to join said group.

    Each page will also have 15 runs, ordered by date. Navigate using the next/back buttons below to see more runs
    You can click on the username to reach the personal profile of the activity logger, or the activity name to view detailed information about
    the activity.


## Personal profile page

    Navigate by clicking your username in the top right corner.

    Here you will see your latest activites and you can use the next/back buttons to navigate further activities.
    Available below the activities is a glimpse into your training data. You can view your lifetime mileage, lifetime average pace,
    recent mileage, and recent average pace.

    There is also a table of the groups you belong to, so others can see and view.

    The url can be copied and pasted to share your page with other runners.


## Viewing detailed activity report

    You can view the details of a logged activity by clicking the hyperlinked name anytime you see an activity summary.
    (Activity summaries available on /, /group, /profile)

    Here you will see all of the data entered. Because some data is optional, any fields not entered will not be shown.
    You will also be able to track the current mileage of the gear used, if any, and the qualitative/additional feedback, if any.


## Weather report

    Select 'Weather' from the navigation bar.
    Type in your zipcode for the most precise forecast, but feel free to use your city for general results.

    Once your location is entered, click 'Search'.

    You will see a forcast of current conditions such as weather, condition, and wind speed.
    You will recieve a suggestion about if the conditions are suitable for running
    You will recieve advice on what to wear when running


## Changing Password

    To change your password, navigate to your profile page  by selecting your username in the top right corner.

    Enter your current password, a new password, and confirm the password. Your new password will be saved, and the old password will
    no longer be associated with your account.


## Conclusion

    Thank you again for using our service, ABC Run Log.

    The run log here is designed to be an easy way for athletes and coaches to keep each other accountable and stay on top of the numbers.

    Any questions, suggestions, or concerns can be brought to the owners, Acer, Ben, and Colin, through this link:
    "https://projects.iq.harvard.edu/abcrunning/contact_owner"