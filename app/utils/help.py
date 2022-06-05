from dash import dcc


HELP = dcc.Markdown('''# Overview

Spotify Analyzer is an app which allows you analyzing tracks, albums and (public) playlists from Spotify. 

In order to use the app just type a track/album/playlist name in the input field at the top od our site and click *search*. Then all cards, which lie below the search bar, will have useful vizualizations about sall selected tracks. All vizualizations are interactive, so while hovering a mouse above one fragment more info should appear.

# Details

## Searching

* You can either look for an item, or select one from our predefined datasets
* After you search for a playlist or album, all songs from there will appear in the list of songs classified to a query with the name of playlist/album
* After you search a track, the track will appear in the list of songs classified to "Your playlist" - all songs, which will be added individually will be labeled with such name
* You can revert each search query individually, all you need is selecting drop-down menu "Undo one of the steps" and select a query there
* You can revert all changes - click the "Reset" button
* Every time you will search something a loading animation will apear on the right to the "Reset" button - when it's visible just keep calm and wait for results
* It might turn out, that the result of the search wasn't satisfatcory. Note, that multiple songs, albums or especially playlists may have the same name. In such a case you can try following trick:
  * While typing song or album name you can type artist:{ARTIST} after a space, e.g.:
    > Hello artist:Adele
    
    Where "Hello" is the song's name, and "Adele" is the Artist

## Vizualizations

### Value boxes

We have 3 value boxes here, showing:
* Lenght of the playlist (in minutes)
* Mean value of the music tempo measured in Bumps Per Minute
* Percentage of explicit songs in all currently added tracks

### List of songs 

A table showing all tracks is very useful! You can:
* Sort and filter all songs by each column (name, album, artist and query)
* Select which songs do you currently want to analyze - if you select only few tracks all vizualizations will correspon only to them!
* Delete each song separetaly 

### General statistics - radar (star) plot

A radar plot is a plot which allows us to see which attributes describe our tracks in most accurate way. We can show the data in 3 different ways using "Select the behaviour of radar plot" drop-down menu:
* **Average everything** - it generalizes all queries and display average values of all songs currently visible in the table on the left
* **By query** - it shows every query separetely
* **Each song separetely** - it shows every track separetely

### Top songs

On default this bar chart shows top 5 category based on danceability, while the color of bars is definied by their energy. But the whole behaviour of this plot can change:
* The slider allows to change top 5 to top 10, 15 or 20 songs
* Using drop-down menus the color and bar chart attributes can be changed

### Parallel Coordinates Plot

A parallel coordinates plot show nice corelations between parameters. It's very helpful with multivariete data. 
You can choose what parameters you want to include in the plot, as well as specific queries.

### Compare data on a sunchart

A sunchart is a round plot which shows us proportions in data given the parameters. On default we compare songs' keys, modes and their explicitness. But this can be easily changed by entering another attributes in the input separating them by comma in order from the one that it the closest to the cirsle's center, e.g.:
> query, mode, key

### Scatterplot

Here we can show the distributtion of the data given parameters. All parameters can be changed using left-side drop-down menus.

## Parameters overview

We have following audio attributes:
* **Danceability** - describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
* **Energy** - a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
* **Speechiness** - detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
* **Acousticness** - a confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.
* **Liveness** - detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.
* **Valence** - a measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
* **Duration** - the duration of the track in seconds.
* **Popularity** - the popularity of the artist. The value will be between 0 and 100, with 100 being the most popular. The artist's popularity is calculated from the popularity of all the artist's tracks.
* **Instrumentalness** - predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
* **Loudness** - the overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db.
* **Tempo** - the overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.
* **Mode** - indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.
* **Key** - the key the track is in. Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1.
* **Explicit** - define whether a song is explicit
* **Time_signature** - nn estimated time signature. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure). The time signature ranges from 3 to 7 indicating time signatures of "3/4", to "7/4".
''')
