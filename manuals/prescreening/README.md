# Prescreening Manual

## 1: Ensure Consent

* Make sure participant has filled out all parts of the consent form. 
* Make sure a member of the research team (ask Paul) has signed the consent form as well
* **IMPORANT:** never put the subid in an email to the participant, or in any email, text, Zoom invite, calendar event, slack messagae, or other communication that could potentially link the subid with the name or email address of the participant.
    * The ONLY place where participant names/emails will be linked with subids is in the offline SUBID KEY (a flash drive)


## 2: Schedule prescreening
* Find a time that works well for both you & the participant via email
* Confirm this time with Paul so that he can set up Zoom session
* Send participant the Zoom link via email

Note: Try your best to reply to all participant emails within 24 hours, and between 9am-5pm in (to the best of your knowledge) their time zone
* To keep communications as secure as possible please **always** use your `columbia.edu` address and never a non-Columbia email address.

## 3: One day before prescreening, 

Remind participant of prescreening time via email, with Zoom link

## 4: 15 minutes before scheduled time of prescreening call

* Set up github branch for prescreening session
    * Go to github desktop and make sure you're on the main branch. Click `Fetch Origin` and then `Pull` (if needed) to make sure you are up to date
    * Create a new branch labeled `AMFM###` for the participant you are about to prescreen. 
    * *Double check* that this is the correct participant, and check the `raw_data` folder to make sure there are no files for this participant already

* Get your command line set up to run the prescreening script
    * This might be a little different depending on your computer setup, but navigate to the `AMFM/scripts` folder beforehand so you a ready to go
    * You can test out whether you're in the right place by running the prescreen script just to see if it starts (i.e. if it prints out some text, then quitting right away)
        * Note: `ctrl + c`  should be able to quit you out of most running things on the command line cleanly 

* Get your REDCap consent form ready:

    1. Open [REDCap](https://redcap.psych.columbia.edu/index.php) website
    2. Login with your username and password:
    3. Click on the AMFM Study under "My Projects":
<img src="my projects.png">
    4. Find "Manage Survey Participants" on the left side of the page, under "Data Collection" section
    5. Click on "Participant List" tab on the main page, you'll see the list of participant emails with their identifiers. Clicking on the "Participant Identifier" will sort the participants by their identifier from smallest to largest
    6. Click on the green check in the "Responded?" column next to the participant you're working with; this will open up the consent form saved in the REDCap system; scroll down and find the emergency contact information if they chose to provide 


* Be ready to get on the Zoom if needed if the participant is extra early


## 5: 5 minutes before schedule time of prescreening call 

* Be on the Zoom ready to greet the participant when they show up. 
* Get your Zoom & command line windows arranged so you can easily see both
* Start the prescreening script from the command line as follows using 2 command line arguments for the `subid` and `year`:

```console
python 1_run_prescreen.py AMFM300 2021
```

## 6: Once the participant joins the call

* Welcome the participant! Help them as best you can to feel comfortable on the call, and make sure to answer any questions before settling in.
* Remember that while it is important to keep our procedures as standardized as possible, it is far more important that our participants feel comfortable and welcomed in the study. 
* Follow the directions from the prescreening script, making sure to adjust to any needs of the participant.

### If a participant is included

* Try to pull up your calendar and schedule 3 study sessions
    * 1st session should be at least one week (ideally between 1-2 weeks) from the current day
    * Each session should be at least one week (ideally between 1-2 weeks) from the last
    * Pick times where you will have a 2-hour timeslot free for setup + up to a 90-minute session (the participant only has to be free for up to 90 min though)


### If a participant is excluded

* Thank them for their participation, and explain that they will be paid for their time in the study. 
* If the participant asks why they excluded, it is okay to tell them unless this is because of the T-MoCA (*because we do not want to cause participant undue stress by telling them they have fallen below our study-specific criteria on a neuropsychiatric test, especially that we don't have official clinical training on it*)
    * If the participant was excluded because of a low T-MoCA score, we can simply say that not all participants will have the opportunity to take part in all three sessions, and they were only chosen for this initial session.

## After the Zoom is over

Whether included or excluded:
* Note the total time the participant was on the call and send to Paul for payment calculations
* Commit the files created for prescreening this participant to the participant's branch (i.e. the branch `AMFM###`), push the branch to Github, and submit a pull request from Github requesting Paul as the reviewer

If included:
* Send Paul the selected times for each scheduled session
    * Follow up to make sure Paul creates separate Zoom links for each, and email these to the participant
    * See the [README for sessions](../sessions/README.md) for detailed instructions



# Troubleshooting 

## If the participant's Zoom connection is bad

* See if things are any better if they turn off video or go to another room
* Be extra kind and patient with the participant 
    * Some people may *really* want to participate even if the tech is tricky
* Use your best judgement to make a decision by the end of the call if their call quality is too poor for music & memory sessions to be feasible.
    * If the quality is bad but the participant thinks it would be better another day, you can offer to reschedule the call based on your judgement


## If a script crashes or other command line problem happens:

Don't worry! It happens, and is probably Paul's fault. 

If you think you can resolve it quickly:
* It is okay to tell the participant something along the lines of *"I'm sorry, I'm having a quick technical difficulty on my end -- one moment and I'll be ready to keep going soon"*

If it is a more complicated problem you don't think you can fix easily during the session. 
* Apologize to the participant for having to cut the session short, and let them know you'll be in touch about rescheduling.

Depending on how far you got, you may be able to pick up by specifically running the remaining scripts in the `prescreening` folder as follows:


*to run the event selection* 
```console
python prescreening/2b_select_events.py AMFM300
```

*to run moca*

```console
python prescreening/2c_moca.py AMFM300
```

**Either way, let Paul know right after the session is over so he can help fix it**