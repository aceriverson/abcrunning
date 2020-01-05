## Design Overview For ABCRunLog

## Login and Register
This part of the website was built during pset8 for finance, so the code is similar. ABCRunLog places users on the login page.
If they have an account, the user is able to login to their account as normal. If the website visitor does not have an
account, the light blue task bar featured at the top of the page allows the user to access the register page. There,
they are able to create a new account. They are asked to confirm password, so that they can make sure they did not accidentally
mistype their chosen password without realizing it. The passwords given are hashed before being stored in the database
so that if the database and its contents are somehow compromised, hackers still will be unable to use the passwords to access
those individual users' accounts.

## Logout
The logout function is again similar to pset8, using session.clear() to log the user out.

## Home/Activities
Upon registering for an account, the user is sent to the index page. This is a split page containing on the left, the latest
activities recorded by people in groups with the user, and on the right, the latest activities of our own user.
The connections activities is a select query using AND so the ID of the poster is not the same as our current user.
The query also uses a nested query to get the IDs of all users in all groups where the current user is in. The right
side is a simpler query, pulling any activites where the poster id is our own user. The activities shown are summaries,
with link to the poster's profile, and links to the detailed activity report. These are to be discussed further down.
When a new user logs in, because they neither have connections nor logged any activities of their own, they are instead
prompted with links to /joingroups and /new. This is done through an if statement in Jinja2, checking if any activities
exist, and if not, giving said prompt for the respective column.

## Log Run
The log run page provides users with a chance to post an activity. The function calls for users to input certain mandatory
information like the length and time of the run as well as a title. There are many other metrics that the user may input,
however, many of these inputs like heart rate and elevation gain are optional. This is to make the website accessible to
individuals who may not have the information or do not care about these metrics. Users are able to set the date to any point
in time from past to present. Users are allowed to set the date to past points in time to allow them to update their log
if they fall behind and/or are not able to update their log the same day as the activity they posted. With that being said,
we do not allow users to enter activities in the future, for this is a run log not a run planner. The functionality here is
a POST method form, which we then sanitize the inputs and store them in our activities SQL table.

## Gear
The gear page is linked to an SQL table also titled gear. This table stores the gear's id, the owner's id, the mileage
of the shoe, the current status of the shoe, and the name/brand/model. The gear's id is a primary key and the owner's id
is a foreign key connnecting the tables between users and their gear. The mileage column is manually updated each time a run
is recorded, so the distance from that activity is added to the shoe's mileage. The status column is default 0, which means active.
If it is active, then it will appear in your Active Gear section of /gear. These shoes will populate a select field of the /new page
so they can be applied to runs being logged. If the shoe is selected to be retired on the /group page, it's status is moved to 1. These
shoes are still visible so they appear in you Retired Gear section in /gear. They cannot be applied to logged activities. Finally, gear
that is set to status 1 (retired) can also be permanently removed in the /gear section. This sets its status to 2, it is no longer
visible, and cannot be applied to logged activities. The initial thought was to delete these shoes from our table, but by keeping
them, we can still see what gear was applied to runs in the past, even if that gear was removed from the /gear view.

## Weather
The weather page uses the openweathermap api to determine the current temperature, windspeed, and general condition in the
selected area. We opted to use the zipcode information because using just a city name and country code would lead to issues
if multiple cities in a country have the same name. However, we were forced to implement a city option as well for smaller
countries that may not use zipcodes or who's zipcodes are not in the openweather index. We also opted to use manually entered
location data rather than location services because it allows for more flexibility for users that have VPNs or limitations on
location services. With the output from the API, we used the temperature data and "weather type id" to determine the conditions
and make tailored running recommendations based on our own experiences and the conditions.

## Groups
Groups are accomplished with two SQL tables. Our first table keeps track of the group's id, it's creator, member count, and
then the name and bio. The second table keeps track of all events where users join a group, and in return, can be removed from
a group by deleting said entry. To join a group, we used a crude version of request.args. When electing to join a group through
Group ID, the form would be set to the GET method, which was then read through the current URL, and then said group was joined
if not previously joined. The second method to join is though the popular list, which is a POST method form. The top 20 groups
are determined by membership count, which is updated whenever someone joins or leaves a group. If you have already joined a group
in the top 20 groups, it will not show up on the table, and if you are in every top 20 group, the table will not appear entirely.
This is accomplished through an if statement comparing the current group to all of the groups you have joined in Jinja2. To make
this functionality work, we need to update the page twice, so there is a script which reloads the page immediately after loading
it the first time. This allows our if statements to run and keep the table updated for groups you have joined.

Next is leaving groups. The page uses a for loop in Jinja2 to create a select field for all of the groups you are in, except the
groups you have created yourself. This prevents administrators from leaving groups without a leader. When a regular user leaves a
group, an SQL update runs to remove the joingroup exchange, and subtract one from the member count of said group.

Creating groups is straightforward as a POST method form. The name and bio are given by the user, then it is inserted into the
groups table where an ID is automatically created, the user's ID is assigned to administrator, and the member count is set to 1.

Viewing groups was the most complex part. Here we used the proper request.args method to select the groupid, and page number.
When loading just /group, you are given a select option containing all of the groups you are a member of. You can view the group
which pulls up a query of 15 latest runs per page, a url which will automatically add the paster into the group, and a Group ID
to be pasted in /joingroup as well. To determine pages, we used a select query containing OFFSET, where the offset was the current
page minus 1, then multiplied by 15. Then we added links in the table caption to change the page number so you can move back/forth.

## Profile Pages
The profile page uses the request.args function to determine user's id and the page number. Similar to the /group section, it
shows the 15 most recent runs, and you can move from page to page to see older activities, by using an OFFSET parameter in the SELECT
query, where OFFSET is 15 * (page - 1). The user also can see their lifetime metrics. This is an average of all of their distances,
average of all of their paces, a sum of their distances, and a sum of their time logged. Next the user can see their last 7 days
metric, a common timeframe used in training. The same metric of average distance, average pace, total distance, and total time are used
except applied over the last 7 days of activites instead of lifetime. Next the user can see a table of all of the groups that they have
joined, with links to their pages. This is so the user can keep track of their groups, and so others can see which groups a particular user
is affiliated with. Next, if you are visiting your own profile, a link to Change Password will appear. This is through a Jinja2 if statement
and standard python if statement that checks if the current user is the same as the user of the page. Below and finally there is a url which can be
shared with anyone so they can see your profile.

## Detailed Activity Report
Again with the crude version of request.url, we can see detailed reports of every activity logged. Anytime a summary is shown on the webpage,
it also contains a link to the detailed report. This is simply a ?activityid= URL, viewable to anyone, even those not logged in. It contains
the user's name, and a link to their profile. It contains the run's name, and date. In one box, the two required metrics of distance and time
are then used to calculate pace after POSTing /new. These three metrics will always appear regardless, and if the additional metrics of
elevation, heartrate average, and heartrate max are entered, they will appear as well in the box. This is through a Jinja2 if statement.
The next box that appears is the additional data field, if it is entered in the /new page. And finally the shoe is in it's own box
if any gear is selected. It displays the gear's brand/model and nickname, as well as the mileage row of the shoe.