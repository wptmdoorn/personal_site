---
{
    "title": "Methcomp: the Python package for method comparison",
    "short_title": "methcomp",
    "pub_date": "2020-03-09",
    "last_mod": "2024-02-05",
    "author": "William van Doorn"
}
---

<div class="row">
<img src="/02_methcomp/methcomp1.png" style="width: 30%; height:auto; margin: 10px" />
<img src="/02_methcomp/methcomp3.png" style="width: 30%; height:auto; margin: 10px" />
<img src="/02_methcomp/methcomp4.png" style="width: 30%; height:auto; margin: 10px" />
</div>

# Methcomp: the Python package for method comparison

## Introduction
Laboratory medicine is amongst the fastest growing specialities in medicine, being crucial in the diagnosis, prevention and in monitoring of
disease states for individual patients, as well as for the evaluation of treatment for populations of patients [1]. High quality and safety in laboratory testing has
therefore a crucial role in modern healthcare. Validation, comparison and verification of current and new laboratory tests is thus essential to maintain high quality and safe laboratory tests [2]. In the process of validating a laboratory test, we often employ (statistical) tools (i.e. method comparison software) to assist us making decisions about the new laboratory test. To the best of our knowledge, there is no such publicly available software tool to do this 
in the Python programming language.  

The Python programming language was invested in the 1990s by Guido van Rossum [3]. Although it has been available for such a long time, its popularity really took of when
the latest version of Python was released back in 2008 (Python 3) [4]. Python as we know today has first-class integration with a lot low of level systems (e.g. clinical chemistry analyzers), can easily handle CPU heavy tasks and has powerful toolsets for mathematics, statistics and computer science. Not only does this provide us with direct access to the systems we use in our laboratories, but also can it be used for a lot of automation, machine learning and extensive data analysis on-site. 
Python is especially interesting for method comparison as it would allow us to directly validate and compare new methods on the system itself rather than having to analyze it in a later stage using a distinctive tool (i.e. R or even Excel). Additionally, having access to these tools directly in Python also allows us to monitor
and validate new, innovative techniques such as clinical decision support using machine learning. Recently, we aimed to develop 
a new public software package called `methcomp` which is designed to fill this gap.

