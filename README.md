# Song Sentiment Analyzer


## Overview


* Description
* Motivation
* Code execution
* Code implementation
* Author

## 1. Description

Construct of a song sentiment analyzer. This analyzer is able to receive the name of a music group or artist as an input and create an initial dataset with the lyrics of all the songs of it. This dataset is later used to analyze the lyrics of each song with the LLM Bert Model from Google to give a score of the sentiment. Finally, we can visualize with plots the evolution of one or more groups through the years and all the songs of one specific group.

## 2. Motivation

Most music groups evolve through the years their style and their approach to music. This can be spotted looking into its lyrics. However, obtaining all the lyrics and manually analyze them to study their evolution and their differences with other groups can be a very tedious.

For that purpose, SongSentimentAnlyzer is able to create a dataset with the songs, albums and lyrics for a vast number of music artists and visualize their sentiment evolution after carefully analyzing the meaning of their lyrics.

## 3. Code execution

It is very easy to execute the pipeline of this project. First, we need to select a music artist and confirm that this artist has a page on `azlyrics.com`, which is the web page where the lyrics are obtained from.

Then we can execute the following command to create the dataset.

```bash
python create_initial_dataset.py -group-name  <group_name>
```

The group name should be in lowercase and without whitespaces. It's also worth mentioning that to avoid saturating the `azlyrics.com` page, we only load a song every 15 seconds. Therefore, for very prolific groups, the creation of the dataset can last a lot. However, it won't consume a lot of CPU resources as most of the time will be sleeping.

The next step is to analyze the lyrics to create the dataset that won't contain the lyrics and will have the score for every song indicating its sentiment (1 will be fully positive and 0 will be fully negative).

```bash
python songs_sentiment_analysis.py -group-name <group_name>
```

Finally, we can visualize the plots with `matplotlib` a multiple plot with the evolution through the years of several groups and a single plot that will show all the songs of a specific group.

```bash
python songs_sentiment_plot.py -single <group_name> -multiple <group_name1> <group_name2> ...
```

## 4. Code implementation

As it has been commented, the code contains 3 sepparated sections.

### 4.1. Create initial dataset

Once the name of the music artist is received, this program will load the html containing the web page of that group on `azlyrics.com`. Thanks to this html, we will get the name and the url for every song. For each one of them, we will get the name of the album and the year that album was released. In case the song has been released as a single, the album will be single, and the year will be 0. This is a mark that indicates that this song is not going to be counted for the later plots (even though its sentiment score will still be computed).

We will also get the lyrics of the song parsed after wiping all tokens that are not actually part of the lyrics and are just part of the html grammar.

Finally, we will have a dataset for the specified group with one row per song and the name, album, url, release year and lyrics of the song on that row.

### 4.2. Song sentiment analysis

To carry out the song sentiment analysis of one specific group, we will compute a score from 0 to 1 (1 will be fully positive and 0 will be fully negative) for each song and save the same dataset we have previously created substituting the lyrics of each song by this score.

To compute this score, we will use the Large Language Model called `distilbert-base-uncased-finetuned-sst-2-english`, which comes from the Bert base model, by Google. This model is able to get a sequence of words and generate an embedding with multiple dimensions for each one of them. It has been trained with a large amount of English text and is able to understand the meaning of these words and place them into an abstract space where the sequence of words with similar meanings will be close to each other.

DistilBERT is, as its paper explains, a distilled version of BERT: smaller, faster, cheaper and lighter that reduces the size of the BERT model by 40% and retains the 97% of its language understanding. On top of this model, it has been added an extra layer of complexity that finetunes this model to predict the sentiment of a sentence. This final model has been trained with SST (Stanford Sentiment Treebank) dataset that contains sentences and a label equal to 0 for negative sentences and 1 for positive sentences.

Each sentence of the song lyrics is passed through this model, returning logits with the negative and positive charge. This is passed through a softmax to return the probability of being positive and negative, that add up to 1. These scores are finally added to a dataset that is saved with -scores suffix.

### 4.3. Songs sentiment plot

With this program, we can visualize a multiple plot that shows for every group a line with the evolution with the years as the X axis and the Y axis as the positive sentiment of the lyrics of the album released that year (which is the average of the songs of that album).

The single plot shows the same X and Y axis, but we have a scatter plot with a point for each song a specific music group.

## 5. Author

Sergi Pérez Escalante