
<h1 align="center">
IS 597 Programing for Analytics & Data Processing
</h1>

<h1 align="center">
Type II Final Project
</h1>  

<br>
<br>

<p align="center">

**Crime and Arrest Data Analysis in Los Angeles**

</p>

<p align="center">

Harsh Salvi & Divya Sharma

</p>

![alt text](https://ca-times.brightspotcdn.com/dims4/default/19db5e3/2147483647/strip/true/crop/3751x2407+0+0/resize/840x539!/quality/90/?url=https%3A%2F%2Fcalifornia-times-brightspot.s3.amazonaws.com%2Fbe%2F8f%2Fc89aab314076b84ea3544039311a%2Fla-photos-1staff-460618-lme-triple-shooting01-als.JPG)

## Team Members

Harsh Salvi - hsalvi2@illinois.edu 

Divya Sharma - dsharm31@illinois.edu

## Overview

Los Angeles County is the most populous in the Unites States as per [Wikipedia](https://en.wikipedia.org/wiki/Los_Angeles_County,_California). Its population is 10.04 million as of the 2019 Cencus data. With such a high population, investigating crime rates and factors related to it is a common thought. Since this area has been widely analyzed upon, we decided to use these specific dataset combinations which have very little public analyses performed on them. We have four hypotheses, in which we test factors commonly related to crime. We use [Numba](http://numba.pydata.org/) to optimize performance of one of the preprocessing functions which significantly reduces the calculation time by approximately 9 times.

## Datasets

[Crime and Arrest Data for LA County](https://www.kaggle.com/cityofLA/los-angeles-crime-arrest-data?select=crime-data-from-2010-to-present.csv)

[Los Angeles Census Data](https://www.kaggle.com/cityofLA/los-angeles-census-data)

[LA County Median Income Data](http://www.laalmanac.com/employment/em12c.php)

[Full Moon Calendar](https://www.kaggle.com/lsind18/full-moon-calendar-1900-2050)

[Daylight Savings Time Periods](https://en.wikipedia.org/wiki/Daylight_saving_time_in_the_United_States)

[LA County Race Populations](https://datausa.io/api/data?Geography=05000US06037&drilldowns=Race,Ethnicity&measures=Hispanic%20Population,Hispanic%20Population%20Moe)

# Hypotheses

## Hypothesis 1 : Areas with a higher black population have higher arrests based on Homicide

<p align="center">

<img src="https://github.com/harsh-bat/2021_Spring_finals/blob/main/pics/races.jpg">

</p>

## Results

<p align="center">

<img src="https://github.com/harsh-bat/2021_Spring_finals/blob/main/pics/hypo1.png">

</p>

### Conclusion : There is some relation between homicide arrest rate and black population percentage. We fail to reject hypothesis 1.

## Hypothesis 2: Zip Codes with higher median household income have a lower crime rate

<p align="center">

<img src="https://github.com/harsh-bat/2021_Spring_finals/blob/main/pics/income.jpg">

</p>

## Results

<p align="center">

<img src="https://github.com/harsh-bat/2021_Spring_finals/blob/main/pics/hypo2.png">

</p>

### Conclusion : No strong relation between median household income and crime rate. We reject hypothesis 2.

## Hypothesis 3: Crime Rate for some crimes decreases more than 10% during daylight savings time

<p align="center">

<img src="https://github.com/harsh-bat/2021_Spring_finals/blob/main/pics/daylight.jfif">

## Results

</p>
<p align="center">

<img src="https://github.com/harsh-bat/2021_Spring_finals/blob/main/pics/hypo3a.png">

</p>
<p align="center">

<img src="https://github.com/harsh-bat/2021_Spring_finals/blob/main/pics/hypo3b.png">

</p>

### Conclusion : Crime rate decreses more than 10% during DST for Identity Theft crimes. We fail to reject hypothesis 3.

## Hypothesis 4: Crime Rate for some crimes increases more than 10% on a full moon night

<p align="center">

<img src="https://github.com/harsh-bat/2021_Spring_finals/blob/main/pics/fullmoon.jpg">

## Results

</p>
<p align="center">

<img src="https://github.com/harsh-bat/2021_Spring_finals/blob/main/pics/hypo4.png">

</p>

### Conclusion : Crime rate for no crimes increases more than 10% on a full moon night. Hence, we reject hypothesis 4.

## References

[Numba Documentation -  Compiling Python code with @jit](https://numba.pydata.org/numba-doc/latest/user/jit.html)
[Pandas Documentation](https://pandas.pydata.org/docs/user_guide/index.html#user-guide)
[Pandas Correlation Groupby](https://stackoverflow.com/questions/28988627/pandas-correlation-groupby)
