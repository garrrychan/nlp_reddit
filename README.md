# nlp_reddit

What's the difference between a life pro tip, and one that is a bit more questionable? This can be sometimes a subtle difference, or a moral grey area to distinguish, even for humans.

> Life Pro Tip:
A concise and specific tip that improves life for you and those around you in a specific and significant way.


Example: "If you want to learn a new language, figure out the 100 most frequently used words and start with them. Those words make up about 50% of everyday speech, and should be a very solid basis."

> An Unethical Life Pro Tip is a tip that improves your life in a meaningful way, perhaps at the expense of others and/or with questionable legality. Due to their nature, do not actually follow any of these tips–they're just for fun.


Example: "Save business cards of people you don't like. If you ever hit a parked car accidentally, just write "sorry" on the back and leave it on the windshield."

I've collected over 1960 total top posts (web scrap) from 2 subreddits, and created a machine learning model using Natural Langauge Processing (NLP) to classify which subreddit a particular post belongs too.


Can my model pick up on sarcasm, internet 'trolling', or tongue-in-cheek semantic of sentences? Probably not, but let's try. I hope you have as much fun playing with this, as I did making it.

If you're feeling lucky, visit my app for a Life Pro Tip!
https://nlp-reddit-garry.herokuapp.com/


# tldr 
| Classification Model  | Training Accuracy %  | Test Accuracy %  
|---|---|---|
| Baseline |	0.5	| 0.5 |
| Logistic |	0.999 |	0.895 |
| Naive Bayes	| 0.995	| 0.805 |
| Support Vector Machines |	0.920 |	0.903 |

Given these results, my selected production model was the logistic regression model with CountVectorizer as the vectorizer. The Logistic Model is nearly the most performant, but also provides a high level of interpret-ability compared to SVM.

In conclusion:
* The more 'popular' i.e. more comments and score, the great likelihood that it is unethical. Controversial posts tend to gain more popularity.

* In this training set, if the document includes the word 'business', then the likelihood of being unethical is far more likely by 3x. There's probably a lot of unethical comments around taking advantage of businesses!