## Methcomp
Methcomp is a Python software package designed to provide users with an easy-to-use, flexible interface to perform method comparison,
validation and verification. It allows us to create a variety of method comparison visualizations using simple, straight-forward interface. 
Methcomp is easily accessible by downloading it from the Python software repository
(direct link is [here](https://pypi.org/project/methcomp/)) using the command: 

```python
pip install methcomp
```

Source code for the project is available through [Github](https://github.com/wptmdoorn/methcomp). In this blog post, we will describe
a few examples using the methcomp software library:
1. Scatter plot with regression  
2. Difference plots   
3. Glucose sensor error grids   

## Scatter plots: Passing-Bablok and Deming
A frequently used approach to compare two methods is by producing a scatter plot with a regression line to examine
the relationship between the first and second method. Although linear regression is often used, it has serious drawbacks which
limits the use in method comparison. Deming [5, 6] and Passing-Bablok [7] regression are statistical techniques that allow, in contrast to
linear regression, random measurement errors in the X-axis values. In the case of Deming regression, the assumption is made that these errors
are normally distributed, and in case of Passing-Bablok, no assumptions are made. Using the methcomp software package, we can easily create these
plots; beneath we describe an example for Deming regression.

```python
method1 = [x * uniform(1, 1.5) for x in range(2, 50)] # Generate 50 random measurements for method 1 with some noise
method2 = [x * uniform(1, 1.5) for x in range(2, 50)] # Generate 50 random measurements for method 2 with some noise
deming(method1, method2, CI=0.95) # Generate plot
plt.show() # Show plot on screen
```

This code will result in the following graphical visualizations; shown for Deming (left) and Passing-Bablok (right).

<div class="row">
<img src="/02_methcomp/deming.png" alt="drawing" style="width: 45%; margin: 10px"/> 
<img src="/02_methcomp/pb.png" alt="drawing" style="width: 45%; margin: 10px"/> 
  <span style="color:gray; font-size:0.8em;"><b>Figure 1:</b> Illustrative examples of Deming (left) and Passing-Bablok (right) on a random
generated dataset of measurements for method 1 and method 2. Shaded areas present the 95% confidence interval for both regression lines. </span>
</div>

##  Difference plots: Bland-Altman
A second approach to method comparison is to provide information about the actual "difference" between two methods, often carried out with "Bland-Altman" plots [8, 9]. 
Bland-Altman plots depict the differences (or alternatively the ratios) between the two methods which are plotted against the averages of the methods. 
Horizontal lines are drawn at the mean difference and at the limits of agreement, which are defined as the mean difference +/- 1.96 times the standard deviation of the differences (although this can be altered in specific context). Bland-Altman plots especially excel in detecting bias and therefore are often used complementary to regression analysis. Once again, generating a Bland-Altman plot is very straightforward using the methcomp package:

```python
method1 = [x * uniform(1, 1.5) for x in range(2, 50)] # Generate 50 random measurements for method 1 with some noise
method2 = [x * uniform(1, 1.5) for x in range(2, 50)] # Generate 50 random measurements for method 2 with some noise
blandaltman(method1, method2, difference='absolute', CI=0.95) # Generate Bland-Altman plot
plt.show() # Show plot on screen
```

This code results in the following Bland-Altman plots s with absolute (left) and relative (right) differences. 

<div class="row">
<img src="/02_methcomp/blandaltman_abs.png" alt="drawing" style="width: 45%; margin: 10px"/> 
<img src="/02_methcomp/blandaltman_rel.png" alt="drawing" style="width: 45%; margin: 10px"/>  
  <span style="color:gray; font-size:0.8em;"><b>Figure 2:</b> Illustrative examples of Bland-Altman plots for the absolute (left) and relative
differences (right) on a random generated dataset of measurements for method 1 and method 2. Shaded areas present the 95% confidence interval for mean and limit of
agreement lines.</span>
</div>

## Glucose sensor error grids
The third current available feature of methcomp is designed for method comparison in a specific field, namely glucose sensor measurement comparisons. Glucose sensor error grids, defined by Clarke (1987) [9] and Parkes (2000) [10, 11], are specifically designed as a method comparison tool for reference
and new blood glucose measurement systems. These graphical plots are simple scatter plots complemented with a Cartesian grid which labels each of the points to a specific zone. Each of these zones has a different clinical interpretation and consequence, allowing us to do a clinical evaluation of the new versus the old
method. For instance, values that are in zones C to E can potentially lead to dangerous situations causing harm for the individual wearing the glucose sensor. 
To construct a Clarke error grid using the methcomp package we use the following code: 

```python
sensor1 = [x * uniform(1, 1.5) for x in range(2, 50)] # Generate 50 random glucose measurements for sensor 1 
sensor2 = [x * uniform(1, 1.5) for x in range(2, 50)] # Generate 50 random glucose measurements for sensor 2
clarke(sensor1, sensor2, units='mmol') # Generate Clarke plot
plt.show() # Show plot on screen
```

This will result in the plot we observe left in the example below. Moreover, we can use the same set of measurements to create Parkes error grid plot which is shown 
in the right picture. 

<div class="row">
<img src="/02_methcomp/clarke.png" alt="drawing" style="width: 45%; margin: 10px"/> 
<img src="/02_methcomp/parkes.png" alt="drawing" style="width: 45%; margin: 10px"/> 
  <span style="color:gray; font-size:0.8em;"><b>Figure 3:</b> Illustrative examples of Clarke (left) and Parkes (right) error grids on a random set of
measurements from an old versus a new glucose sensor system. Zone A and B depict clinically safe zones, whilst zones C to E are potentially dangerous (see 
respective papers for detailed description of zones [9-11].</span>
</div>

## Conclusion
Method comparison, validation and verification is crucial for modern clinical laboratories. Unfortunately, method comparison tools were not publicly available in the
Python programming language to date. In this blog post we introduce [methcomp](https://pypi.org/project/methcomp/), a new publicly available Python software package. 
Using the methcomp interface, we discussed and created three different type of method comparison visualization plots.

**References**
1. Seyhan, A.A., Carini, C. Are innovation and new technologies in precision medicine paving a new era in patients centric care?. J Transl Med 17, 114 (2019). https://doi.org/10.1186/s12967-019-1864-9  
2. Jensen, A. L., & Kjelgaard-Hansen, M. (2006). Method comparison in the clinical laboratory.   Veterinary Clinical Pathology, 35(3), 276–286. https://doi.org/10.1111/j.1939-165x.2006.tb00131.x 
3. van Rossum, G., Python tutorial, Technical Report CS-R9526, Centrum voor Wiskunde en Informatica (CWI), Amsterdam, May 1995  
4. http://pypl.github.io/PYPL.html. Consulted on 16 March, 20120.  
5. Koopmans, T. C. (1937). Linear regression analysis of economic time series. DeErven F. Bohn, Haarlem, Netherlands.  
6. Deming, W. E. (1943). Statistical adjustment of data. Wiley, NY (Dover Publications edition, 1985).  
7. Passing H and Bablok W. J Clin Chem Clin Biochem, vol. 21, no. 11, 1983, pp. 709 - 720  
8. Altman, D. G., and Bland, J. M. Series D (The Statistician), vol. 32, no. 3, 1983, pp. 307–317.  
9. Altman, D. G., and Bland, J. M. Statistical Methods in Medical Research, vol. 8, no. 2, 1999, pp. 135–160.  
10. Clarke, W. L., Cox, D., et al. Diabetes Care, vol. 10, no. 5, 1987, pp. 622–628.  
11. Parkes, J. L., Slatin S. L. et al. Diabetes Care, vol. 23, no. 8, 2000, pp. 1143-1148.  
12. Pfutzner, A., Klonoff D. C., et al. J Diabetes Sci Technol, vol. 7, no. 5, 2013, pp. 1275-1281.  