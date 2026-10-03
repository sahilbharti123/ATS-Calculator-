# Comic strip scripts for Your Life in Seasons. Keys become images/<key>.svg.
# Keep every line short, warm and funny; the reader is "You". No em dashes anywhere.

STRIPS = {

"comic-cast": {
    "title": "Meet the court that runs your life, one season at a time",
    "panels": [
        {"chars": [{"name": "Sun", "expr": "proud", "pose": "arms_up"}, {"name": "Moon", "expr": "calm", "pose": "wave"}, {"name": "Mars", "expr": "angry", "pose": "point"}],
         "bubbles": [{"who": "Sun", "text": "I am the King. In my season you finally find out who you are."},
                     {"who": "Mars", "text": "In mine you finally finish that argument with the landlord."}]},
        {"chars": [{"name": "Mercury", "expr": "happy", "pose": "think"}, {"name": "Jupiter", "expr": "calm", "pose": "stand"}, {"name": "Venus", "expr": "happy", "pose": "wave"}],
         "bubbles": [{"who": "Jupiter", "text": "In my sixteen years you grow. Sometimes wiser. Sometimes just wider."},
                     {"who": "Venus", "text": "In my twenty, darling, you learn what you love. And you buy cushions."}]},
        {"chars": [{"name": "Saturn", "expr": "calm", "pose": "stand"}, {"name": "Rahu", "expr": "sly", "pose": "point"}, {"name": "Ketu", "expr": "calm", "pose": "sit"}],
         "bubbles": [{"who": "Saturn", "text": "Nineteen years. I check the accounts. All of them."},
                     {"who": "Rahu", "text": "Eighteen years. I make you want things. Many things. Right now."}]},
    ]},

"ch01-comic": {
    "title": "Same person, three seasons",
    "panels": [
        {"caption": "Age 24. The Venus season.",
         "chars": [{"name": "You", "expr": "happy", "pose": "arms_up"}, {"name": "Venus", "expr": "happy", "pose": "wave"}],
         "bubbles": [{"who": "You", "text": "Life is a party and everyone is invited!"}, {"who": "Venus", "text": "Also, we are getting new curtains."}]},
        {"caption": "Age 31. The Saturn season.",
         "chars": [{"name": "You", "expr": "worried", "pose": "think"}, {"name": "Saturn", "expr": "calm", "pose": "stand"}],
         "bubbles": [{"who": "You", "text": "Why is everything so heavy? I used to be fun."}, {"who": "Saturn", "text": "You were. Now you will be reliable. It pays better."}]},
        {"caption": "Age 40. The Jupiter season.",
         "chars": [{"name": "You", "expr": "surprised", "pose": "point"}, {"name": "Jupiter", "expr": "proud", "pose": "stand"}],
         "bubbles": [{"who": "You", "text": "So all those years... it was not me being three different people?"}, {"who": "Jupiter", "text": "It was you. Under three different managers."}]},
    ]},

"ch02-comic": {
    "title": "How your first season is chosen",
    "panels": [
        {"caption": "The night you were born, the Moon was standing on one of 27 streets in the sky.",
         "chars": [{"name": "Moon", "expr": "calm", "pose": "point"}, {"name": "Mercury", "expr": "happy", "pose": "wave"}],
         "bubbles": [{"who": "Moon", "text": "This street belongs to Mercury. So Mercury goes first."}]},
        {"chars": [{"name": "Mercury", "expr": "proud", "pose": "point"}, {"name": "You", "expr": "surprised", "pose": "stand", "r": 34}],
         "bubbles": [{"who": "Mercury", "text": "Welcome. I run your household until you are eleven. Then Ketu, then Venus for twenty years, then..."},
                     {"who": "You", "text": "Do I get a say in the order?"}]},
        {"chars": [{"name": "Mercury", "expr": "sly", "pose": "think"}, {"name": "You", "expr": "worried", "pose": "stand", "r": 34}],
         "bubbles": [{"who": "Mercury", "text": "No. But you get an app. Set it to the standard Indian setting and it will show you the whole timetable."},
                     {"who": "You", "text": "Of course the planet of apps would say that."}]},
    ]},

"ch03-comic": {
    "title": "Seasons inside seasons",
    "panels": [
        {"caption": "A twenty-year Venus season. Venus is in charge of the whole house.",
         "chars": [{"name": "Venus", "expr": "happy", "pose": "arms_up"}, {"name": "You", "expr": "happy", "pose": "stand", "r": 34}],
         "bubbles": [{"who": "Venus", "text": "Twenty years of my management. Music, comfort, love, good food."}]},
        {"caption": "But every few years she hands the kitchen keys to someone else. That is a sub-season.",
         "chars": [{"name": "Venus", "expr": "calm", "pose": "point"}, {"name": "Rahu", "expr": "sly", "pose": "wave"}, {"name": "You", "expr": "worried", "pose": "stand", "r": 32}],
         "bubbles": [{"who": "Venus", "text": "Rahu will do the next three years. Day to day. I will supervise."},
                     {"who": "Rahu", "text": "We are going to want a bigger kitchen."}]},
        {"chars": [{"name": "You", "expr": "worried", "pose": "point", "r": 38}, {"name": "Venus", "expr": "calm", "pose": "stand"}],
         "bubbles": [{"who": "You", "text": "So when things go strange, who do I complain to?"},
                     {"who": "Venus", "text": "Both of us. Mostly him. Check whether he and I are even friends, and which room he is sitting in."}]},
    ]},

"ch04-comic": {
    "title": "The Ketu season: seven years of less",
    "panels": [
        {"chars": [{"name": "You", "expr": "surprised", "pose": "point", "r": 38}, {"name": "Ketu", "expr": "calm", "pose": "sit"}],
         "bubbles": [{"who": "You", "text": "You are running my life for seven years and you do not even have a head?"}]},
        {"chars": [{"name": "You", "expr": "worried", "pose": "stand", "r": 38}, {"name": "Ketu", "expr": "calm", "pose": "sit"}],
         "bubbles": [{"who": "You", "text": "Fine. What are we doing this season?"}, {"who": "Ketu", "text": "Less."}]},
        {"chars": [{"name": "You", "expr": "surprised", "pose": "think", "r": 38}, {"name": "Ketu", "expr": "calm", "pose": "sit"}],
         "bubbles": [{"who": "You", "text": "Less what?"}, {"who": "Ketu", "text": "Yes."}]},
    ]},

"ch05-comic": {
    "title": "The Venus season: the long bloom",
    "panels": [
        {"caption": "Year 1 of 20.",
         "chars": [{"name": "Venus", "expr": "happy", "pose": "wave"}, {"name": "You", "expr": "happy", "pose": "stand", "r": 36}],
         "bubbles": [{"who": "Venus", "text": "Welcome! First we make the house beautiful. Then we fall in love. Then maybe both again."}]},
        {"caption": "Year 11 of 20.",
         "chars": [{"name": "Venus", "expr": "calm", "pose": "point"}, {"name": "You", "expr": "sleepy", "pose": "sit", "r": 36}],
         "bubbles": [{"who": "You", "text": "I have become very comfortable."}, {"who": "Venus", "text": "That is the danger of me, darling. Comfort is a chair you forget to leave."}]},
        {"caption": "Year 20 of 20. The Sun is at the door.",
         "chars": [{"name": "Venus", "expr": "sad", "pose": "wave"}, {"name": "You", "expr": "worried", "pose": "stand", "r": 36}, {"name": "Sun", "expr": "proud", "pose": "stand", "r": 34}],
         "bubbles": [{"who": "Sun", "text": "Right. Everyone off the sofa. We have a self to build."}]},
    ]},

"ch06-comic": {
    "title": "The Sun season: six years in the light",
    "panels": [
        {"chars": [{"name": "Sun", "expr": "proud", "pose": "point"}, {"name": "You", "expr": "worried", "pose": "stand", "r": 36}],
         "bubbles": [{"who": "Sun", "text": "Stand in the light. Say your name. Say it like you mean it."}, {"who": "You", "text": "I prefer the corner, actually."}]},
        {"chars": [{"name": "Sun", "expr": "angry", "pose": "arms_up"}, {"name": "You", "expr": "surprised", "pose": "stand", "r": 36}],
         "bubbles": [{"who": "Sun", "text": "Six years. No corners. Also, call your father."}]},
        {"chars": [{"name": "Sun", "expr": "happy", "pose": "stand"}, {"name": "You", "expr": "proud", "pose": "arms_up", "r": 36}],
         "bubbles": [{"who": "You", "text": "I asked for the promotion. Out loud. In a meeting."}, {"who": "Sun", "text": "Now you are getting it. The season, I mean. The promotion too, probably."}]},
    ]},

"ch07-comic": {
    "title": "The Moon season: the household of the mind",
    "panels": [
        {"chars": [{"name": "Moon", "expr": "happy", "pose": "wave"}, {"name": "You", "expr": "happy", "pose": "stand", "r": 36}],
         "bubbles": [{"who": "Moon", "text": "Have you eaten? Sit. I made your favourite. Also, we may be moving house."}]},
        {"chars": [{"name": "Moon", "expr": "sad", "pose": "think"}, {"name": "You", "expr": "surprised", "pose": "stand", "r": 36}],
         "bubbles": [{"who": "You", "text": "You were so happy a minute ago."}, {"who": "Moon", "text": "That was a different minute."}]},
        {"chars": [{"name": "Moon", "expr": "calm", "pose": "stand"}, {"name": "You", "expr": "calm", "pose": "sit", "r": 36}],
         "bubbles": [{"who": "Moon", "text": "Ten years of feeling everything. Learn to watch the tide instead of fighting it, and you will do well."}]},
    ]},

"ch08-comic": {
    "title": "The Mars season: the Commander takes charge",
    "panels": [
        {"caption": "6:00 am.",
         "chars": [{"name": "Mars", "expr": "angry", "pose": "point"}, {"name": "You", "expr": "sleepy", "pose": "stand", "r": 36}],
         "bubbles": [{"who": "Mars", "text": "Today: fix the roof, confront the cousin about the land, join the gym, win."}, {"who": "You", "text": "It is six in the morning."}]},
        {"chars": [{"name": "Mars", "expr": "proud", "pose": "arms_up"}, {"name": "You", "expr": "surprised", "pose": "stand", "r": 36}],
         "bubbles": [{"who": "Mars", "text": "Then you are late."}]},
        {"chars": [{"name": "Mars", "expr": "happy", "pose": "stand"}, {"name": "You", "expr": "proud", "pose": "arms_up", "r": 36}],
         "bubbles": [{"who": "You", "text": "Seven years of this and I own property, I have muscles, and the cousin and I are not speaking."},
                     {"who": "Mars", "text": "Two out of three. Good season."}]},
    ]},

"ch09-comic": {
    "title": "The Rahu season: the great churning",
    "panels": [
        {"chars": [{"name": "Rahu", "expr": "sly", "pose": "point"}, {"name": "You", "expr": "surprised", "pose": "stand", "r": 36}],
         "bubbles": [{"who": "Rahu", "text": "You need this. And that. And a visa. And a bigger phone. And to be famous, slightly."}]},
        {"chars": [{"name": "Rahu", "expr": "happy", "pose": "wave"}, {"name": "You", "expr": "worried", "pose": "think", "r": 36}],
         "bubbles": [{"who": "You", "text": "I did not want any of this yesterday."}, {"who": "Rahu", "text": "Yesterday you were not in my season."}]},
        {"caption": "Eighteen years later.",
         "chars": [{"name": "Rahu", "expr": "calm", "pose": "stand"}, {"name": "You", "expr": "calm", "pose": "sit", "r": 36}],
         "bubbles": [{"who": "You", "text": "Half of what I chased was smoke. The other half built my whole life."}, {"who": "Rahu", "text": "That is the deal. I never said which half."}]},
    ]},

"ch10-comic": {
    "title": "The Jupiter season: growth and grace",
    "panels": [
        {"chars": [{"name": "Jupiter", "expr": "happy", "pose": "wave"}, {"name": "You", "expr": "calm", "pose": "stand", "r": 36}],
         "bubbles": [{"who": "Jupiter", "text": "Let us learn something. Let us teach something. Let us have a child, or a garden, or a very large idea."}]},
        {"chars": [{"name": "Jupiter", "expr": "proud", "pose": "point"}, {"name": "You", "expr": "worried", "pose": "stand", "r": 36}],
         "bubbles": [{"who": "You", "text": "I am forty-five."}, {"who": "Jupiter", "text": "Exactly. Finally old enough to be a beginner properly."}]},
        {"chars": [{"name": "Jupiter", "expr": "sly", "pose": "stand"}, {"name": "You", "expr": "surprised", "pose": "think", "r": 36}],
         "bubbles": [{"who": "You", "text": "Why do my trousers not fit?"}, {"who": "Jupiter", "text": "Growth, my child. I never said where."}]},
    ]},

"ch11-comic": {
    "title": "The Saturn season: the long audit",
    "panels": [
        {"chars": [{"name": "Saturn", "expr": "calm", "pose": "point"}, {"name": "You", "expr": "worried", "pose": "stand", "r": 36}],
         "bubbles": [{"who": "Saturn", "text": "Where were you in 2014?"}, {"who": "You", "text": "...sleeping?"}]},
        {"chars": [{"name": "Saturn", "expr": "calm", "pose": "stand"}, {"name": "You", "expr": "sad", "pose": "stand", "r": 36}],
         "bubbles": [{"who": "Saturn", "text": "Noted. We will do it properly this time. Slowly. With receipts."}]},
        {"caption": "Nineteen years later.",
         "chars": [{"name": "Saturn", "expr": "happy", "pose": "stand"}, {"name": "You", "expr": "proud", "pose": "arms_up", "r": 36}],
         "bubbles": [{"who": "You", "text": "A house. A craft. People who trust me. I hate that you were right."}, {"who": "Saturn", "text": "Everyone does. Then they thank me. Then they forget. Then I come back."}]},
    ]},

"ch12-comic": {
    "title": "The Mercury season: the clever years",
    "panels": [
        {"chars": [{"name": "Mercury", "expr": "happy", "pose": "arms_up"}, {"name": "You", "expr": "surprised", "pose": "stand", "r": 36}],
         "bubbles": [{"who": "Mercury", "text": "New course! New side business! New language! A podcast! Also I replied to your aunt, you are welcome."}]},
        {"chars": [{"name": "Mercury", "expr": "proud", "pose": "point"}, {"name": "You", "expr": "worried", "pose": "think", "r": 36}],
         "bubbles": [{"who": "You", "text": "Can we please do one thing at a time?"}, {"who": "Mercury", "text": "We are doing one thing. Seventeen times."}]},
        {"chars": [{"name": "Mercury", "expr": "calm", "pose": "stand"}, {"name": "Saturn", "expr": "calm", "pose": "stand", "r": 34}, {"name": "You", "expr": "calm", "pose": "stand", "r": 32}],
         "bubbles": [{"who": "Mercury", "text": "I take the colour of my company. Sit me next to Saturn and I become an accountant."}, {"who": "Saturn", "text": "A good one."}]},
    ]},

"ch13-comic": {
    "title": "Same planet, different room",
    "panels": [
        {"caption": "Saturn, sitting in your 10th room: the office.",
         "chars": [{"name": "Saturn", "expr": "proud", "pose": "stand"}, {"name": "You", "expr": "happy", "pose": "stand", "r": 36}],
         "bubbles": [{"who": "Saturn", "text": "Here I am at home. Promotions, slowly. Respect, slowly. But it stays."}]},
        {"caption": "Saturn, sitting in your 7th room: the guest wing, where the partner lives.",
         "chars": [{"name": "Saturn", "expr": "calm", "pose": "think"}, {"name": "You", "expr": "worried", "pose": "stand", "r": 36}],
         "bubbles": [{"who": "Saturn", "text": "Same me. Different room. Love arrives late and stays long. Patience is the fee."}]},
        {"chars": [{"name": "You", "expr": "surprised", "pose": "point", "r": 38}, {"name": "Saturn", "expr": "calm", "pose": "stand"}],
         "bubbles": [{"who": "You", "text": "So before I panic about a season, I should check which room its planet is sitting in?"}, {"who": "Saturn", "text": "And whether it is on your side. And who it is sitting with. Three questions. Then panic, if you must."}]},
    ]},

"ch14-comic": {
    "title": "Weather inside the season",
    "panels": [
        {"caption": "Venus is running the house. Then Saturn walks past the window, overhead, for two and a half years.",
         "chars": [{"name": "Venus", "expr": "calm", "pose": "wave"}, {"name": "Saturn", "expr": "calm", "pose": "stand", "r": 34}, {"name": "You", "expr": "worried", "pose": "stand", "r": 32}],
         "bubbles": [{"who": "Venus", "text": "Ignore him, darling. He is just passing."}, {"who": "Saturn", "text": "Two and a half years of passing."}]},
        {"chars": [{"name": "You", "expr": "worried", "pose": "point", "r": 38}, {"name": "Venus", "expr": "calm", "pose": "stand"}],
         "bubbles": [{"who": "You", "text": "So is this a Venus time or a Saturn time?"}, {"who": "Venus", "text": "A Venus season with Saturn weather. Carry an umbrella. Keep the party."}]},
        {"chars": [{"name": "Jupiter", "expr": "happy", "pose": "wave", "r": 36}, {"name": "Saturn", "expr": "calm", "pose": "stand", "r": 34}, {"name": "You", "expr": "happy", "pose": "arms_up", "r": 32}],
         "bubbles": [{"who": "Jupiter", "text": "And when he and I both look at the same room in the same year, something gets signed."}, {"who": "Saturn", "text": "Two signatures. Then it is real."}]},
    ]},

"ch15-comic": {
    "title": "The changeover",
    "panels": [
        {"caption": "The last year of a Venus season.",
         "chars": [{"name": "Venus", "expr": "sad", "pose": "stand"}, {"name": "You", "expr": "worried", "pose": "stand", "r": 36}, {"name": "Sun", "expr": "calm", "pose": "wave", "r": 34}],
         "bubbles": [{"who": "Venus", "text": "I am packing. Not everything. Just the things you no longer need."}, {"who": "Sun", "text": "I am early. Is that a problem?"}]},
        {"chars": [{"name": "You", "expr": "worried", "pose": "point", "r": 38}, {"name": "Venus", "expr": "calm", "pose": "stand", "r": 34}, {"name": "Sun", "expr": "calm", "pose": "stand", "r": 34}],
         "bubbles": [{"who": "You", "text": "Can you two overlap for a bit? I am not ready."}, {"who": "Sun", "text": "That overlap is the awkward year. Everyone feels it."}]},
        {"chars": [{"name": "Sun", "expr": "proud", "pose": "point"}, {"name": "You", "expr": "calm", "pose": "stand", "r": 36}],
         "bubbles": [{"who": "Sun", "text": "Write her a thank-you letter. Then write me a list of what you want to be known for. We start Monday."}]},
    ]},

"ch16-comic": {
    "title": "Three lives, three seasons, one October",
    "panels": [
        {"caption": "Meera, 37. Venus season, last year. Sun at the door.",
         "chars": [{"name": "You", "expr": "calm", "pose": "think", "r": 36, "label": False}, {"name": "Venus", "expr": "calm", "pose": "wave", "r": 34}],
         "bubbles": [{"who": "You", "text": "Twenty years of this. Marriage, a home, a practice. Now I keep wanting my own name on the door."}]},
        {"caption": "Arjun, 31. Rahu season, Venus sub-season.",
         "chars": [{"name": "Rahu", "expr": "sly", "pose": "point", "r": 40}],
         "bubbles": [{"who": "Rahu", "text": "Research abroad. Or marriage. Or both. Why choose? Choosing is for other seasons."}]},
        {"caption": "Devika, 47. Rahu season, Saturn sub-season beginning.",
         "chars": [{"name": "Saturn", "expr": "calm", "pose": "stand", "r": 40}],
         "bubbles": [{"who": "Saturn", "text": "The property matter, the health matter, the daughter's exams. One file at a time. I have brought a chair."}]},
    ]},

"ch17-comic": {
    "title": "Living well in a hard season",
    "panels": [
        {"chars": [{"name": "You", "expr": "sad", "pose": "stand", "r": 38}, {"name": "Saturn", "expr": "calm", "pose": "stand"}],
         "bubbles": [{"who": "You", "text": "Everyone says your season is a punishment."}, {"who": "Saturn", "text": "I am not here to punish you. I am here to show you what is already paid, and what is still owed."}]},
        {"chars": [{"name": "You", "expr": "worried", "pose": "point", "r": 38}, {"name": "Rahu", "expr": "sly", "pose": "stand"}],
         "bubbles": [{"who": "You", "text": "And a man on the internet says a stone will fix you."}, {"who": "Rahu", "text": "That man is me, in a different season. Keep your money. Fix your routine."}]},
        {"chars": [{"name": "Ketu", "expr": "calm", "pose": "sit"}, {"name": "You", "expr": "calm", "pose": "sit", "r": 38}],
         "bubbles": [{"who": "You", "text": "So what do I actually do in a hard season?"}, {"who": "Ketu", "text": "The task of the season. Every day. Smaller than you think. Longer than you like."}]},
    ]},

"ch18-comic": {
    "title": "Your season map",
    "panels": [
        {"caption": "You, with an app printout and a pencil.",
         "chars": [{"name": "You", "expr": "calm", "pose": "think", "r": 40}],
         "bubbles": [{"who": "You", "text": "Mercury till eleven. Ketu till eighteen. Venus till thirty-eight. Marriage here. The bad year here. The move here."}]},
        {"chars": [{"name": "You", "expr": "surprised", "pose": "arms_up", "r": 40}],
         "bubbles": [{"who": "You", "text": "Oh. It was never random."}]},
        {"chars": [{"name": "Sun", "expr": "happy", "pose": "wave", "r": 26, "x": 0.12}, {"name": "Moon", "expr": "happy", "pose": "wave", "r": 26, "x": 0.5}, {"name": "Saturn", "expr": "happy", "pose": "wave", "r": 26, "x": 0.88}],
         "bubbles": [{"who": "Moon", "text": "We were here the whole time. Now you know how to read us. Go gently."}]},
    ]},
}
