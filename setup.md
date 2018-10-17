General intro
=============
* Everybody uses text prediction.
* Text prediction is machine learning.
* kNN is simple: you just compare to a large collection of previously seen language.
* Because there are so many different things you can say, very often there won't be anything similar in the dataset. In that case we pick the highest item in a frequency list.
* Let's try to predict some tweets of the most popular twitter users on earth.

Interaction #1: explain the prediction engine
---------------------------------------------
* x different example tweets, each by a different user (or do we want multiple tweets per user?)
* You can select a tweet, and then go forward and backward while typing
* At each stage, the left context has another color, and the y most similar left contexts with a still matching prediction are seen
* If there is no context, we show the best we've got from the frequency list
* Used language model is left unspecified
* To decide: if multiple contexts lead to the same prediction, do we show them all?



Language models
===============
* This whole idea is a very simple kind of statistical language model. 
* Built up completely based on example language data. If you put in different data, you get another model. 
* We can make language models based on a number of different twitter accounts, and you'll see they would all finished 

Interaction #2: explain language modeling
-----------------------------------------
* Mostly same as interaction #1 (even the same tweets?)
* Difference 1: you only see the best matching prediction (or predictions?) of a language model
* Difference 2: you see multiple language models, preferably the language models of all authors of all example tweets
* Possibly: also a general language model



Personalization & evaluation
============================
* Some language models give better predictions than others.
* You might have noticed that the personal language model always wins. 
* (That's by the way why we are using Twitter, it's a huge collection of language organized by language user).
* Instead of eyeballing it, we can also count: we can quite easily calculate which language model had their predicted letter correct than others
* Let's do that for z example tweets per user

Interaction #3: explain eval
-----------------------------
* Show y different twitter users the users can pick from
* When selecting, you see the scores for a number of ranked language models
* There is also a visualization (colored dots?) to see how z example tweets did. When you hover the visualization, you see the actual tweet




More data
=========
* The more material you have, the more likely it is that the example you need was in the training material
* You can see that if we artifically remove some training material: the predictions get worse
* This is why the predictions from Taylor Swift's model is so bad at predicting any other tweets than its own: because there are so few tweets, the chance that there is a context useful for a new prediction is just too small. 

Interaction #4: show you need more
----------------------------------
* Mostly same as interaction #3
* Difference: smaller personal language models for each tweet



Sociolinguistics
================
* It would of course be best if we add tweets by people that tweet really similar; in a similar style about a similar topic. Who would that be? Sociolinguistics says: people who talk to each other a lot.
* You can have an estimate of people who talk to each other a lot by looking at @-mentions on Twitter.
* We can make an overview of the percentage of overlapping words in each pair of two Twitter accounts (Jaccard index), where accounts with more overlapping words are more closely together.
* If you hover, you can see who actually talk to each other
* You see that, indeed, people who talk to each other use more overlapping words.

Interaction #5: friends talk similar
------------------------------------
* Connection graph
* If you hover a dot, friends light up.



Sociolect
=========
* It works! If we extend language models with the tweets of friends, it works better than just adding random tweets.

Interaction #6: show you need more
----------------------------------
* Mostly same as interaction #4
* Difference: sociolect language models versus random language models



Outro
=====
* Language transplantation