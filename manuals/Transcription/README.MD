# Autobiographical Interview Transcription Manual

## Columns: 
* `subid`: input the subid of the participant, it should start with AMFM
'session': input session number 
* `event`: input the event (from the list of event prompts) after double checking the audio file too
* `memory_duration`: use the `time_code` column, and calculate the memory duration from the time code for the first utterance of the participant for a memory up to the time code when the experimenter says "thank you for sharing that memory"
* `sentence`: input all sentences from the moment the experimenter says the prompt ( you mentioned that you remember a time …. Can you talk more about that …)
* `probe`: A *sentence-level* marking. <strong> everything in this column should be lower case! Possible words you can input are [ “unrelated”, “experimenter”, ”recall”, ”general”] </strong>
  - unrelated: *Do not score the sentence.* - sentences like “ I hear someone at the doorbell” or “ I remember going to the park when I was 32”(out of time frame) or clarifying questions, etc.. If the experimenter asks a clarifying question before the general probe then the responses to that questions are unrelated. 
  - experimenter: *Do not score the sentence.* - anything the experimenter says
  - recall: *score this sentence* - anything the participant says before the experimenter gives the general probe
  - general: *score this sentence* - anything the participant says after the experimenter gives the general probe - asks the participant “Is there anything else you can remember?”

* `notes_scoring`: used for any notes on scoring
* `notes_transcription`: used for any notes on transcription, such as when participant had to be redirected to talk about a memory in the time period
  * used to clarify the meaning of what a participant is saying -- communications from the transcriber or person working with participant to the scorer (for example, if a word is unclear, describing what it means)
  * sentence should say something like [wine brand] or [see notes] if there are notes that need to be referred to 

* `exclude_trial`: write a 1 if ENTIRE trial needs to be excluded
* `exclusion_reason`: <strong> used to document why the WHOLE TRIAL was excluded. </strong> Possible words you can input are 
  * time_period - participant's recall is of something in a time period more than 2 years away from the boundaries of the prompted developmental time period (or less than 5 years old). The prompted event DID NOT happen in the right time period, as far as the participant indicates. 
    * IF the trial also includes some recall in the right time period, DO NOT use this marking and DO NOT exclude the trial -- use 'unrelated' in the `Probe` column for this instead
  * no_recall - The prompted event *likely* happened in the time period, but participant says something to the effect of *I can't remember that*
  * interruption - memory recall or time between music-recall is interrupted for more than 10s
  * repeat - memory recalled is the SAME EVENT as any other event previously recalled
    * only mark this for a *repeat of the exact same event* -- if there are references to previous events recalled but the main event is different, that's okay - we won't exclude (these details would be 'other' details since they are metacognitive)
  * uncomfortable - participant has memory of event in time period, but is not comfortable sharing the details of the memories
  * never_happened - participant says that the event literally never happened. no memory could possibly be recalled. e.g. "I don't have a sibling" or "I never went on a cruise" 
  * technical -- technical error causes a problem in the trial (we can't transcribe what the participant is saying for more than 10s). Most common is low-quality audio/static making it impossible to hear dialogue

## General rules:
* If a participant switches the event he/she wants to talk about then the first response would be considered unrelated while the second response would be considered recall 
* If there is a run on sentence add a period before words like “and” when zoom cuts the sentence at that word 
* Transcribe everything including clarifying questions but words like “um” are not that important
* Responses to questions such as “Can you talk about a more specific memory” would be considered recall. Only responses after the general probe would be considered general

## Steps to making the transcript:
* You can access the recording and zoom transcript file on OSF [AMFM Internal].  In the shared amfm_memories folder, there is a transcription folder, make a folder in that transcription folder and name with the subid. Make a copy of the blank_transcription_template and move that copy to the folder with the subid. 
* You can know which prompts are used by going to the raw_data folder on the AMFM Github. You will find the session data for each participant in that folder  

Rename the folder with the correct file syntax!

<strong> File syntax </strong>

subjectID_transcription_s#
Ex: `AMFM001_transcription_s1`



