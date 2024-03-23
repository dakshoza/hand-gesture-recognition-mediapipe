user_score_dictionary = {
    "Sorry": -2,
    "Thank you": 3,
    "Please": 2,
    "Excuse me": -1,
    "Welcome": 2,
    "Hello": 3,
    "Goodbye": 2,
    "Good morning": 3,
    "Good night": 3,
    "Namaste": 3,
    "May I help you": 1,
    "Wait": 0,
    "Repeat": 0,
    "Thank you very much": 4,
    "Like": 2,
    "Don't like": -1,
    "Love": 4,
    "Hate": -3,
    "Enjoy": 3,
    "Happy": 4,
    "Sad": -3,
    "Angry": -2,
    "Surprised": 1,
    "Tired": -1,
    "Rice": 2,
    "Bread": 1,
    "Water": 3,
    "Vegetables": 2,
    "Fruit": 3,
    "Wake up": 2,
    "Brush teeth": 1,
    "Eat": 3,
    "Work": 0,
    "Sleep": 4
}

category_word_dictionary = {
    "Manners and Etiquettes": [
        "Sorry",
        "Thank you",
        "Please",
        "Excuse me",
        "Welcome"
    ],
    "Greetings and Salutations": [
        "Hello",
        "Goodbye",
        "Good morning",
        "Good night",
        "Namaste"
    ],
    "Polite Phrases": [
        "May I help you",
        "Sorry",
        "Wait",
        "Repeat",
        "Thank you very much"
    ],
    "Likes and Dislikes": [
        "Like",
        "Don't like",
        "Love",
        "Hate",
        "Enjoy"
    ],
    "Feelings and Emotions": [
        "Happy",
        "Sad",
        "Angry",
        "Surprised",
        "Tired"
    ],
    "Food Items": [
        "Rice",
        "Bread",
        "Water",
        "Vegetables",
        "Fruit"
    ],
    "Daily Routine": [
        "Wake up",
        "Brush teeth",
        "Eat",
        "Work",
        "Sleep"
    ]
}

category_vid_dict = {
    "Manners and Etiquettes": "https://youtu.be/n42ohSmbAFI?si=WKTuTmz5y5wvBFW9",
    "Greetings and Salutations": "https://youtu.be/5vHmvYA8Z6Q?si=nn03PxS_QKIBPH0z",
    "Polite Phrases": "https://youtu.be/neE5Fg4FVtA?si=SgbNbb7GNeYci4fJ",
    "Likes and Dislikes": "https://youtu.be/N88aAdNtZu4?si=_mMIICXOnXzQJb-u",
    "Feelings and Emotions": "https://youtu.be/N88aAdNtZu4?si=_mMIICXOnXzQJb-u",
    "Food Items": "https://youtu.be/N88aAdNtZu4?si=_mMIICXOnXzQJb-u",
    "Daily Routine": "https://youtu.be/RdAUR8z2mmM?si=fuIDQSExjZ2IBn58"
}

def return_vid_recs(user_dictionary=user_score_dictionary, 
                    category_word_dictionary=category_word_dictionary, 
                    category_vid_dict=category_vid_dict) -> dict:
    negative_words = [word for word, score in user_dictionary.items() if score < 0]
    category_count = {category: 0 for category in category_word_dictionary}
    result = {}

    for word in negative_words:
        for category, words in category_word_dictionary.items():
            if word in words:
                category_count[category] += 1

    sorted_categories = sorted(category_count.items(), key=lambda x: x[1], reverse=True)

    for category, count in sorted_categories:
        words_in_category = [word for word in negative_words if word in category_word_dictionary[category]]
        if words_in_category:
            words_data = []
            for word in words_in_category:
                words_data.append(word)
            if category in category_vid_dict:
                video_url = category_vid_dict[category]
            else:
                video_url = ""
            result[category] = {"words": words_data, "video_url": video_url}

    return result
