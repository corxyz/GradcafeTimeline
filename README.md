# Gradcafe Timeline

Inspired by [this](https://www.reddit.com/r/gradadmissions/comments/7srxxy/decision_timelines_for_particular_universities/) reddit post on admission timelines for different universities, I decided to go ahead and make a **command line tool for plotting decision timeline based on Gradcafe data**.

- [Features](#features)
- [Getting Started](#getting-started)
- [Example Usage](#example-usage)
- [Contributing](#contributing)
- [Authors](#authors)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- **Gradcafe result timeline plotter** based on admission-related search query
- **Customizable timeline options** (e.g. admission cycle, period, decision type)
- **CLI (Command Line Interface)**, the only interface I understand, kind of

## Getting Started

Please make sure you have all required software/packages installed:

### Prerequisites

- [Python 2.7](https://www.python.org/downloads/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [Matplotlib](https://matplotlib.org/users/installing.html)

## Example Usage

After you have installed all dependencies, navigate to the root directory and start with the following simple command in terminal:
``
$ python main.py -q <query_string>
``

The query string would be the admission-related search you would otherwise enter to search on [Results](https://www.thegradcafe.com/survey/) page of Gradcafe. **Please make sure to wrap your search string in quotes if it contains any whitespace.**

For example, if you would like to see the admission timeline for "computer science", use

``
$ python main.py "computer science"
``

This would give you a graph generated from **all** decision results (**Interview, Accepted, Rejected & Waitlisted**) available on Gradcafe related to "computer science" over all available years. The time line starts in September and ends in August, basically following a typical academic year in US. For an arbitrary point (x,y) on the graph, x is the date (month and day only), and y is the total number of decisions made by that date. The graph looks like the following:

![enter image description here](https://lh3.googleusercontent.com/pgq7c6zNCbYCwylzoIztFVRqihAfHPIgpUsdLj6nlTc8LFLqGchMKjNoBwQy66PfdQJOGT_QnD3w "example_timeline_cs")

If you would like to see the admission timeline for "(yale|"johns hopkins") econ*", use

``
$ python main.py "(yale|\"johns hopkins\") econ*"
``

*Note the backslash("\") in front of quotes as part of the query string.*

### Additional Options (Optional)

The following optional arguments allow you to further narrow down admission results by specifying the admission cycles, admission periods, and decision types to be included in your timeline.

| Variable | Option | Description |
|--|--|--|
| help | `--help`, `-h` | help message about general usage of the cli tool |
| minYear | `--min_year`, `-y` | earliest year from which decision results are included **(default: 2012)** |
| startMonth | `--start_month`, `-s` | start month of timeline (academic year) in integer **(default: 9 (September))** | 
| endMonth | `--end_month`, `-e` | end month of timeline (academic year) in integer **(default: 8 (August))** |
| decisions | `--decisions`, `-d` | type of academic decision **(default: None)**| 

For example, to generate a timeline using admission results associated with "math" starting from 2015 till now, looking at only Accepted and Rejected results dated between January and March, use the command

``
$ python main.pyd "math" -y 2015 -s 1 -e 3 -d "Accepted Rejected"
``

The plot would look like the following:

![enter image description here](https://lh3.googleusercontent.com/cdNL6yA6byxkD4_qt4mbLSqAzSA15pwsst_c7Ae2Lguu-gHljqN49SIFFOxXW4nXt9j3evkBLgV_ "example-math-2015-jan-march-ar")
 
## Contributing

TBA

## Authors

Corey Zhou aka amecolli

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Inspired by [u/un_deaddy](https://www.reddit.com/user/un_deaddy)'s reddit [post](https://www.reddit.com/r/gradadmissions/comments/7srxxy/decision_timelines_for_particular_universities/)
* Adapted from [GradcafeWatcher](https://github.com/utkarshsimha/GradcafeWatcher)
* Unconditional mental support I received during the 2019 grad school admission cycle
