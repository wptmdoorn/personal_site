---
{
    "title": "How do we trust Machine Learning algorithms in Medicine?",
    "short_title": "Uncertainty Quantification in Healthcare",
    "pub_date": "2019-09-01",
    "last_mod": "2024-02-05",
    "author": "William van Doorn"
}
---

<p align="center">
  <img src="/01_uncertainty/fig1.png" alt="drawing" width="80%"/> <br>
</p>

# How do we trust Machine Learning algorithms in Medicine?

### Introduction 

Recent advancements in machine learning (ML) have cleared the path to the deployment of machine learning-based decision support systems in a wide variety of areas including medicine. A substantial number of these systems have proven to achieve superior performance compared to classical systems and/or medical specialists. Yet, most of these systems are not implemented for daily clinical care because they still lack several other important features. One of these features is the **degree of trust** a medical specialist can, or rather should, have in the prediction of an algorithm. For example, consider the situation where an algorithm predicts the day of re-admission to assist a clinical specialist in deciding if a patient can be discharged or not. Currently, most machine learning algorithms output a so-called "point" prediction (_Figure 1A_) which does not provide us with an estimate of the uncertainty concerning the prediction. Recently, numerous research groups describe "probabilistic" algorithms (_Figure 1B_) which output a probability distribution amongst the prediction, resulting in a convenient way to quantify the uncertainty. 

<p align="center">
  <img src="/01_uncertainty/fig1.png" alt="drawing" width="80%"/> <br>
  <span style="color:gray; font-size:0.8em;"><b>Figure 1:</b> (A) Point-wise prediction of days to re-admission for patient A (blue) and patient B (orange). No degree of uncertainty is displayed. (B) Probabilistic prediction with uncertainty estimation in the form of a probability distribution around the predictions of patients A and B.</span>
</p>

These uncertainty estimates would be beneficial for a clinical specialist in putting the algorithmic prediction into context. In this blog post, we will briefly discuss several approaches to model this predictive uncertainty. Next, we will pick a recent implementation based on gradient boosting systems and provide a simple example in an emergency department setting.

### Modeling predictive uncertainty
Different approaches to model uncertainty using probabilistic algorithms have been described in the literature. From a statistical point of view, we can categorize these methods as either non-Bayesian (frequentist) and Bayesian. Furthermore, one would preferentially use algorithms that are -built on top of, or similar to- existing architectures that work well for that specific task, such as deep neural networks for image classification, a recurrent neural network for natural language processing, and so on. In medicine, we frequently deal with structured, tabular data, and it has been shown numerous times that gradient boosting systems are superior to other machine learning algorithms [1].

