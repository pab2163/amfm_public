# AMFM Music & Memory Sessions Manual

## Reminder: 
* <strong>NEVER share participant information through [written] digital communication only share through verbal communication that is NOT kept </strong>
  

# About a week before the music & memory session:

* Zoom session links on the google calender are to be labeled by Paul using a random  string that is connected to the subid. You will know which string is attached to which subid during the weekly meetings, please write this information <strong>on paper you keep safe and private</strong> 
* If this is session 1, confirm with Paul that all necessary files (`AMFM###_ses1.csv` are prepared for running sessions)
* Make sure you have all non-music clips downloaded from [OSF](https://osf.io/ae7nw/)

# One day before the music & memory session: 

* Make sure to have access to the spotify link for the participant
    * These should be found in our databse on Google Drive, but ask Paul if you don't see it
    * Check the spotify playlist for the participant and make sure that all songs are *playable* (none are greyed out)
    * Make sure you have **pulled** any updates to your participant's branch (i.e. `AMFM###`) to your computer from Github. 


# 15 minutes before the session time: 

Prepare:

1. The slides to share with the participant while they answer questions about the music and memory [Google Doc Version](https://docs.google.com/presentation/d/1wBSUd-9QQxjFHZkhtv_LR9f3JiX8bivUUIZ04TP7WdA/edit?usp=sharing). 
2. Make sure you are on the correct branch for your participant (i.e. `AMFM###`)
3. Open up your command line so you are in the `AMFM/scripts`
4. Open up Spotify 
5. Put on headphones (this way you'll be sure that participants hear the sound straight from Zoom, rather than through computer speakers)

# 5 minutes before the session time:
* Be on the Zoom session ready to greet the participant
* Make sure the zoom session is being recorded
    * the session should be recorded automatically -- if it is not already being recorded then turn recording on if you can (if you don't have this option, call Paul)
* Have a piece of paper or notebook and pen next to you in case you need to make a note during the session


**Type in terminal <em> AFTER </em> making sure you are in the right folder**

`python 3_run_session.py [subid] [session #]`

* Make sure you have the slides ready so you can share them as the session is taking place


# Once the participant joins: 

* Greet participant, inform the participant that you can answer questions they may have 
* Inform the participant that he/she can close their camera if they wish and that they can take breaks

# During the session 
* If breaks happen just keep the terminal window open
* If there was a knock on the door or another interruption during the 30 seconds of music, pause the music then when the participant is back play it again
* If there is an interruption that lasts more then 10 seconds during memory recall, skip the rest of the trial (it will be excluded)

* If a participant experiences emotional distress then be patient, understanding and listen to what the participant is saying. Do not push them to do any part of the experiment they do not feel comfortable with. Make sure to remind the participant that they can take a break if they wish. 
* If a participant is close to speaking for the entire 4 minutes, 15 seconds before 4 minutes are up try to politely stop the participant. You can say <em> "Thats all the time we have" or "let's please move on to the next question for now" </em>
* If a participant dosen't want to finish the session or the session has to end for other reasons, you can save the data by treating further trials as 'skips', just enter 0 for all items.
* If a participant answers the <em>"how positive/vivid"</em> question then changes their mind about the answer, write this down as a note with the trial number. Make sure that you inform the participant that you are just writing down a correction
* If a participant starts talking about the same memory but from a different session, ask the participant if they can talk about a different event that relates to the prompt
* Mention the time period alongside the prompt but make sure to stay consistant with this practice and do that for all sessions for the participants
* The general time periods are: childhood (5-9), adolescence (14-18), adulthood (20-25) but a year or two outside the time period is fine too unless its before the age of 5. Childhood (5-up to 11), Adolescence (12-19) and Adulthood (19-27)
* If a participant is not recalling any specific episode, ask if they have a more specific memory once. If after that the participant is still recalling semantic information let them continue talking
* If you are certain that a memory is out the time range, interrupt the participant. If you aren't too sure then don't interrupt until the end
    * If a participant switches to a memory in the correct time period then make sure to give him/her the full 4 minutes 
* If a participant talks about a memory outside the time period, repeat the prompt with the specific time period range too

# After each session: 

* Commit and the files created for session to the participant's branch (i.e. the branch `AMFM###`), push the branch to Github, and submit a pull request from Github requesting Paul as the reviewer

# After the 3rd session
s
* <strong> Destroy the paper with the secret string and subid </strong> 


# What to do if issues happen during the session? 

* Any issues are mostly likely Paul's fault! If you hit a technical problem, don't worry -- these things happen. *

If the issue is tiny and you can fix it quickly: 
* It is okay to tell the participant something along the lines of *"I'm sorry, I'm having a quick technical difficulty on my end -- one moment and I'll be ready to keep going soon"*

If you can't fix the issue: 
* Apologize to the participant for having to cut the session short, and let them know you'll be in touch about rescheduling.

<strong> Tell Paul what happened after the session </strong>
