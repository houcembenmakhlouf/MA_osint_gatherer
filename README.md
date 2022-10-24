# Data collection from Twitter Api

This project's purpose is to collect data such as retweets, likes, quotes, replies, and profile information from Twitter Api.
The data input was based on news outlets but any other type of profile could be treated. For this, a csv file is needed under the folder "data" which structure is as follow:

```
name,twitter
Aachener Zeitung / Aachener Nachrichten,az_topnews
```
## data collection process

This project uses scraping software packages. The new version of Twitter API called Twitter API V2 which offers new and more detailed data objects. Python packages such as ``` tweepy, snscrape and twarc2``` are utulized to build a data collector platform. This platform enables the scheduling of queuing jobs for retrieving the needed data and processing them in the background with workers. This part of the work can be extended by adding a user interface to facilitate its usage for non-technical persons.

• SQLite database is utilized in order to save the tweets with their corresponding interactions. The data is organized in the tables as shown in the figure below:

<p align="center">
  <img src="https://user-images.githubusercontent.com/45092804/197497001-997885e8-7770-418e-8b77-ac340fa4de26.png" width="600"/>
</p>


# OSINT-Gatherer

Open source intelligence (OSINT) is the act of gathering and analyzing publicly available data for intelligence purposes.
Purpose: Schedule and monitor simple content collection tasks with queues. Based on [Python-RQ](https://python-rq.org/).

Examples for tasks can be found in [`osint_gatherer/tasks`](osint_gatherer/tasks).

## Requirements

- redis
- pipenv

## Install

```shell
pipenv install
```
or with pip
```
pip install requirements.txt
```

## Run

Starter scripts for frontend, worker and scheduler are provided.

```shell
./run.sh
./run-scheduler.sh
./run-worker.sh
```