In brief, gradient boosting systems employ an ensemble of weak learners (here decision trees), which are combined in an iterative process. The aim is to sequentially improve model accuracy, where each tree attempts to correct the errors of the preceding stage. For an extensive description of gradient boosting in clinical medicine, see the attached reference [2]. 
A recent [paper](https://arxiv.org/abs/1910.03225) by Tony Duan, Anand Avati and colleagues describes the implementation of probabilistic predictions using gradient boosting systems, which in turn allows the quantification of uncertainty amongst these predictions [3].

### NGBoost: Natural Gradient Boosting for Probabilistic Prediction
NGBoost is a recently developed gradient boosting algorithm implemented in the Python language on top of scikit-learn. Complete source code and implementation details are available at [Github](https://stanfordmlgroup.github.io/projects/ngboost/). NGBoost is consists of three essential components: a set of base learners, the probability distribution, and a scoring role (_Figure 2_).

<p align="center">
  <img src="/01_uncertainty/fig2.png" alt="drawing" width="100%"/> <br>
  <span style="color:gray; font-size:0.8em;"><b>Figure 2:</b> Schematic overview of the NGBoost algorithm consisting of three components: base learners, a probability distribution and a scoring role. Image derived from the NGBoost <a href="https://stanfordmlgroup.github.io/projects/ngboost/">homepage</a>.</span>
</p>  

Most frequently, we use simple decision trees as base learners, but using more complex tree structures as base learners is definitely an option and should be explored further. The probability distribution needs to be compatible with the output variable, e.g., a Normal distribution if we want to predict a continuous variable. Our approach of modeling a probability distribution over the output results in a natural way to quantify those predictive uncertainties. The quality of our modeled distributions are evaluated by comparing them to the true distribution using a scoring rule. We will apply this framework to predict days of re-admission in an emergency department setting.

### NGBoost in practice
The emergency department (ED), with its highly condensed time frame for decision-making, represents a unique and challenging environment for algorithms to assist clinical specialists in their decision making. A frequent decision for clinical specialists to consider is to decide whether or not a patient can be discharged from the ED. A clinician has to ensure discharging is safe and that the patient will not re-admit to the hospital in a short notice. Therefore, we aim to develop an algorithm that predicts days to re-admission of an individual patient, ultimately assisting the clinical specialist in his decision-making.

We have access to a dataset consisting of 19.282 patient presentations to an ED with 11 variables collected during this presentation. These variables include simple characteristics, history, and several laboratory measurements. Also, it contains a variable which represents the numeric amount of days before the patient was re-admitted to the hospital:  
* Age  
* Sex  
* Time of presentation  
* Last admission (in days)  
* Clinical risk score MEDS   
* Amount of comorbidities  
* Amount of drugs taken  
* Respiratory rate  
* Hemoglobin level  
* Lactate level    
* CRP level   
* <b>Days of re-admission (outcome)</b>    

Using standard machine learning workflow, we will randomly partition this dataset into 70% to use for algorithm development (the ‘training’ dataset), and the remainder (30%) to use in evaluating the performance of our algorithm (the ‘test’ dataset). The corresponding Python code for loading and partitioning our data is:

```python
data = pd.read_csv('/data/emergency_department.csv') # Read data
X_data = data.drop(columns=['readmission_days'] # Extract 11 features to use for prediction
Y_data = data['readmission_days'] # Extract outcome variable
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.30) # Split our data into 70% train/30% test
```

We will initialize our NGBoost algorithm with standard settings: a simple decision tree as the base learner, a Normal distribution as output distribution to model, and the maximum likelihood estimate (MLE) as our scoring function. Next, we will train our NGBoost algorithm using data derived from the training dataset.

```python
ngb = NGBRegressor(Base=default_tree_learner, 
              Dist=Normal, 
              Score=MLE(), 
              natural_gradient=True,
              verbose=False)
ngb.fit(X_train, Y_train)
```

Once we trained the NGBoost algorithm, we can assess the overall performance of the NGBoost algorithm in the test dataset, which the algorithm was not exposed to before. We will use the root mean squared error (MSE) and negative log-likelihood (NLL) to assess overall performance. This results in the following numbers:

```python
RMSE in test dataset: 3.110
NLL in test dataset: 2.130
```

Overall, the performance of our algorithm can be considered reasonable. The real strength of our algorithms come to light when we look at individual predictions. Two examples are shown below (_Figure 3_), where we visualized the algorithm prediction, the normal distribution (density) amongst the prediction, and also the “true” days to re-admission.

<p align="center">
  <img src="/01_uncertainty/fig3.png" alt="drawing" width="100%"/> <br>
  <span style="color:gray; font-size:0.8em;"><b>Figure 3:</b> (A) Example of a prediction and its modeled normal distribution. We observe that the distribution around the prediction is tightly spaced. (B) Example of a prediction and its modeled normal distribution which shows a wider distribution compared to A. Also, we observe that the distance to the true label is greater than in example A.</span>
</p>  

The modeled distributions around the predictions provide us an estimation of the degree of uncertainty amongst a prediction. We can clearly observe the left prediction (_Figure 3A_) has a smaller distribution compared to the right prediction (_Figure 3B_), which also is reflected in the prediction being much closer to the real value.

### Conclusion
Machine learning algorithms have shown excellent discriminatory performance in medicine but to date still, require features such as uncertainty quantification. In this blog post, we employed NGBoost, a recent implementation of gradient boosting trees, to provide a probabilistic prediction in an emergency department dataset. We were able to predict days to re-admission for an individual patient, and most importantly, provide individual uncertainty measures amongst the prediction. These probabilistic predictions are the first step towards more complete machine learning algorithms for medicine.

**References**  
1. Fernandez-Delgado, M., Cernadas, E., Barro, S., and Amorim, D. Do we need hundreds of classifiers to solve real world classification problems? The Journal of Machine Learning Research, 15(1):3133–3181, 2014  
2. Zhang, Z., Zhao, Y., Canes, A., Steinberg, D., Lyashevska, O., & , . (2019). Predictive analytics with gradient boosting in clinical medicine. Annals of translational medicine, 7, 152.  
3. Duan, T., Avati, A., Ding, D., Basu, A., Andrew, N.G., & Schuler, A. (2019). NGBoost: Natural Gradient Boosting for Probabilistic Prediction. arXiv e-prints, arXiv:1910.03225.  