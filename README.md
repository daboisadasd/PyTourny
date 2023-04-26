# PyTourny


## bot goals:

### keep track of everyone who is participating when they enter the offline join command and save their name to db

### maintain a queue when 12 people have used the offline join command

### when the specified discord user enters the raid start command everyone in the offline voice channel will be deafened who is not in the queue

### when someone dies they use the dead command and it undeafens them and adds a death to their name in the db

### the last person to die enters the winner command and gets placed into the queue and the first person in the queue replaces them

### in the end i want to display the queue and winners stats on a simple django site

### as for twitch integration it would be cool to send status updates and death counts to the twitch chats but idk if i actually want to go down that road
